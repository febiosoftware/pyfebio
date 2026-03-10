from typing import Literal

from pydantic_xml import BaseXmlModel, attr, element

from ._types import (
    StringFloatVec3,
    StringFloatVec9,
)


class Value(BaseXmlModel, validate_assignment=True):
    lc: int = attr()
    text: float | StringFloatVec3 = 1.0


class BCZeroDisplacement(BaseXmlModel, tag="bc", validate_assignment=True):
    type: Literal["zero displacement"] = attr(default="zero displacement", frozen=True)
    node_set: str = attr()
    x_dof: Literal[0, 1] = element(default=0)
    y_dof: Literal[0, 1] = element(default=0)
    z_dof: Literal[0, 1] = element(default=0)


class BCZeroShellDisplacement(BaseXmlModel, tag="bc", validate_assignment=True):
    type: Literal["zero shell displacement"] = attr(default="zero shell displacement", frozen=True)
    node_set: str = attr()
    sx_dof: Literal[0, 1] = element(default=0)
    sy_dof: Literal[0, 1] = element(default=0)
    sz_dof: Literal[0, 1] = element(default=0)


class BCZeroFluidPressure(BaseXmlModel, tag="bc", validate_assignment=True):
    type: Literal["zero fluid pressure"] = attr(default="zero fluid pressure", frozen=True)
    node_set: str = attr()


class BCPrescribedDisplacement(BaseXmlModel, tag="bc", validate_assignment=True):
    type: Literal["prescribed displacement"] = attr(default="prescribed displacement", frozen=True)
    node_set: str = attr()
    dof: Literal["x", "y", "z"] = element()
    value: Value = element()
    relative: Literal[0, 1] = element(default=0)


class BCPrescribedShellDisplacement(BaseXmlModel, tag="bc", validate_assignment=True):
    type: Literal["prescribed shell displacement"] = attr(default="prescribed shell displacement", frozen=True)
    node_set: str = attr()
    dof: Literal["sx", "sy", "sz"] = element()
    value: Value = element()
    relative: Literal[0, 1] = element(default=0)


class BCPrescribedFluidPressure(BaseXmlModel, tag="bc", validate_assignment=True):
    type: Literal["prescribed fluid pressure"] = attr(default="prescribed fluid pressure", frozen=True)
    node_set: str = attr()
    value: Value = element()
    relative: Literal[0, 1] = element(default=0)


class BCPrescribedDeformation(BaseXmlModel, tag="bc", validate_assignment=True):
    type: Literal["prescribed deformation"] = attr(default="prescribed deformation")
    node_set: str = attr()
    scale: Value = element()
    F: StringFloatVec9 = element(default="1.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,1.0")
    relative: Literal[0, 1] = element(default=0)


class BCRigid(BaseXmlModel, tag="bc", validate_assignment=True):
    type: Literal["rigid"] = attr(default="rigid", frozen=True)
    node_set: str = attr()
    rb: str = element()


class BCRigidDeformation(BaseXmlModel, tag="bc", validate_assignment=True):
    type: Literal["rigid deformation"] = attr(default="rigid deformation", frozen=True)
    node_set: str = attr()
    pos: StringFloatVec3 = element(default="0.0,0.0,0.0")
    rot: Value = element()
    relative: Literal[0, 1] = element(default=0)


class BCNormalDisplacement(BaseXmlModel, tag="bc", validate_assignment=True):
    type: Literal["normal displacement"] = attr(default="normal displacement", frozen=True)
    surface: str = attr()
    scale: Value = element()
    surface_hint: Literal[0, 1] = element(default=0)


class BCZeroConcentration(BaseXmlModel, tag="bc", validate_assignment=True):
    """
    Assign a zero concentration boundary condition for a solute to a node set.
    Hint: c_dof should be a string of the form "c{solute id}" e.g. "c1", "c2", etc.
    """

    type: Literal["zero concentration"] = attr(default="zero concentration", frozen=True)
    node_set: str = attr()
    c_dof: str = element()


class BCPrescribedConcentration(BaseXmlModel, tag="bc", validate_assignment=True):
    """
    Assign a prescribed concentration of a solute to a node set.
    Hint: dof should be a string of the form "c{solute id}" e.g. "c1", "c2", etc.
    """

    type: Literal["prescribed concentration"] = attr(default="prescribed concentration", frozen=True)
    node_set: str = attr()
    dof: str = element()
    value: Value = element()
    relative: Literal[0, 1] = element(default=0)


class MatchingOsmCoefficient(BaseXmlModel, tag="bc", validate_assignment=True):
    type: Literal["matching_osm_coef"] = attr(default="matching_osm_coeff", frozen=True)
    surface: str = attr()
    ambient_pressure: float = element()
    ambient_osmolarity: float = element()
    shell_bottom: Literal[0, 1] = element(default=0)


class ChildDof(BaseXmlModel, tag="child_dof", validate_assignment=True):
    node: int = element()
    dof: Literal["x", "y", "z", "p"] = element()
    value: float = element()


class BCLinearConstraint(BaseXmlModel, tag="bc", validate_assignment=True):
    type: Literal["linear constraint"] = attr(default="linear constraint", frozen=True)
    node: int = element()
    dof: Literal["x", "y", "z", "p"] = element()
    child_dof: list[ChildDof] = element(default=[])


BoundaryConditionType = (
    BCZeroDisplacement
    | BCZeroShellDisplacement
    | BCZeroFluidPressure
    | BCPrescribedDisplacement
    | BCPrescribedShellDisplacement
    | BCPrescribedFluidPressure
    | BCPrescribedDeformation
    | BCRigid
    | BCRigidDeformation
    | BCNormalDisplacement
    | BCZeroConcentration
    | BCPrescribedConcentration
    | BCLinearConstraint
)


class Boundary(BaseXmlModel, tag="Boundary", validate_assignment=True):
    all_bcs: list[BoundaryConditionType] = element(default=[], tag="bc")

    def add_bc(self, new_bc: BoundaryConditionType):
        assert isinstance(new_bc, BoundaryConditionType), "new_bc must be a BoundaryConditionType"
        self.all_bcs.append(new_bc)
