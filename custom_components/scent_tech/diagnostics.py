"""Diagnostics support for the Smart Technology Scent Diffuser integration."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.redact import async_redact_data

from . import ScentTechConfigEntry
from .const import CONF_ADDRESS, MANUAL_DISPENSE_SECONDS


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ScentTechConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for one diffuser without secrets."""
    client = entry.runtime_data
    return {
        "entry": {
            "title": entry.title,
            "version": entry.version,
            "minor_version": entry.minor_version,
            "data": async_redact_data(dict(entry.data), {CONF_ADDRESS}),
            "options": dict(entry.options),
        },
        "device": {
            "address": "**REDACTED**",
            "name": client.name,
            "connected": client.is_connected,
        },
        "controls": {
            "automatic_diffusion": client.schedule_enabled,
            "preset": client.preset,
            "spray_duration_seconds": client.spray_duration,
            "pause_time_seconds": client.pause_time,
            "manual_dispense_seconds": MANUAL_DISPENSE_SECONDS,
        },
        "ble": asdict(client.diagnostics),
    }
