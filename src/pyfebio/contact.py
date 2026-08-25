from typing import Literal

from pydantic_xml import BaseXmlModel, attr, element


class SlidingBase(BaseXmlModel, validate_assignment=True):
    name: str | None = attr(default=None)
    surface_pair: str = attr()
    laugon: Literal["PENALTY", "AUGLAG"] = element(default="PENALTY")
    two_pass: Literal[0, 1] = element(default=0)
    penalty: float = element(default=1.0)
    auto_penalty: Literal[0, 1] = element(default=0)
    update_penalty: Literal[0, 1] = element(default=0)
    tolerance: float = element(default=0.01)
    gaptol: Literal[0] | float = element(default=0)
    minaug: int = element(default=0)
    maxaug: int = element(default=10)
    search_tol: float = element(default=0.01)
    search_radius: Literal[0] | float = element(default=0)
    knmult: float = element(default=1.0)
    seg_up: int = element(default=0)
    node_reloc: Literal[0, 1] = element(default=0)


class SlidingElastic(SlidingBase):
    type: Literal["sliding-elastic"] = attr(default="sliding-elastic")
    symmetric_stiffness: Literal[0, 1] = element(default=1)
    smooth_aug: int = element(default=0)
    tension: Literal[0, 1] = element(default=0)
    fric_coeff: Literal[0] | float = element(default=0)
    flip_primary: Literal[0, 1] = element(default=0)
    flip_secondary: Literal[0, 1] = element(default=0)
    shell_bottom_primary: Literal[0, 1] = element(default=0)
    shell_bottom_secondary: Literal[0, 1] = element(default=0)
    search_radius: Literal[0] | float = element(default=1)
    offset: Literal[0] | float = element(default=0)


class SlidingFacetOnFacet(SlidingBase):
    type: Literal["sliding-facet-on-facet"] = attr(default="sliding-facet-on-facet")
    smooth_aug: int = element(default=0)


class SlidingNodeOnFacet(SlidingBase):
    type: Literal["sliding-node-on-facet"] = attr(default="sliding-node-on-facet")
    fric_coeff: Literal[0] | float = element(default=0)
    fric_penalty: Literal[0] | float = element(default=0)
    ktmult: Literal[0] | float = element(default=0)


SlidingContactType = SlidingElastic | SlidingFacetOnFacet | SlidingNodeOnFacet


class ContactPotential(BaseXmlModel, validate_assignment=True):
    type: Literal["contact potential"] = attr(default="contact potential", frozen=True)
    name: str = attr()
    surface_pair: str = attr()
    kc: float = element(default=1.0e-6)
    p: int = element(default=4)
    check_intersections: Literal[0, 1] = element(default=0)
    R_in: float = element(default=-0.01)
    R_out: float = element(default=0.05)
    R0_min: Literal[0] | float = element(default=0)
    w_tol: Literal[0] | float = element(default=0)
    integration_rule: Literal["default", "higher-order"] = element(default="default")


class SlidingBiphasic(SlidingBase):
    type: Literal["sliding-biphasic"] = attr(default="sliding-biphasic")
    ptol: Literal[0] | float = element(default=0)
    pressure_penalty: float = element(default=1)
    symmetric_stiffness: Literal[0, 1] = element(default=1)
    fric_coeff: Literal[0] | float = element(default=0)
    contact_frac: float = element(default=0.0)
    smooth_aug: int = element(default=0)
    smooth_fls: int = element(default=0)
    search_radius: Literal[0] | float = element(default=1)
    flip_primary: Literal[0, 1] = element(default=0)
    flip_secondary: Literal[0, 1] = element(default=0)
    shell_bottom_primary: Literal[0, 1] = element(default=0)
    shell_bottom_secondary: Literal[0, 1] = element(default=0)


class Sliding2(SlidingBase):
    type: Literal["sliding2"] = attr(default="sliding2")
    ptol: Literal[0] | float = element(default=0)
    pressure_penalty: float = element(default=1)
    symmetric_stiffness: Literal[0, 1] = element(default=1)
    search_radius: Literal[0] | float = element(default=1)
    smooth_aug: int = element(default=0)
    dual_proj: Literal[0, 1] = element(default=1)


SlidingBiphasicContactType = SlidingBiphasic | Sliding2


class TiedBase(BaseXmlModel, validate_assignment=True):
    name: str = attr()
    surface_pair: str = attr()
    laugon: Literal["PENALTY", "AUGLAG"] = element(default="PENALTY")
    tolerance: float = element(default=0.1)
    penalty: float = element(default=1)
    minaug: int = element(default=0)
    maxaug: int = element(default=10)


class TiedElastic(TiedBase):
    type: Literal["tied-elastic"] = attr(default="tied-elastic", frozen=True)
    auto_penalty: Literal[0, 1] = element(default=0)
    update_penalty: Literal[0, 1] = element(default=0)
    two_pass: Literal[0, 1] = element(default=0)
    knmult: float = element(default=1)
    search_tol: float = element(default=0.01)
    search_radius: float = element(default=1)
    gaptol: float = element(default=-1)
    symmetric_stiffness: Literal[0, 1] = element(default=1)
    flip_primary: Literal[0, 1] = element(default=0)
    flip_secondary: Literal[0, 1] = element(default=0)


class TiedFacetOnFacet(TiedBase):
    type: Literal["tied-facet-on-facet"] = attr(default="tied-facet-on-facet", frozen=True)
    tolerance: float = element(default=0.01)
    search_tolerance: float = element(default=0.0001)
    gap_offset: Literal[0, 1] = element(default=0)


class TiedNodeOnFacet(TiedBase):
    type: Literal["tied-node-on-facet"] = attr(default="tied-node-on-facet", frozen=True)
    tolerance: float = element(default=0.01)
    search_tolerance: float = element(default=0.0001)
    offset_shells: Literal[0, 1] = element(default=0)
    max_distance: Literal[0] | float = element(default=0)
    special: Literal[0, 1] = element(default=1)
    node_reloc: Literal[0, 1] = element(default=0)


class TiedBiphasic(TiedBase):
    type: Literal["tied-biphasic"] = attr(default="tied-biphasic", frozen=True)
    gaptol: float = element(default=-1)
    ptol: float = element(default=-1)
    auto_penalty: Literal[0, 1] = element(default=0)
    update_penalty: Literal[0, 1] = element(default=0)
    two_pass: Literal[0, 1] = element(default=0)
    search_tol: float = element(default=0.01)
    search_radius: float = element(default=1)
    knmult: float = element(default=1)
    pressure_penalty: float = element(default=1)
    symmetric_stiffness: Literal[0, 1] = element(default=1)


ContactType = (
    SlidingElastic
    | SlidingFacetOnFacet
    | SlidingNodeOnFacet
    | SlidingBiphasic
    | Sliding2
    | ContactPotential
    | TiedElastic
    | TiedFacetOnFacet
    | TiedNodeOnFacet
    | TiedBiphasic
)


class Contact(BaseXmlModel, tag="Contact", validate_assignment=True):
    all_contact_interfaces: list[ContactType] = element(default=[], tag="contact")

    def add_contact(self, new_contact: ContactType):
        assert isinstance(new_contact, ContactType), "new_contact must be a ContactType"
        if new_contact.name is None:
            new_contact.name = f"{new_contact.type}_{len(self.all_contact_interfaces) + 1}"
        self.all_contact_interfaces.append(new_contact)
