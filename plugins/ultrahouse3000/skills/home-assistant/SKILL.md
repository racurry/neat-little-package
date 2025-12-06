---
name: home-assistant
description: Guidance for Home Assistant configurations. Use when writing automations, dashboards, or service calls for HA.
---

# Home Assistant Skill

**Fetch official docs for current syntax** - HA evolves rapidly:

- <https://www.home-assistant.io/docs/automation/> - Automation syntax
- <https://www.home-assistant.io/integrations/> - All integrations
- <https://www.home-assistant.io/dashboards/> - Dashboard config

## Quality Checklist

- [ ] Use modern service syntax: `target:` + `data:`, not `entity_id:` at root
- [ ] Automations have unique `id` and explicit `mode`
- [ ] Secrets via `!secret`, never hardcoded
- [ ] Templates tested in Developer Tools → Template
- [ ] Check entity availability for unreliable devices

## Common Pitfalls

### Legacy Syntax

Claude may generate deprecated patterns. Use modern syntax:

```yaml
# Wrong: deprecated
service: homeassistant.turn_on
entity_id: light.porch

# Right: modern
service: light.turn_on
target:
  entity_id: light.porch
```

Automations need `id` and `mode`:

```yaml
automation:
  - id: porch_light_sunset
    alias: "Porch light at sunset"
    mode: single  # or restart, queued, parallel
    trigger:
      - platform: sun
        event: sunset
    action:
      - service: light.turn_on
        target:
          entity_id: light.porch
```

### Missing Availability Checks

Unreliable devices need guards:

```yaml
action:
  - choose:
      - conditions:
          - condition: template
            value_template: >
              {{ states('light.unreliable_bulb') not in ['unavailable', 'unknown'] }}
        sequence:
          - service: light.turn_on
            target:
              entity_id: light.unreliable_bulb
```

### Trigger Spam

State triggers fire on every change. Use thresholds or debounce:

```yaml
# Threshold: only fires when crossing
trigger:
  - platform: numeric_state
    entity_id: sensor.temperature
    above: 75

# Debounce: must stay in state
trigger:
  - platform: state
    entity_id: sensor.temperature
    for:
      minutes: 5
```

### Hardcoded Values

Use templates for dynamic content:

```yaml
# Bad
message: "Front door opened"

# Good
message: "Front door opened at {{ now().strftime('%I:%M %p') }}"
```
