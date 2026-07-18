"""Scent Tech BLE diffuser integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .client import ScentTechClient
from .const import (
    CONF_ADDRESS,
    CONF_NAME,
    CONF_SEND_WAKE,
    DEFAULT_SEND_WAKE,
    PLATFORMS,
)

type ScentTechConfigEntry = ConfigEntry[ScentTechClient]


async def async_setup_entry(
    hass: HomeAssistant, entry: ScentTechConfigEntry
) -> bool:
    """Set up Scent Tech from a config entry."""
    entry.runtime_data = ScentTechClient(
        hass,
        entry.data[CONF_ADDRESS],
        entry.data[CONF_NAME],
        send_wake_packet=entry.options.get(CONF_SEND_WAKE, DEFAULT_SEND_WAKE),
    )
    entry.async_on_unload(entry.add_update_listener(_async_options_updated))
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def _async_options_updated(
    hass: HomeAssistant, entry: ScentTechConfigEntry
) -> None:
    """Reload after options change."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(
    hass: HomeAssistant, entry: ScentTechConfigEntry
) -> bool:
    """Unload a config entry."""
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        await entry.runtime_data.async_disconnect()
    return unloaded
