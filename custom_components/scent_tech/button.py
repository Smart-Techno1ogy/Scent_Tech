"""Button platform for Smart Technology BLE scent diffusers."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import ScentTechConfigEntry
from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ScentTechConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the manual dispense button."""
    async_add_entities([ScentTechDispenseButton(entry)])


class ScentTechDispenseButton(ButtonEntity):
    """Dispense a short burst of fragrance on demand."""

    _attr_has_entity_name = True
    _attr_name = "Dispense now"
    _attr_icon = "mdi:spray"
    _attr_should_poll = False

    def __init__(self, entry: ScentTechConfigEntry) -> None:
        self._client = entry.runtime_data
        self._attr_unique_id = f"{self._client.address}_dispense_now"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._client.address)},
            connections={("bluetooth", self._client.address)},
            name=self._client.name,
            manufacturer="Smart Technology",
            model="Scent Tech B30N BLE Diffuser",
        )

    @property
    def available(self) -> bool:
        """Allow a press to establish or restore the BLE connection."""
        return True

    async def async_press(self) -> None:
        """Dispense one three-second fragrance burst."""
        await self._client.async_dispense_now()
