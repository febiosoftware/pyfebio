from typing import Literal

from pydantic import model_validator
from pydantic_xml import BaseXmlModel, attr, element


class SolidDomain(BaseXmlModel, validate_assignment=True):
    name: str = attr(default="SolidPart")
    type: Literal["elastic-solid", "three-field-solid", "rigid-solid", "udg-hex", "sri-solid", "remodelling-solid", "ut4-solid"] | None = (
        attr(default=None)
    )
    elem_type: (
        Literal[
            "HEX8G6",
            "HEX8G8",
            "HEX20G8",
            "TET4G1",
            "TET4G4",
            "TET10G4",
            "TET10G8",
            "TET10GL11",
            "TET15G8",
            "TET15G11",
            "TET15G15",
            "PENTA15G8",
        ]
        | None
    ) = attr(default=None)
    mat: str = attr(default="material")
    alpha: float | None = element(default=None)
    iso_stab: Literal[0, 1] | None = element(default=None)


class ShellDomain(BaseXmlModel, validate_assignment=True):
    name: str = attr(default="ShellPart")
    type: (
        Literal[
            "elastic-shell",
            "three-field-shell",
            "rigid-shell",
            "elastic-shell-old",
            "elastic-shell-eas",
            "elastic-shell-ans",
        ]
        | None
    ) = attr(default=None)
    mat: str = attr(default="material")
    shell_thickness: float = element(default=0.01)


class BeamDomain(BaseXmlModel, validate_assignment=True):
    name: str = attr(default="BeamPart")
    type: Literal["linear-truss", "elastic-truss", "linear-beam"] = attr()
    mat: str = attr(default="material")
    cross_sectional_area: float | None = element(default=None)
    v: float | None = element(default=None)

    @model_validator(mode="after")
    def validate_material(self):
        if self.type == "elastic-truss":
            if self.cross_sectional_area is None:
                raise ValueError("Cross-sectional area must be specified for elastic-truss domain")
            if self.v is None:
                raise ValueError("Poisson ratio (v) must be specified for elastic-truss domain")
        else:
            if self.cross_sectional_area is not None:
                raise ValueError("Cross-sectional area must not be specified when type is not 'elastic-truss'")
            if self.v is not None:
                raise ValueError("Poisson ratio (v) must not be specified when type is not 'elastic-truss'")
        return self


class MeshDomains(BaseXmlModel, validate_assignment=True):
    solid_domains: list[SolidDomain] = element(default=[], tag="SolidDomain")
    shell_domains: list[ShellDomain] = element(default=[], tag="ShellDomain")
    beam_domains: list[BeamDomain] = element(default=[], tag="BeamDomain")

    def add_solid_domain(self, new_solid_domain: SolidDomain):
        self.solid_domains.append(new_solid_domain)

    def add_shell_domain(self, new_shell_domain: ShellDomain):
        self.shell_domains.append(new_shell_domain)

    def add_beam_domain(self, new_beam_domain: BeamDomain):
        self.beam_domains.append(new_beam_domain)
