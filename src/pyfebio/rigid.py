from typing import Literal

from pydantic_xml import BaseXmlModel, attr, element

from ._types import (
    StringFloatVec3,
)


class Value(BaseXmlModel, validate_assignment=True):
    lc: int | None = attr(default=None)
    text: float = 1.0


class RigidFixed(BaseXmlModel, tag="rigid_bc", validate_assignment=True):
    """ """

    type: Literal["rigid_fixed"] = attr(default="rigid_fixed", frozen=True)
    rb: str = element()
    Rx_dof: Literal[0, 1] = element(default=0)
    Ry_dof: Literal[0, 1] = element(default=0)
    Rz_dof: Literal[0, 1] = element(default=0)
    Ru_dof: Literal[0, 1] = element(default=0)
    Rv_dof: Literal[0, 1] = element(default=0)
    Rw_dof: Literal[0, 1] = element(default=0)


class RigidPrescribed(BaseXmlModel, tag="rigid_bc", validate_assignment=True):
    type: Literal["rigid_displacement", "rigid_rotation"] = attr(default="rigid_displacement", frozen=True)
    rb: str = element()
    dof: Literal["x", "y", "z", "Ru", "Rv", "Rw"] = element()
    relative: Literal[0, 1] = element(default=0)
    value: Value = element()


class RigidBodyRotationVector(BaseXmlModel, tag="rigid_bc", validate_assignment=True):
    class X(BaseXmlModel, tag="vx", validate_assignment=True):
        lc: int = attr()
        text: float = 0.0

    class Y(BaseXmlModel, tag="vy", validate_assignment=True):
        lc: int = attr()
        text: float = 0.0

    class Z(BaseXmlModel, tag="vz", validate_assignment=True):
        lc: int = attr()
        text: float = 0.0

    type: Literal["rigid_rotation_vector"] = attr(default="rigid_rotation_vector", frozen=True)
    rb: str = element()
    vx: X = element()
    vy: Y = element()
    vz: Z = element()


class RigidBodyEulerAngle(BaseXmlModel, tag="rigid_bc", validate_assignment=True):
    class X(BaseXmlModel, tag="Ex", validate_assignment=True):
        lc: int = attr()
        text: float = 0.0

    class Y(BaseXmlModel, tag="Ey", validate_assignment=True):
        lc: int = attr()
        text: float = 0.0

    class Z(BaseXmlModel, tag="Ez", validate_assignment=True):
        lc: int = attr()
        text: float = 0.0

    type: Literal["rigid_euler_angles"] = attr(default="rigid_euler_angles", frozen=True)
    rb: str = element()
    Ex: X = element()
    Ey: Y = element()
    Ez: Z = element()


class RigidForceLoad(BaseXmlModel, tag="rigid_load", validate_assignment=True):
    type: Literal["rigid_force"] = attr(default="rigid_force", frozen=True)
    rb: str = element()
    dof: Literal["Rx", "Ry", "Rz"] = element()
    relative: Literal[0, 1] = element(default=0)
    load_type: Literal[0, 1, 2] = element(default=0)
    value: Value = element()


class RigidFollowerForceLoad(BaseXmlModel, tag="rigid_load", validate_assignment=True):
    type: Literal["rigid_follower_force"] = attr(default="rigid_follower_force", frozen=True)
    rb: str = element()
    insertion: StringFloatVec3 = element()
    relative: Literal[0, 1] = element(default=0)
    force: StringFloatVec3 = element()


class RigidMomentLoad(BaseXmlModel, tag="rigid_load", validate_assignment=True):
    type: Literal["rigid_moment"] = attr(default="rigid_moment", frozen=True)
    rb: str = element()
    dof: Literal["Ru", "Rv", "Rw"] = element()
    relative: Literal[0, 1] = element(default=0)
    value: Value = element()


class RigidFollowerMomentLoad(BaseXmlModel, tag="rigid_load", validate_assignment=True):
    type: Literal["rigid_follower_moment"] = attr(default="rigid_follower_moment", frozen=True)
    rb: str = element()
    moment: StringFloatVec3 = element()


class RigidCableLoad(BaseXmlModel, tag="rigid_load", validate_assignment=True):
    class CablePoint(BaseXmlModel, tag="rigid_cable_point", validate_assignment=True):
        rigid_body_id: str = element()
        position: StringFloatVec3 = element()

    type: Literal["rigid_cable"] = attr(default="rigid_cable", frozen=True)
    force_direction: StringFloatVec3 = element()
    relative: Literal[0, 1] = element(default=1)
    force: Value = element()
    rigid_cable_point: list[CablePoint] = element(default=[])


class RigidConnector(
    BaseXmlModel,
    tag="rigid_connector",
    validate_assignment=True,
):
    """ """

    name: str = attr()
    body_a: str = element()
    body_b: str = element()
    tolerance: float = element(default=0.1)
    minaug: int = element(default=0)
    maxaug: int = element(default=10)
    gaptol: Literal[0] | float = element(default=0)
    angtol: Literal[0] | float = element(default=0)
    force_penalty: float = element(default=1)
    moment_penalty: float = element(default=1)
    auto_penalty: Literal[0, 1] = element(default=1)


class Free(BaseXmlModel, validate_assignment=True):
    text: Literal[0] = 0


class RigidSphericalJoint(RigidConnector):
    type: Literal["rigid spherical joint"] = attr(default="rigid spherical joint", frozen=True)
    joint_origin: StringFloatVec3 = element(default="0.0,0.0,0.0")
    prescribed_rotation: Literal[0, 1] = element(default=0)
    rotation_x: Value | Free = element(default=Free())
    rotation_y: Value | Free = element(default=Free())
    rotation_z: Value | Free = element(default=Free())
    moment_x: Value | Free = element(default=Free())
    moment_y: Value | Free = element(default=Free())
    moment_z: Value | Free = element(default=Free())


class RigidRevoluteJoint(RigidConnector):
    class Free(BaseXmlModel):
        text: Literal[0] = 0

    type: Literal["rigid revolute joint"] = attr(default="rigid revolute joint", frozen=True)
    laugon: Literal[0, 1] = element(default=0)
    joint_origin: StringFloatVec3 = element(default="0.0,0.0,0.0")
    prescribed_rotation: Literal[0, 1] = element(default=0)
    rotation_axis: StringFloatVec3 = element(default="1.0,0.0,0.0")
    transverse_axis: StringFloatVec3 = element(default="0.0,1.0,0.0")
    moment: Value | Free = element(default=Free())
    rotation: Value | Free = element(default=Free())


class RigidPrismaticJoint(RigidConnector):
    type: Literal["rigid prismatic joint"] = attr(default="rigid prismatic joint", frozen=True)
    joint_origin: StringFloatVec3 = element(default="0.0,0.0,0.0")
    translation_axis: StringFloatVec3 = element(default="1.0,0.0,0.0")
    transverse_axis: StringFloatVec3 = element(default="0.0,1.0,0.0")
    prescribed_translation: Literal[0, 1] = element(default=0)
    translation: Value | Free = element(default=Free())
    force: Value | Free = element(default=Free())


class RigidCylindricalJoint(RigidConnector):
    type: Literal["rigid cylindrical joint"] = attr(default="rigid cylindrical joint", frozen=True)
    laugon: Literal["PENALTY", "AUGLAG", "LAGMULT"] = element(default="PENALTY")
    joint_origin: StringFloatVec3 = element(default="0.0,0.0,0.0")
    joint_axis: StringFloatVec3 = element(default="0.0,0.0,0.0")
    transverse_axis: StringFloatVec3 = element(default="0.0,0.0,0.0")
    prescribed_rotation: Literal[0, 1] = element(default=0)
    prescribed_translation: Literal[0, 1] = element(default=0)
    translation: Value | Free = element(default=Free())
    force: Value | Free = element(default=Free())
    rotation: Value | Free = element(default=Free())
    moment: Value | Free = element(default=Free())


class RigidPlanarJoint(RigidConnector):
    type: Literal["rigid planar joint"] = attr(default="rigid planar joint", frozen=True)
    joint_origin: StringFloatVec3 = element(default="0.0,0.0,0.0")
    rotation_axis: StringFloatVec3 = element(default="0.0,0.0,0.0")
    translation_axis_1: StringFloatVec3 = element(default="0.0,0.0,0.0")
    prescribed_rotation: Literal[0, 1] = element(default=0)
    prescribed_translation_1: Literal[0, 1] = element(default=0)
    prescribed_translation_2: Literal[0, 1] = element(default=0)
    rotation: Value | Free = element(default=Free())
    translation_1: Value | Free = element(default=Free())
    translation_2: Value | Free = element(default=Free())


class RigidLock(RigidConnector):
    type: Literal["rigid lock"] = attr(default="rigid lock", frozen=True)
    joint_origin: StringFloatVec3 = element(default="0.0,0.0,0.0")
    first_axis: StringFloatVec3 = element(default="1.0,0.0,0.0")
    second_axis: StringFloatVec3 = element(default="0.0,1.0,0.0")


class RigidSpring(BaseXmlModel, tag="rigid_connector", validate_assignment=True):
    type: Literal["rigid spring"] = attr(default="rigid spring", frozen=True)
    name: str = attr()
    body_a: str = element()
    body_b: str = element()
    k: float = element(default=1)
    insertion_a: StringFloatVec3 = element(default="0.0,0.0,0.0")
    insertion_b: StringFloatVec3 = element(default="1.0,0.0,0.0")
    free_length: Literal[0] | float = element(default=0)


class RigidDamper(BaseXmlModel, tag="rigid_connector", validate_assignment=True):
    type: Literal["rigid damper"] = attr(default="rigid damper", frozen=True)
    name: str = attr()
    body_a: str = element()
    body_b: str = element()
    c: float = element(default=1e-7)
    insertion_a: StringFloatVec3 = element(default="0.0,0.0,0.0")
    insertion_b: StringFloatVec3 = element(default="1.0,0.0,0.0")


class RigidAngularDamper(BaseXmlModel, tag="rigid_connector", validate_assignment=True):
    type: Literal["rigid angular damper"] = attr(default="rigid angular damper", frozen=True)
    name: str = attr()
    body_a: str = element()
    body_b: str = element()
    c: float = element(default=1e-7)


class RigidContractileForce(BaseXmlModel, tag="rigid_connector", validate_assignment=True):
    type: Literal["rigid contractile force"] = attr(default="rigid contractile force", frozen=True)
    name: str = attr()
    body_a: str = element()
    body_b: str = element()
    insertion_a: StringFloatVec3 = element(default="0.0,0.0,0.0")
    insertion_b: StringFloatVec3 = element(default="1.0,0.0,0.0")
    f0: Value = element()


RigidBCType = RigidFixed | RigidPrescribed | RigidBodyRotationVector | RigidBodyEulerAngle

RigidLoadType = RigidForceLoad | RigidFollowerForceLoad | RigidMomentLoad | RigidFollowerMomentLoad | RigidCableLoad

RigidConnectorType = (
    RigidSphericalJoint
    | RigidRevoluteJoint
    | RigidCylindricalJoint
    | RigidPrismaticJoint
    | RigidPlanarJoint
    | RigidLock
    | RigidSpring
    | RigidDamper
    | RigidAngularDamper
    | RigidContractileForce
)


class Rigid(BaseXmlModel, tag="Rigid", validate_assignment=True):
    all_rigid_bcs: list[RigidBCType] = element(default=[], tag="rigid_bc")
    all_rigid_loads: list[RigidLoadType] = element(default=[], tag="rigid_load")
    all_rigid_connectors: list[RigidConnectorType] = element(default=[], tag="rigid_connector")

    def add_rigid_bc(
        self,
        new_rigid_bc: RigidBCType,
    ):
        self.all_rigid_bcs.append(new_rigid_bc)

    def add_rigid_load(
        self,
        new_rigid_load: RigidLoadType,
    ):
        self.all_rigid_loads.append(new_rigid_load)

    def add_rigid_connector(self, new_rigid_connector: RigidConnectorType):
        self.all_rigid_connectors.append(new_rigid_connector)
