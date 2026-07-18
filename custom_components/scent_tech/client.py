"""Persistent BLE client for Scent Tech diffusers."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
import logging
from time import monotonic
from collections.abc import Callable
from typing import Any

from bleak import BleakClient
from bleak.exc import BleakError
from bleak_retry_connector import establish_connection

from homeassistant.components import bluetooth
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from .const import (
    CHARACTERISTIC_UUID,
    COMMAND_OFF,
    COMMAND_ON,
    COMMAND_DEDUPLICATION_SECONDS,
    COMMAND_WAKE,
    MANUAL_DISPENSE_SECONDS,
    PAUSE_TIME_DEFAULT,
    PRESET_CUSTOM,
    PRESET_VALUES,
    SPRAY_DURATION_DEFAULT,
    SCHEDULE_ENABLED_DEFAULT,
)

_LOGGER = logging.getLogger(__name__)


@dataclass(slots=True)
class ScentTechDiagnostics:
    """Runtime diagnostics that contain no credentials."""

    commands_requested: int = 0
    commands_written: int = 0
    commands_deduplicated: int = 0
    connection_attempts: int = 0
    connections_established: int = 0
    unexpected_disconnects: int = 0
    connection_failures: int = 0
    last_command: str | None = None
    last_notification: str | None = None
    last_error: str | None = None


class ScentTechClient:
    """Maintain one BLE connection and serialize commands to a diffuser."""

    def __init__(
        self,
        hass: HomeAssistant,
        address: str,
        name: str,
        *,
        send_wake_packet: bool,
    ) -> None:
        """Initialize the BLE client."""
        self._hass = hass
        self.address = address
        self.name = name
        self.send_wake_packet = send_wake_packet
        self.diagnostics = ScentTechDiagnostics()
        self._lock = asyncio.Lock()
        self._dispense_lock = asyncio.Lock()
        self._client: BleakClient | None = None
        self._closing = False
        self._last_payload: bytes | None = None
        self._last_write_at = 0.0
        self.spray_duration = SPRAY_DURATION_DEFAULT
        self.pause_time = PAUSE_TIME_DEFAULT
        self.schedule_enabled = SCHEDULE_ENABLED_DEFAULT
        self._listeners: set[Callable[[], None]] = set()

    @property
    def intensity(self) -> int:
        """Backward-compatible alias for spray duration."""
        return self.spray_duration

    @property
    def stop_time(self) -> int:
        """Backward-compatible alias for pause time."""
        return self.pause_time

    @property
    def preset(self) -> str:
        """Return the matching preset or Custom."""
        for name, values in PRESET_VALUES.items():
            if values == (self.spray_duration, self.pause_time):
                return name
        return PRESET_CUSTOM

    def async_add_listener(self, listener: Callable[[], None]) -> Callable[[], None]:
        """Register an entity state listener."""
        self._listeners.add(listener)
        return lambda: self._listeners.discard(listener)

    def _notify_listeners(self) -> None:
        """Notify entities after local state changes."""
        for listener in tuple(self._listeners):
            listener()

    @property
    def is_connected(self) -> bool:
        """Return whether the persistent BLE session is connected."""
        return self._client is not None and self._client.is_connected

    def _disconnected(self, client: BleakClient) -> None:
        """Handle a disconnect reported by Bleak."""
        if client is not self._client:
            return
        self._client = None
        if not self._closing:
            self.diagnostics.unexpected_disconnects += 1
            _LOGGER.debug("Scent Tech diffuser %s disconnected", self.address)

    def _notification(self, _sender: Any, data: bytearray) -> None:
        """Record notifications for diagnostics and protocol analysis."""
        value = bytes(data).hex()
        self.diagnostics.last_notification = value
        _LOGGER.debug("Notification from %s: %s", self.address, value)

    async def _async_connect(self) -> BleakClient:
        """Return the live persistent client, connecting once when needed."""
        if self.is_connected:
            return self._client  # type: ignore[return-value]

        ble_device = bluetooth.async_ble_device_from_address(
            self._hass, self.address, connectable=True
        )
        if ble_device is None:
            detail = bluetooth.async_address_reachability_diagnostics(
                self._hass,
                self.address,
                bluetooth.BluetoothReachabilityIntent.CONNECTION,
            )
            message = f"Diffuser {self.address} is not reachable over Bluetooth: {detail}"
            self.diagnostics.connection_failures += 1
            self.diagnostics.last_error = message
            raise HomeAssistantError(message)

        self.diagnostics.connection_attempts += 1
        _LOGGER.debug("Connecting to Scent Tech diffuser %s", self.address)
        try:
            client = await establish_connection(
                client_class=BleakClient,
                device=ble_device,
                name=self.name,
                max_attempts=1,
            )
            client.set_disconnected_callback(self._disconnected)
            self._client = client
            self.diagnostics.connections_established += 1
            self.diagnostics.last_error = None

            # The captured application traffic uses the same FFE1 characteristic
            # for writes and notifications. Failure to subscribe must not prevent
            # the proven ON/OFF writes from working.
            try:
                await client.start_notify(CHARACTERISTIC_UUID, self._notification)
                _LOGGER.debug("Subscribed to notifications from %s", self.address)
            except (BleakError, TimeoutError, OSError) as err:
                _LOGGER.debug(
                    "Notification subscription unavailable for %s: %s",
                    self.address,
                    err,
                )

            _LOGGER.debug("Persistent connection established to %s", self.address)
            return client
        except (BleakError, TimeoutError, OSError) as err:
            message = f"Unable to connect to diffuser: {err}"
            self.diagnostics.connection_failures += 1
            self.diagnostics.last_error = message
            raise HomeAssistantError(message) from err


    @staticmethod
    def _build_packet(command: int, data: bytes) -> bytes:
        """Build a framed Scent Tech packet with its protocol checksum."""
        length = 1 + len(data)
        body = bytes((length, command)) + data
        checksum = (0x101 - sum(body)) & 0xFF
        return b"\x55\xaa" + body + bytes((checksum, 0x5A))

    def build_settings_packet(
        self, spray_duration: int, pause_time: int, schedule_enabled: bool
    ) -> bytes:
        """Build command 0x14 containing schedule state and cycle settings."""
        data = (
            bytes((1 if schedule_enabled else 0,))
            + bytes.fromhex("01ff00e0016405")
            + spray_duration.to_bytes(2, "little")
            + pause_time.to_bytes(2, "little")
            + bytes.fromhex("01000000")
        )
        return self._build_packet(0x14, data)

    async def async_set_settings(
        self,
        *,
        spray_duration: int | None = None,
        pause_time: int | None = None,
        intensity: int | None = None,
        stop_time: int | None = None,
    ) -> bool:
        """Write the complete settings packet, preserving the other setting.

        intensity and stop_time remain accepted for upgrades from earlier builds.
        """
        if spray_duration is None:
            spray_duration = intensity
        if pause_time is None:
            pause_time = stop_time
        new_duration = self.spray_duration if spray_duration is None else spray_duration
        new_pause = self.pause_time if pause_time is None else pause_time
        payload = self.build_settings_packet(
            new_duration, new_pause, self.schedule_enabled
        )
        written = await self.async_send(payload)
        if written:
            self.spray_duration = new_duration
            self.pause_time = new_pause
            self._notify_listeners()
        return written

    async def async_set_schedule(self, enabled: bool) -> bool:
        """Enable or disable the stored repeating spray/pause cycle."""
        payload = self.build_settings_packet(
            self.spray_duration, self.pause_time, enabled
        )
        written = await self.async_send(payload)
        if written:
            self.schedule_enabled = enabled
            self._notify_listeners()
        return written

    async def async_dispense_now(self) -> None:
        """Run one short manual fragrance burst without changing the schedule."""
        async with self._dispense_lock:
            await self.async_send(COMMAND_ON)
            try:
                await asyncio.sleep(MANUAL_DISPENSE_SECONDS)
            finally:
                # Always request stop after a successful start, including if Home
                # Assistant cancels the button action during the delay.
                await asyncio.shield(self.async_send(COMMAND_OFF))

    async def async_set_preset(self, preset: str) -> bool:
        """Apply one of the predefined fragrance presets in one BLE write."""
        try:
            duration, pause = PRESET_VALUES[preset]
        except KeyError as err:
            raise HomeAssistantError(f"Unsupported preset: {preset}") from err
        return await self.async_set_settings(
            spray_duration=duration, pause_time=pause
        )

    async def async_send(self, payload: bytes) -> bool:
        """Send one packet on the persistent session.

        Return False when a rapid duplicate is deliberately suppressed.
        """
        self.diagnostics.commands_requested += 1

        async with self._lock:
            now = monotonic()
            if (
                payload == self._last_payload
                and now - self._last_write_at < COMMAND_DEDUPLICATION_SECONDS
            ):
                self.diagnostics.commands_deduplicated += 1
                _LOGGER.warning(
                    "Suppressed duplicate Scent Tech command %s for %s",
                    payload.hex(),
                    self.address,
                )
                return False

            client = await self._async_connect()
            try:
                if self.send_wake_packet:
                    _LOGGER.debug(
                        "Writing optional wake packet %s to %s",
                        COMMAND_WAKE.hex(),
                        self.address,
                    )
                    await client.write_gatt_char(
                        CHARACTERISTIC_UUID, COMMAND_WAKE, response=False
                    )
                    await asyncio.sleep(0.15)

                _LOGGER.debug(
                    "Writing one Scent Tech command %s to %s",
                    payload.hex(),
                    self.address,
                )
                await client.write_gatt_char(
                    CHARACTERISTIC_UUID, payload, response=False
                )

                self._last_payload = payload
                self._last_write_at = monotonic()
                self.diagnostics.commands_written += 1
                self.diagnostics.last_command = payload.hex()
                self.diagnostics.last_error = None
                return True
            except (BleakError, TimeoutError, OSError) as err:
                # Do not automatically replay a command: a failed acknowledgement
                # does not prove the diffuser failed to execute it, and replaying can
                # create duplicate beeps/actions.
                self._client = None
                try:
                    if client.is_connected:
                        await client.disconnect()
                except (BleakError, TimeoutError, OSError):
                    pass
                message = f"Unable to send command to diffuser: {err}"
                self.diagnostics.connection_failures += 1
                self.diagnostics.last_error = message
                raise HomeAssistantError(message) from err

    async def async_disconnect(self) -> None:
        """Close the persistent BLE session during integration unload."""
        async with self._lock:
            self._closing = True
            client = self._client
            self._client = None
            if client is None or not client.is_connected:
                return
            try:
                _LOGGER.debug("Disconnecting from Scent Tech diffuser %s", self.address)
                await client.disconnect()
            except (BleakError, TimeoutError, OSError) as err:
                _LOGGER.debug("Error disconnecting from %s: %s", self.address, err)
