<p align="center">
  <img src="smart-technology-logo.png" alt="Smart Technology" width="620">
</p>

# Smart Technology Scent Diffuser

Control compatible Smart Technology / Scent Tech Bluetooth fragrance diffusers locally from Home Assistant—without the manufacturer app or a cloud account.

[![HACS Validation](https://github.com/Smart-Techno1ogy/Scent_Tech/actions/workflows/hacs.yml/badge.svg)](https://github.com/Smart-Techno1ogy/Scent_Tech/actions/workflows/hacs.yml)
[![Hassfest](https://github.com/Smart-Techno1ogy/Scent_Tech/actions/workflows/hassfest.yml/badge.svg)](https://github.com/Smart-Techno1ogy/Scent_Tech/actions/workflows/hassfest.yml)
[![GitHub Release](https://img.shields.io/github/v/release/Smart-Techno1ogy/Scent_Tech)](https://github.com/Smart-Techno1ogy/Scent_Tech/releases)
[![License](https://img.shields.io/github/license/Smart-Techno1ogy/Scent_Tech)](LICENSE)

## Controls

- **Dispense now** — one three-second fragrance burst on demand.
- **Automatic diffusion** — enable or disable the repeating spray/pause cycle.
- **Preset** — Light, Balanced, Intense, or Custom.
- **Spray duration** — 3–8 seconds.
- **Pause time** — 90–600 seconds.

The integration maintains a local BLE connection for quick control and supports multiple diffusers. Home Assistant determines the final ordering of mixed entity types on the device page; a dashboard card can enforce a preferred order.

### Presets

| Preset | Spray duration | Pause time |
|---|---:|---:|
| Light | 3 s | 600 s |
| Balanced | 5 s | 300 s |
| Intense | 8 s | 120 s |
| Custom | User selected | User selected |

## Installation with HACS

Until the integration is included in the default HACS catalogue:

1. Open **HACS → Integrations**.
2. Open the menu and choose **Custom repositories**.
3. Add `https://github.com/Smart-Techno1ogy/Scent_Tech` with category **Integration**.
4. Find **Smart Technology Scent Diffuser** and select **Download**.
5. Restart Home Assistant.
6. Open **Settings → Devices & services → Add integration** and search for **Smart Technology Scent Diffuser**.

## Manual installation

Copy `custom_components/scent_tech` into `/config/custom_components/` and restart Home Assistant.

## Setup and use

Keep the diffuser powered on and within Bluetooth range. Home Assistant should discover devices advertising a name beginning with `Scent-`; manual setup using the Bluetooth address is also available.

For automatic operation, first select a preset (or set custom spray and pause values), then enable **Automatic diffusion**. Press **Dispense now** whenever you want a single immediate burst.

## Supported hardware

Tested with the Scent Tech B30N BLE diffuser using the FFE0 service and FFE1 characteristic. Other models using the same protocol may work but have not yet been confirmed.

## Automations and protocol

- [Automation examples](docs/automations.md)
- [BLE protocol notes](docs/protocol.md)
- [Troubleshooting](docs/troubleshooting.md)

## Support

Open a [GitHub issue](https://github.com/Smart-Techno1ogy/Scent_Tech/issues) and attach the integration diagnostics from Home Assistant. Bluetooth addresses are redacted from diagnostics, but review files before publishing them.

## Acknowledgements

The BLE protocol was decoded from captured traffic and tested on a Smart Technology B30N diffuser. Protocol analysis and the Home Assistant implementation were developed collaboratively with ChatGPT.

## Licence

MIT
