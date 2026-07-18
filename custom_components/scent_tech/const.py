"""Constants for the Smart Technology Scent Diffuser integration."""

from __future__ import annotations

from typing import Final

from homeassistant.const import Platform

DOMAIN: Final = "scent_tech"
PLATFORMS: Final = [
    Platform.BUTTON,
    Platform.SWITCH,
    Platform.SELECT,
    Platform.NUMBER,
]

CONF_ADDRESS: Final = "address"
CONF_NAME: Final = "name"
CONF_SEND_WAKE: Final = "send_wake_packet"

DEFAULT_NAME: Final = "Scent Diffuser"
DEFAULT_SEND_WAKE: Final = False

SERVICE_UUID: Final = "0000ffe0-0000-1000-8000-00805f9b34fb"
CHARACTERISTIC_UUID: Final = "0000ffe1-0000-1000-8000-00805f9b34fb"

COMMAND_ON: Final = bytes.fromhex("55aa0407120100e35a")
COMMAND_OFF: Final = bytes.fromhex("55aa0407120000e45a")
COMMAND_WAKE: Final = bytes.fromhex("55aa0147b95a")

MANUAL_DISPENSE_SECONDS: Final = 3

SPRAY_DURATION_MIN: Final = 3
SPRAY_DURATION_MAX: Final = 8
SPRAY_DURATION_DEFAULT: Final = 5
PAUSE_TIME_MIN: Final = 90
PAUSE_TIME_MAX: Final = 600
PAUSE_TIME_STEP: Final = 30
PAUSE_TIME_DEFAULT: Final = 300
SCHEDULE_ENABLED_DEFAULT: Final = False

PRESET_LIGHT: Final = "Light"
PRESET_BALANCED: Final = "Balanced"
PRESET_INTENSE: Final = "Intense"
PRESET_CUSTOM: Final = "Custom"
PRESET_OPTIONS: Final = [
    PRESET_LIGHT,
    PRESET_BALANCED,
    PRESET_INTENSE,
    PRESET_CUSTOM,
]
PRESET_VALUES: Final = {
    PRESET_LIGHT: (3, 600),
    PRESET_BALANCED: (5, 300),
    PRESET_INTENSE: (8, 120),
}

MANUFACTURER: Final = "Smart Technology"
MODEL: Final = "Scent Tech B30N BLE Diffuser"

COMMAND_DEDUPLICATION_SECONDS: Final = 1.5
