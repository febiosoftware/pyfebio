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
    "acceleration",
    "Almansi strain",
    "beam curvature",
    "beam reference stress",
    "beam reference stress couple",
    "beam strain",
    "beam stress",
    "beam stress couple",
    "body force",
    "concentration gap",
    "contact area",
    "contact force",
    "contact gap",
    "contact penalty",
    "contact pressure",
    "contact status",
    "contact stick",
    "contact traction",
    "continuous damage",
    "continuous damage beta",
    "continuous damage D1",
    "continuous damage D2",
    "continuous damage D2beta",
    "continuous damage D3",
    "continuous damage Ds",
    "continuous damage gamma",
    "continuous damage P",
    "continuous damage Psi0",
    "current density",
    "current element angular momentum",
    "current element center of mass",
    "current element kinetic energy",
    "current element linear momentum",
    "current element strain energy",
    "damage",
    "deformation gradient",
    "density",
    "Deshpande-Fleck stress",
    "deviatoric elasticity",
    "deviatoric fiber stretch",
    "deviatoric strain energy density",
    "deviatoric strong bond SED",
    "deviatoric weak bond SED",
    "dilatation gradient",
    "discrte element direction",
    "discrete element elongation",
    "discrete element force",
    "discrete element length",
    "discrete element percent elongation",
    "discrete element signed force",
    "discrete element strain energy",
    "discrete element stretch",
    "displacement",
    "Drucker shear stress",
    "Drucker-Prager stress",
    "edge contact gap",
    "effective elasticity",
    "effective fluid pressure",
    "effective friction coefficient",
    "effective shell fluid pressure",
    "effective shell solute concentration",
    "effective solute concentration",
    "elastic fluid pressure",
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
    "facet area",
    "fatigue bone fraction",
    "fiber stretch",
    "fiber vector",
    "field",
    "fixed charge density",
    "fluid acceleration",
    "fluid body force",
    "fluid bulk modulus",
    "fluid density",
    "fluid density rate",
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
    "fluid pressure tangent strain",
    "fluid rate of deformation",
    "fluid relative Reynolds number",
    "fluid shear stress error",
    "fluid shear viscosity",
    "fluid specific entropy",
    "fluid specific free energy",
    "fluid specific free enthalpy",
    "fluid specific gauge enthalpy",
    "fluid specific internal energy",
    "fluid specific strain energy",
    "fluid strain energy density",
    "fluid stress",
    "fluid stress power density",
    "fluid surface energy flux",
    "fluid surface force",
    "fluid surface pressure",
    "fluid surface traction power",
    "fluid velocity",
    "fluid volume ratio",
    "fluid volume ratio gradient",
    "fluid vorticity",
    "growth infinitesimal strain",
    "growth Lagrange strain",
    "growth left Hencky",
    "growth left stretch",
    "growth relative volume",
    "growth right Hencky",
    "growth right stretch",
    "ideal gas pressure",
    "incremental displacement",
    "infinitesimal strain",
    "in-situ target stretch",
    "intact bond fraction",
    "kinetic energy density",
    "Lagrange strain",
    "left Cauchy-Green",
    "left Hencky",
    "left stretch",
    "local fluid load support",
    "material axes",
    "mesh_data",
    "micro energy",
    "mixture deviatoric strain energy density",
    "mixture specific strain energy",
    "mixture strain energy density",
    "mixture stress",
    "nodal acceleration",
    "nodal contact gap",
    "nodal contact pressure",
    "nodal contact traction",
    "nodal fluid flux",
    "nodal fluid velocity",
    "nodal shell director",
    "nodal strain",
    "nodal stress",
    "nodal surface traction",
    "nodal vector gap",
    "nodal veleocity",
    "octahedral plastic strain",
    "osmolarity",
    "osmotic coefficient",
    "parameter",
    "partition coefficient",
    "permeability",
    "pid controller",
    "PK1 norm",
    "PK1 stress",
    "PK2 stress",
    "plastic yield stress",
    "plasticity heat supply density",
    "porosity",
    "pressure gap",
    "prestrain compatibility",
    "prestrain correction",
    "prestrain stretch",
    "prestrain stretch error",
    "rate of deformation",
    "reaction forces",
    "receptor-ligand",
    "referential fixed charge density",
    "referential solid volume fraction",
    "relative fluid velocity",
    "relative volume",
    "right Cauchy-Green",
    "right Hencky",
    "right stretch",
    "rigid acceleration",
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
    "rotation",
    "RVE generations",
    "RVE recruitment",
    "RVE strain",
    "s norm",
    "sbm areal concentration",
    "sbm concentration",
    "sbm referential apparent density",
    "scalar surface load",
    "shell bottom nodal strain",
    "shell bottom nodal stress",
    "shell bottom strain",
    "shell bottom stress",
    "shell director",
    "shell displacement",
    "shell relative volume",
    "shell strain",
    "shell thickness",
    "shell top nodal strain",
    "shell top nodal stress",
    "shell top strain",
    "shell top stress",
    "solid stress",
    "solid volume fraction",
    "solute concentration",
    "solute flux",
    "solute relative Peclet number",
    "solute volumetric flux",
    "specific strain energy",
    "SPR infinitesimal strain",
    "SPR Lagrange strain",
    "SPR prestrain correction",
    "SPR principal stress",
    "SPR relative volume",
    "SPR stress",
    "SPR-P1 stress",
    "strain energy density",
    "stress",
    "stress error",
    "strong bond SED",
    "surface area",
    "surface reaction force",
    "surface reaction moment",
    "surface traction",
    "total angular momentum",
    "total energy",
    "total linear momentum",
    "truss stretch",
    "uncoupled pressure",
    "ut4 nodal stress",
    "vector gap",
    "velocity",
    "volume fraction",
    "weak bond SED",
    "yielded bond fraction",
]


class Var(BaseXmlModel, validate_assignment=True):
    type: PlotDataVariables = attr()


class OutputPlotfile(BaseXmlModel, tag="plotfile", validate_assignment=True):
    type: Literal["febio", "vtk"] = attr(default="febio")
    file: str | None = attr(default=None)
    all_vars: list[Var] = element(default=[], tag="var")

    def add_var(self, new_var: Var):
        assert isinstance(new_var, Var), "new_var must be a Var"
        self.all_vars.append(new_var)


class Output(BaseXmlModel, validate_assignment=True):
    logfile: list[OutputLogfile] = element(default=[])
    plotfile: list[OutputPlotfile] = element(default=[])

    def add_plotfile(self, new_plotfile: OutputPlotfile):
        assert isinstance(new_plotfile, OutputPlotfile), "new_plotfile must be an OutputPlotfile"
        self.plotfile.append(new_plotfile)

    def add_logfile(self, new_logfile: OutputLogfile):
        assert isinstance(new_logfile, OutputLogfile), "new_logfile must be an OutputLogfile"
        self.logfile.append(new_logfile)
