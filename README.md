# ad-powerfsm

_Power-based Finite State Machines for [Home Assistant](https://www.home-assistant.io/)/[AppDaemon](https://www.home-assistant.io/docs/ecosystem/appdaemon/)._

## Installation

This app is best installed using [HACS](https://github.com/custom-components/hacs), so that you can easily track and download updates.

Alternatively, download the `powerfsm` directory from inside the `apps` directory here to your local `apps` directory, then add the configuration to enable the `powerfsm` module.

## App configuration

```yaml
lounge_tv_state:
  module: powerfsm
  class: PowerFSM
  power_sensor: sensor.lounge_tv:current_power_w
  idle_power: 10
  idle_timeout: 0
  idle_state: Standby
  work_state: On
```

key | optional | type | default | description
-- | -- | -- | -- | --
`module` | False | string | | The module name of the app.
`class` | False | string | | The name of the Class.
`power_sensor` | False | AttributeDefinition | | The entity_id of the HACS sensor.
`idle_power` | False | number | | Power below or equal to which the device is idle
`idle_timeout` | True | TimeDuration | 0 | How long the consumption must fall below idle_power to trigger a transition
`idle_state` | True | string | Idle | Name of the state when idle
`work_state` | True | string | Working | Name of the state when working
`attn_state` | True | string | Needs Attention | Name of the state when attenion is required
`requires_attn` | True | boolean | False | Requires attention to transition from working to idle

### Types

#### AttributeDefinition

An entity id with an optional state attribute suffix separated with a colon. e.g., `sensor.dish_washer_power`, `switch.dish_washer:power`.

#### TimeDuration

A number will be interpreted as a value in seconds; `h`, `m`, `s` suffixes are supported. e.g., `1h30m`, `10m`, `30s`.
