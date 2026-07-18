# BLE protocol notes

This document records the portions of the Scent Tech BLE protocol confirmed during development. Values are hexadecimal unless stated otherwise.

## Transport

- Service UUID: `0000FFE0-0000-1000-8000-00805F9B34FB`
- Characteristic UUID: `0000FFE1-0000-1000-8000-00805F9B34FB`
- Commands are written without response.

## Frame

```text
55 AA [length] [command] [data...] [checksum] 5A
```

`length` covers the command byte and data bytes. The checksum is:

```text
(0x101 - sum(length + command + data bytes)) & 0xFF
```

## Manual power commands

```text
ON   55 AA 04 07 12 01 00 E3 5A
OFF  55 AA 04 07 12 00 00 E4 5A
```

The **Dispense now** button sends ON, waits three seconds, then sends OFF.

## Automatic diffusion settings

Command `0x14` stores the automatic-mode flag, spray duration, and pause time in one packet:

```text
55 AA 11 14
[schedule enabled: 00/01]
01 FF 00 E0 01 64 05
[spray duration, uint16 little-endian]
[pause time, uint16 little-endian]
01 00 00 00
[checksum] 5A
```

Confirmed ranges used by the manufacturer app:

- Spray duration: 3–8 seconds
- Pause time: 90–600 seconds, in 30-second steps

Example: enabled, 8-second spray, 90-second pause:

```text
55 AA 11 14 01 01 FF 00 E0 01 64 05 08 00 5A 00 01 00 00 00 2E 5A
```

## Optional wake packet

```text
55 AA 01 47 B9 5A
```

This is disabled by default because the confirmed single-write commands work without it and it may cause extra beeps. It can be enabled in the integration options for hardware that requires it.
