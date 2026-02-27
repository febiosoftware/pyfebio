from typing import Literal

from pydantic_xml import BaseXmlModel, attr, element

from ._types import (
    StringFloatVec3,
)


class Scale(BaseXmlModel, validate_assignment=True):
    lc: int = attr()
    text: float | StringFloatVec3 = 1.0


class NodalLoad(BaseXmlModel, tag="nodal_load", validate_assignment=True):
    type: Literal["nodal_load"] = attr(default="nodal_load", frozen=True)
    node_set: str = attr()
    dof: Literal["x", "y", "z", "p"] = element(default="z")
    scale: Scale = element(default=Scale(lc=1))


class NodalForce(BaseXmlModel, tag="nodal_load", validate_assignment=True):
    type: Literal["nodal_force"] = attr(default="nodal_force", frozen=True)
    node_set: str = attr()
    value: Scale = element(default=Scale(lc=1, text="0.0,0.0,1.0"))


class NodalTargetForce(BaseXmlModel, tag="nodal_load", validate_assignment=True):
    type: Literal["nodal_target_force"] = attr(default="nodal_target_force", frozen=True)
    node_set: str = attr()
    force: StringFloatVec3 = element(default="0.0,0.0,1.0")
    scale: Scale = element(default=Scale(lc=1))


NodalLoadType = NodalLoad | NodalForce | NodalTargetForce


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


class Loads(BaseXmlModel, validate_assignment=True):
    all_surface_loads: list[TractionLoad | PressureLoad | FluidFlux | FluidPressure] = element(default=[])
    all_nodal_loads: list[NodalLoadType] = element(default=[])

    def add_surface_load(self, new_load: PressureLoad | TractionLoad | FluidFlux | FluidPressure):
        self.all_surface_loads.append(new_load)

    def add_nodal_load(self, new_load: NodalLoadType):
        self.all_nodal_loads.append(new_load)
