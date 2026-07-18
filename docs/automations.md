# Automation examples

Replace the example entity IDs with those created for your diffuser.

## Enable automatic diffusion when someone arrives

```yaml
alias: Hall diffuser when occupied
triggers:
  - trigger: state
    entity_id: binary_sensor.home_occupied
    to: "on"
actions:
  - action: select.select_option
    target:
      entity_id: select.scent_diffuser_preset
    data:
      option: Balanced
  - action: switch.turn_on
    target:
      entity_id: switch.scent_diffuser_automatic_diffusion
```

## Disable automatic diffusion overnight

```yaml
alias: Stop diffuser overnight
triggers:
  - trigger: time
    at: "22:30:00"
actions:
  - action: switch.turn_off
    target:
      entity_id: switch.scent_diffuser_automatic_diffusion
```

## Dispense once from another automation

```yaml
actions:
  - action: button.press
    target:
      entity_id: button.scent_diffuser_dispense_now
```
