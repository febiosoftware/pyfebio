from enum import Enum
from typing import Literal

from pydantic_xml import BaseXmlModel, attr, element


class NodeDataEnum(str, Enum):
    x_coordinate = "x"
    y_coordinate = "y"
    z_coordinate = "z"
    x_displacement = "ux"
    y_displacement = "uy"
    z_displacement = "uz"
    x_velocity = "vx"
    y_velocity = "vy"
    z_velocity = "vz"
    x_acceleration = "ax"
    y_acceleration = "ay"
    z_acceleration = "az"
    x_reaction_force = "Rx"
    y_reaction_force = "Ry"
    z_reaction_force = "Rz"
    fluid_pressure = "p"


class ElementDataEnum(str, Enum):
    x_coordinate = "x"
    y_coordinate = "y"
    z_coordinate = "z"
    x_stress = "sx"
    y_stress = "sy"
    z_stress = "sz"
    xy_stress = "sxy"
    yz_stress = "syz"
    xz_stress = "sxz"
    p1_stress = "s1"
    p2_stress = "s2"
    p3_stress = "s3"
    x_strain = "Ex"
    y_strain = "Ey"
    z_strain = "Ez"
    xy_strain = "Exy"
    yz_strain = "Eyz"
    xz_strain = "Exz"
    p1_strain = "E1"
    p2_strain = "E2"
    p3_strain = "E3"
    strain_energy_density = "sed"
    devaiatoric_strain_energy_density = "devsed"
    fluid_pressure = "p"
    x_flux = "wx"
    y_flux = "wy"
    z_flux = "wz"


class RigidBodyDataEnum(str, Enum):
    x_coordinate = "x"
    y_coordinate = "y"
    z_coordinate = "z"
    x_velocity = "vx"
    y_velocity = "vy"
    z_velocity = "vz"
    x_acceleration = "ax"
    y_acceleration = "ay"
    z_acceleration = "az"
    x_rotation = "thx"
    y_rotation = "thy"
    z_rotation = "thz"
    x_angular_velocity = "omx"
    y_angular_velocity = "omy"
    z_angular_velocity = "omz"
    x_angular_acceleration = "alx"
    y_angular_acceleration = "aly"
    z_angular_acceleration = "alz"
    x_force = "Fx"
    y_force = "Fy"
    z_force = "Fz"
    x_moment = "Mx"
    y_moment = "My"
    z_moment = "Mz"
    x_euler = "XEuler"
    y_euler = "YEuler"
    z_euler = "ZEuler"


class RigidConnectorDataEnum(str, Enum):
    x_force = "RCFx"
    y_force = "RCFy"
    z_force = "RCFz"
    x_moment = "RCMx"
    y_moment = "RCMy"
    z_moment = "RCMz"
    x_translation = "RCx"
    y_translation = "RCy"
    z_translation = "RCz"
    x_rotation = "RCthx"
    y_rotation = "RCthy"
    z_rotation = "RCthz"


def assemble_data_string(
    requests: list[RigidBodyDataEnum] | list[NodeDataEnum] | list[ElementDataEnum] | list[RigidConnectorDataEnum],
) -> str:
    return ";".join(requests)


class DataEntry(BaseXmlModel, validate_assignment=True):
    data: str = attr(default="")
    file: str | None = attr(default=None)
    delim: str = attr(default=" ")
    format: str | None = attr(default=None)
    text: str | None = None


class OutputLogfile(BaseXmlModel, tag="logfile", validate_assignment=True):
    file: str | None = attr(default=None)
    node_data: list[DataEntry] = element(default=[], tag="node_data")
    element_data: list[DataEntry] = element(default=[], tag="element_data")
    face_data: list[DataEntry] = element(default=[], tag="face_data")
    rigid_body_data: list[DataEntry] = element(default=[], tag="rigid_body_data")
    rigid_connector_data: list[DataEntry] = element(default=[], tag="rigid_connector_data")

    def add_node_data(self, new_output: DataEntry):
        self.node_data.append(new_output)

    def add_element_data(self, new_output: DataEntry):
        self.element_data.append(new_output)

    def add_face_data(self, new_output: DataEntry):
        self.face_data.append(new_output)

    def add_rigid_body_data(self, new_output: DataEntry):
        self.rigid_body_data.append(new_output)

    def add_rigid_connector_data(self, new_output: DataEntry):
        self.rigid_connector_data.append(new_output)


PlotDataVariables = Literal[
    "Acceleration",
    "contact area",
    "contact force",
    "contact gap",
    "contact penalty",
    "contact pressure",
    "contact traction",
    "current density",
    "current element angular momentum",
    "current element center of mass",
    "current element kinetic energy",
    "current element linear momentum",
    "current element strain energy",
    "deformation gradient",
    "damage",
    "density",
    "deviatoric strain energy density",
    "displacement",
    "effective elasticity",
    "effective fluid pressure",
    "effective friction coefficient",
    "effective solute concentration",
    "elasticity",
    "electric potential",
    "element angular momentum",
    "element center of mass",
    "element kinetic energy",
    "element linear momentum",
    "element strain energy",
    "element stress power",
    "enclosed volume",
    "enclosed volume change",
    "Euler angle",
    "fiber stretch",
    "fiber vector",
    "field",
    "fixed charge density",
    "fluid acceleration",
    "fluid density",
    "fluid dilatation",
    "fluid element angular momentum",
    "fluid element center of mass",
    "fluid element kinetic energy",
    "fluid element linear momentum",
    "fluid element strain energy",
    "fluid energy density",
    "fluid flow rate",
    "fluid flux",
    "fluid force",
    "fluid force2",
    "fluid heat supply density",
    "fluid kinetic energy density",
    "fluid load support",
    "fluid mass flow rate",
    "fluid pressure",
    "fluid rate of deformation",
    "fluid shear viscosity",
    "fluid strain energy density",
    "fluid stress",
    "fluid stress power density",
    "fluid surface energy flux",
    "fluid surface force",
    "fluid surface pressure",
    "fluid surface traction power",
    "fluid velocity",
    "fluid volume ratio",
    "fluid vorticity",
    "heat flux",
    "kinetic energy density",
    "Lagrange strain",
    "left Hencky",
    "left stretch",
    "local fluid load support",
    "nested damage",
    "nodal acceleration",
    "nodal contact gap",
    "nodal contact pressure",
    "nodal contact traction",
    "nodal fluid flux",
    "nodal fluid velocity",
    "nodal stress",
    "nodal surface traction",
    "nodal vector gap",
    "nodal velocity",
    "osmolarity",
    "parameter",
    "pressure gap",
    "reaction forces",
    "receptor-ligand concentration",
    "referential fixed charge density",
    "referential solid volume fraction",
    "relative fluid velocity",
    "relative volume",
    "right Hencky",
    "right stretch",
    "rigid acceleration",
    "rigid angular acceleration",
    "rigid angular momentum",
    "rigid angular position",
    "rigid angular velocity",
    "rigid force",
    "rigid kinetic energy",
    "rigid linear momentum",
    "rigid position",
    "rigid rotation vector",
    "rigid torque",
    "rigid velocity",
    "RVE generations",
    "RVE reforming bonds",
    "RVE strain",
    "sbm concentration",
    "sbm referential apparent density",
    "shell director",
    "shell relative volume",
    "shell strain",
    "shell thickness",
    "solute concentration",
    "solute flux",
    "specific strain energy",
    "SPR principal stress",
    "SPR stress",
    "SPR-P1 stress",
    "strain energy density",
    "stress",
    "stress error",
    "surface traction",
    "uncoupled pressure",
    "ut4 nodal stress",
    "vector gap",
    "velocity",
    "volume fraction",
    "in-situ target stretch",
    "prestrain stretch",
    "prestrain correction",
    "SPR prestrain correction",
]


class Var(BaseXmlModel, validate_assignment=True):
    type: PlotDataVariables = attr()


class OutputPlotfile(BaseXmlModel, tag="plotfile", validate_assignment=True):
    type: Literal["febio", "vtk"] = attr(default="febio")
    file: str | None = attr(default=None)
    all_vars: list[Var] = element(default=[], tag="var")

    def add_var(self, new_var: Var):
        self.all_vars.append(new_var)


class Output(BaseXmlModel, validate_assignment=True):
    logfile: list[OutputLogfile] = element(default=[])
    plotfile: list[OutputPlotfile] = element(default=[])

    def add_plotfile(self, new_plotfile: OutputPlotfile):
        self.plotfile.append(new_plotfile)

    def add_logfile(self, new_logfile: OutputLogfile):
        self.logfile.append(new_logfile)
