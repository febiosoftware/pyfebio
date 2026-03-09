from pydantic_xml import BaseXmlModel, attr, element


class Constants(BaseXmlModel, tag="Constants", validate_assignment=True, extra="forbid"):
    T: float = element(default=298)
    P: float = element(default=0)
    R: float = element(default=8.314e-6)
    Fc: float = element(default=96485e-9)


class Solute(BaseXmlModel, tag="solute", validate_assignment=True, extra="forbid"):
    id: int = attr()
    name: str | None = attr(default=None)
    charge_number: int = element(default=1)
    molar_mass: float = element(default=1.0)
    density: float = element(default=1.0)


class Solutes(BaseXmlModel, tag="Solutes", validate_assignment=True, extra="forbid"):
    solute: list[Solute] = element(default=[])


class SolidBoundMolecule(BaseXmlModel, tag="solid_bound", validate_assignment=True, extra="forbid"):
    id: int = attr()
    name: str | None = attr(default=None)
    charge_number: int = element(default=1)
    molar_mass: float = element(default=1.0)
    density: float = element(default=1.0)


class SolidBoundMolecules(BaseXmlModel, tag="SolidBoundMolecules", validate_assignment=True, extra="forbid"):
    solid_bound: list[SolidBoundMolecule] = element(default=[])


class Globals(BaseXmlModel, validate_assignment=True):
    constants: Constants = element(default=Constants(), tag="Constants")
    solutes: Solutes | None = element(default=None, tag="Solutes")
    solid_bound_molecules: SolidBoundMolecules | None = element(default=None, tag="SolidBoundMolecules")
