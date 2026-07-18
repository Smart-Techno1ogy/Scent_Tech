# Troubleshooting

## The diffuser is not discovered

- Confirm it is powered on and nearby.
- Confirm Home Assistant has a working Bluetooth adapter or Bluetooth proxy.
- Look for a device name beginning with `Scent-`.
- Use manual setup with the Bluetooth address if discovery does not appear.

## Commands time out or the device becomes unavailable

- Move the diffuser closer to the Bluetooth adapter or proxy.
- Avoid connecting to the diffuser from the manufacturer app at the same time.
- Reload the integration after closing the manufacturer app.
- Download integration diagnostics and attach them to a GitHub issue.

## The diffuser beeps but does not react

Open the integration's **Configure** dialog and try enabling **Send wake packet before commands**. Leave this disabled when normal commands already work, because it can produce additional beeps.

## Automatic diffusion does not start

Choose a preset or set the custom spray and pause values first, then enable **Automatic diffusion**. The switch controls the repeating cycle; **Dispense now** is a separate one-shot action.
