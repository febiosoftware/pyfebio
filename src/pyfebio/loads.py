from typing import Literal

from pydantic_xml import BaseXmlModel, attr, element

from ._types import (
    StringFloatVec3,
)


class Scale(BaseXmlModel, validate_assignment=True):
    lc: int | None = attr(default=None)
    text: float | StringFloatVec3 = 1.0


class ScaleMath(BaseXmlModel, validate_assignment=True):
    lc: int | None = attr(default=None)
    text: float | str = 0.0


class NodalLoad(BaseXmlModel, tag="nodal_load", validate_assignment=True):
    type: Literal["nodal_load"] = attr(default="nodal_load", frozen=True)
    node_set: str = attr()
    relative: Literal[0, 1] = element(default=0)
    dof: Literal["x", "y", "z", "p"] = element(default="z")
    scale: Scale = element(default=Scale(lc=1))


class NodalForce(BaseXmlModel, tag="nodal_load", validate_assignment=True):
    type: Literal["nodal_force"] = attr(default="nodal_force", frozen=True)
    node_set: str = attr()
    relative: Literal[0, 1] = element(default=0)
    value: Scale = element(default=Scale(lc=1, text="0.0,0.0,1.0"))


class NodalTargetForce(BaseXmlModel, tag="nodal_load", validate_assignment=True):
    type: Literal["nodal_target_force"] = attr(default="nodal_target_force", frozen=True)
    node_set: str = attr()
    force: StringFloatVec3 = element(default="0.0,0.0,1.0")
    scale: Scale = element(default=Scale(lc=1))


class NodalFluidFlux(BaseXmlModel, tag="nodal_load", validate_assignment=True):
    type: Literal["nodal fluidflux"] = attr(default="nodal fluidflux", frozen=True)
    node_set: str = attr()
    relative: Literal[0, 1] = element(default=0)
    value: Scale = element()


NodalLoadType = NodalLoad | NodalForce | NodalTargetForce | NodalFluidFlux


class FluidFlux(BaseXmlModel, tag="surface_load", validate_assignment=True):
    type: Literal["fluidflux"] = attr(default="fluidflux", frozen=True)
    surface: str = attr()
    flux: Scale = element(default=Scale(lc=1, text=0.0001))
    linear: Literal[0, 1] = element(default=0)
    mixture: Literal[0, 1] = element(default=1)


class TractionLoad(BaseXmlModel, tag="surface_load", validate_assignment=True):
    type: Literal["traction"] = attr(default="traction", frozen=True)
    surface: str = attr()
    scale: Scale = element(default=Scale(lc=1))
    traction: StringFloatVec3 = element(default="0,0,1")


class PressureLoad(BaseXmlModel, tag="surface_load", validate_assignment=True):
    type: Literal["pressure"] = attr(default="pressure", frozen=True)
    surface: str = attr()
    symmetric_stiffness: Literal[0, 1] = element(default=0)
    linear: Literal[0, 1] = element(default=0)
    shell_bottom: Literal[0, 1] = element(default=0)
    pressure: Scale = element(default=Scale(lc=1))


class FluidPressure(BaseXmlModel, tag="surface_load", validate_assignment=True):
    type: Literal["fluid pressure"] = attr(default="fluid pressure", frozen=True)
    surface: str = attr()
    pressure: Scale = element(default=Scale(lc=1, text=0.1))


class ConstantBodyForce(BaseXmlModel, tag="body_load", validate_assignment=True):
    type: Literal["const"] = attr(default="const", frozen=True)
    x: Scale = element(default=Scale(text=0.0))
    y: Scale = element(default=Scale(text=0.0))
    z: Scale = element(default=Scale(text=9.81))


class NonConstantBodyForce(BaseXmlModel, tag="body_load", validate_assignment=True):
    type: Literal["non-const"] = attr(default="non-const", frozen=True)
    x: ScaleMath = element(default=ScaleMath(text=0.0))
    y: ScaleMath = element(default=ScaleMath(text=0.0))
    z: ScaleMath = element(default=ScaleMath(text="9.81*Z"))


class CentrifugalBodyForce(BaseXmlModel, tag="body_load", validate_assignment=True):
    type: Literal["centrifugal"] = attr(default="centrifugal", frozen=True)
    angular_speed: float = element(default=0.0)
    rotation_axis: StringFloatVec3 = element(default="0.0,0.0,1.0")
    rotation_center: StringFloatVec3 = element(default="0.0,0.0,0.0")


class MovingFrame(BaseXmlModel, tag="body_load", validate_assignment=True):
    type: Literal["moving frame"] = attr(default="moving frame", frozen=True)
    wx: Scale = element(default=Scale(text=0.0))
    wy: Scale = element(default=Scale(text=0.0))
    wz: Scale = element(default=Scale(text=0.0))
    ax: Scale = element(default=Scale(text=0.0))
    ay: Scale = element(default=Scale(text=0.0))
    az: Scale = element(default=Scale(text=0.0))


class MassDamping(BaseXmlModel, tag="body_load", validate_assignment=True):
    type: Literal["mass damping"] = attr(default="mass damping", frozen=True)
    C: float = element(default=0.0)


BodyLoadType = ConstantBodyForce | NonConstantBodyForce | CentrifugalBodyForce | MovingFrame | MassDamping


class Loads(BaseXmlModel, validate_assignment=True):
    all_surface_loads: list[TractionLoad | PressureLoad | FluidFlux | FluidPressure] = element(default=[])
    all_nodal_loads: list[NodalLoadType] = element(default=[])
    all_body_loads: list[BodyLoadType] = element(default=[])

    def add_surface_load(self, new_load: PressureLoad | TractionLoad | FluidFlux | FluidPressure):
        assert isinstance(new_load, (PressureLoad, TractionLoad, FluidFlux, FluidPressure)), (
            "new_load must be a PressureLoad, TractionLoad, FluidFlux, or FluidPressure"
        )
        self.all_surface_loads.append(new_load)

    def add_nodal_load(self, new_load: NodalLoadType):
        assert isinstance(new_load, NodalLoadType), "new_load must be a NodalLoadType"
        self.all_nodal_loads.append(new_load)

    def add_body_load(self, new_load: BodyLoadType):
        assert isinstance(new_load, BodyLoadType), "new_load must be a BodyLoadType"
        self.all_body_loads.append(new_load)
