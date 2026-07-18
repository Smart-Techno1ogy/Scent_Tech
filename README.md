<p align="center">
  <img src="smart-technology-logo.png" alt="Smart Technology" width="620">
</p>

# Smart Technology Scent Diffuser

A local Bluetooth integration for compatible Smart Technology / Scent Tech BLE fragrance diffusers in Home Assistant.

## Features

- **Dispense now**: a three-second fragrance burst on demand.
- **Automatic diffusion**: enable or disable the repeating cycle.
- **Presets**: Light, Balanced, Strong, and Custom.
- **Spray duration**: 3–8 seconds.
- **Pause time**: 90–600 seconds.
- Persistent BLE connection for fast, quiet control.
- Multiple diffuser support.
- Local operation with no cloud account.

### Presets

| Preset | Spray duration | Pause time |
|---|---:|---:|
| Light | 3 s | 600 s |
| Balanced | 5 s | 300 s |
| Strong | 8 s | 120 s |
| Custom | User selected | User selected |

## Installation with HACS

Until the integration is accepted into the default HACS catalogue:

1. Open **HACS → Integrations**.
2. Open the menu and choose **Custom repositories**.
3. Add `https://github.com/Smart-Techno1ogy/Scent_Tech` as an **Integration**.
4. Find **Smart Technology Scent Diffuser** and select **Download**.
5. Restart Home Assistant.
6. Open **Settings → Devices & services → Add integration** and search for **Smart Technology Scent Diffuser**.

## Manual installation

Copy `custom_components/scent_tech` into your Home Assistant `/config/custom_components/` directory, then restart Home Assistant.

## Usage

- Press **Dispense now** for a single short burst.
- Select a preset or adjust the advanced spray and pause values.
- Enable **Automatic diffusion** to run the repeating cycle.

Home Assistant may decide the final ordering of entities on the device page. A custom dashboard card can provide a fixed preferred order.

## Supported devices

Tested with the Scent Tech B30N BLE diffuser advertising a local name beginning with `Scent-` and using the FFE0/FFE1 GATT service and characteristic.

## Support

Please open a GitHub issue and attach the Home Assistant integration diagnostics. Do not publish secrets or unrelated Home Assistant configuration.

## Licence

MIT
