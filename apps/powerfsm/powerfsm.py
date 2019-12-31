from enum import Enum

import appdaemon.plugins.hass.hassapi as hass

from fsm import Fsm, State, Transition, Condition, LE, GT


class States(Enum):
    IDLE = "IDLE"
    WORK = "WORK"
    ATTN = "ATTN"


def mk_state(mode, name, next_state, condition):
    return State(
        id=mode.value,
        name=name,
        attributes={"mode": mode.value},
        transitions=[
            Transition(
                id=f"{mode.value}_to_{next_state.value}",
                next=next_state.value,
                conditions=[condition],
            )
        ],
    )


class PowerFSM(hass.Hass):
    def initialize(self):
        entity_id = f'sensor.{self.args["id"]}'
        power_sensor = self.args["power_sensor"]
        power_sensor_attr = None
        if ":" in power_sensor:
            power_sensor, power_sensor_attr = power_sensor.split(":")
        idle_power = self.args["idle_power"]
        idle_timeout = self.args.get("idle_timeout", 0)
        idle_state = self.args.get("idle_state", "Idle")
        work_state = self.args.get("work_state", "Working")
        attn_state = self.args.get("attn_state", "Needs Attention")
        requires_attn = self.args.get("requires_attn", False)

        is_idle = Condition(
            id="is_idle",
            entity=power_sensor,
            attribute=power_sensor_attr,
            operator=LE,
            operand=idle_power,
            stability_time=idle_timeout,
        )
        is_working = Condition(
            id="is_working",
            entity=power_sensor,
            attribute=power_sensor_attr,
            operator=GT,
            operand=idle_power,
        )

        states = [
            mk_state(
                mode=States.IDLE,
                name=idle_state,
                next_state=States.WORK,
                condition=is_working,
            ),
            mk_state(
                mode=States.WORK,
                name=work_state,
                next_state=requires_attn and States.ATTN or States.IDLE,
                condition=is_idle,
            ),
        ]
        if requires_attn:
            states.append(
                mk_state(
                    mode=States.ATTN,
                    name=attn_state,
                    next_state=States.WORK,
                    condition=is_working,
                )
            )

        Fsm(self, id=self.args["id"], entity=entity_id, states=states)