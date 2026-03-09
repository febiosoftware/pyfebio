from typing import Literal

from pydantic_xml import BaseXmlModel, attr, element

from ._types import (
    StringFloatVec2,
)


class CurvePoints(BaseXmlModel, validate_assignment=True):
    points: list[StringFloatVec2] = element(default=[], tag="pt")

    def add_point(self, new_point: StringFloatVec2):
        self.points.append(new_point)


class LoadCurve(BaseXmlModel, tag="load_controller", validate_assignment=True):
    id: int = attr()
    type: Literal["loadcurve"] = attr(default="loadcurve", frozen=True)
    interpolate: Literal["LINEAR", "STEP", "SMOOTH"] = element(default="LINEAR")
    extend: Literal["CONSTANT", "EXTRAPOLATE", "REPEAT", "REPEAT OFFSET"] = element(default="CONSTANT")
    points: CurvePoints = element()


class PIDController(BaseXmlModel, validate_assignment=True):
    id: int = attr()
    type: Literal["PID"] = attr(default="PID", frozen=True)
    var: str = element()
    target: float = element()
    Kp: float = element()
    Kd: float = element()
    Ki: float = element()


class MathController(BaseXmlModel, validate_assignment=True):
    id: int = attr()
    type: Literal["math"] = attr(default="math", frozen=True)
    math: str = element()


class LoadData(BaseXmlModel, validate_assignment=True):
    load_controllers: list[LoadCurve | PIDController | MathController] = element(default=[], tag="load_controller")

    def add_load_curve(self, new_load_curve: LoadCurve):
        assert isinstance(new_load_curve, LoadCurve), "new_load_curve must be a LoadCurve"
        self.load_controllers.append(new_load_curve)

    def add_pid_controller(self, new_pid_controller: PIDController):
        assert isinstance(new_pid_controller, PIDController), "new_pid_controller must be a PIDController"
        self.load_controllers.append(new_pid_controller)

    def add_math_controller(self, new_math_controller: MathController):
        assert isinstance(new_math_controller, MathController), "new_math_controller must be a MathController"
        self.load_controllers.append(new_math_controller)
