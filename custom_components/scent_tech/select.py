"""Preset selector for Smart Technology scent diffusers."""

from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import ScentTechConfigEntry
from .const import DOMAIN, PRESET_CUSTOM, PRESET_OPTIONS


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ScentTechConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the fragrance strength preset selector."""
    async_add_entities([ScentTechPresetSelect(entry)])


class ScentTechPresetSelect(SelectEntity):
    """Select a coordinated spray-duration and pause-time preset."""

    _attr_has_entity_name = True
    _attr_name = "Preset"
    _attr_icon = "mdi:tune-variant"
    _attr_should_poll = False
    _attr_options = PRESET_OPTIONS

    def __init__(self, entry: ScentTechConfigEntry) -> None:
        self._client = entry.runtime_data
        self._attr_unique_id = f"{self._client.address}_preset"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._client.address)},
            connections={("bluetooth", self._client.address)},
            name=self._client.name,
            manufacturer="Smart Technology",
            model="Scent Tech B30N BLE Diffuser",
        )

    async def async_added_to_hass(self) -> None:
        self.async_on_remove(self._client.async_add_listener(self._handle_client_update))

    def _handle_client_update(self) -> None:
        self.async_write_ha_state()

    @property
    def current_option(self) -> str:
        return self._client.preset

    async def async_select_option(self, option: str) -> None:
        if option == PRESET_CUSTOM:
            return
        await self._client.async_set_preset(option)
