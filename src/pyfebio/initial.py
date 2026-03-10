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


class InitialFluidPressure(BaseXmlModel, tag="ic", validate_assignment=True):
    type: Literal["initial fluid pressure"] = attr(default="initial fluid pressure", frozen=True)
    node_set: str = attr()
    value: float = element()


class InitialConcentration(BaseXmlModel, tag="ic", validate_assignment=True):
    type: Literal["initial concentration"] = attr(default="initial concentration", frozen=True)
    node_set: str = attr()
    value: float = element()
    dof: str = element()


InitialConditionType = InitialVelocity | InitialPrestrain | InitialConcentration | InitialFluidPressure


class Initial(BaseXmlModel, validate_assignment=True):
    all_initial_conditions: list[InitialConditionType] = element(default=[], tag="ic")

    def add_initial_condition(self, new_initial_condition: InitialConditionType):
        assert isinstance(new_initial_condition, InitialConditionType), "new_initial_condition must be an InitialConditionType"
        self.all_initial_conditions.append(new_initial_condition)
