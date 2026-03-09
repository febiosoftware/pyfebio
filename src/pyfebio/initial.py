from typing import Literal

from pydantic_xml import BaseXmlModel, attr, element

from ._types import (
    StringFloatVec3,
)


class InitialVelocity(BaseXmlModel, validate_assignment=True):
    type: Literal["velocity", "shell_velocity", "initial fluid velocity"] = attr()
    node_set: str = attr()
    value: StringFloatVec3 = element(default="0.0,0.0,0.0")


class InitialPrestrain(BaseXmlModel, validate_assignment=True):
    type: Literal["prestrain"] = attr(default="prestrain", frozen=True)
    node_set: str = attr()
    init: Literal[0, 1] = element(default=1)
    reset: Literal[0, 1] = element(default=1)


class Initial(BaseXmlModel, validate_assignment=True):
    all_initial_conditions: list[InitialVelocity | InitialPrestrain] = element(default=[], tag="ic")

    def add_initial_condition(self, new_initial_condition: InitialVelocity | InitialPrestrain):
        assert isinstance(new_initial_condition, (InitialVelocity, InitialPrestrain)), (
            "new_initial_condition must be an InitialVelocity or InitialPrestrain"
        )
        self.all_initial_conditions.append(new_initial_condition)
