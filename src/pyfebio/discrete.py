from typing import Literal

from pydantic import Field, NegativeFloat, PositiveFloat, model_validator
from pydantic_xml import BaseXmlModel, attr, element

from ._types import StringFloatVec2


class ScalePoints(BaseXmlModel, tag="points", validate_assignment=True):
    pt: list[StringFloatVec2] = element(default=Field(default_factory=list))


class Scale(BaseXmlModel, validate_assignment=True):
    """
    All parameters are set to None initially, to handle all
    customization. We add a validitor to ensure consistency.
    """

    type: Literal["point", "const"] | None = attr(default=None)
    value: float | None = element(default=None)
    interpolate: Literal["linear", "smooth"] | None = element(default=None)
    points: ScalePoints | None = element(default=None)

    @model_validator(mode="after")
    def validate_options(self):
        if self.type is None:
            raise ValueError("type must be specified")
        if self.type == "point":
            if self.value is not None:
                raise ValueError("value must be None when type is 'point'")
            if self.interpolate is None:
                raise ValueError("interpolate must be specified when type is 'point'")
            if self.points is None:
                raise ValueError("points must be specified when type is 'point'")
        else:
            if self.value is None:
                raise ValueError("text must be a float when type is not 'point'")
            if self.interpolate is not None:
                raise ValueError("interpolate must be None when type is not 'point'")
            if self.points is not None:
                raise ValueError("points must be None when type is not 'point'")
        return self


class Spring(BaseXmlModel, tag="discrete_material", validate_assignment=True):
    id: int = attr()
    name: str = attr()
    type: str = attr(default="linear spring", frozen=True)
    E: float = element(default=1.0)


class NonlinearSpringForce(BaseXmlModel, tag="force", validate_assignment=True):
    type: Literal["math"] = attr(default="math", frozen=True)
    math: str = element()


class NonlinearSpring(BaseXmlModel, tag="discrete_material", validate_assignment=True):
    id: int = attr()
    name: str = attr()
    type: Literal["nonlinear spring"] = attr(default="nonlinear spring", frozen=True)
    scale: float = element(default=1.0)
    measure: Literal["elongation", "strain", "stretch"] = element(default="elongation")
    force: NonlinearSpringForce = element()


class TensionOnlyLinearSpring(BaseXmlModel, tag="discrete_material", validate_assignment=True):
    id: int = attr()
    name: str = attr()
    type: Literal["tension-only linear spring"] = attr(default="tension-only linear spring", frozen=True)
    E: float = element(default=1.0)


class ExperimentalSpring(BaseXmlModel, tag="discrete_material", validate_assignment=True):
    id: int = attr()
    name: str = attr()
    type: Literal["experimental spring"] = attr(default="experimental spring", frozen=True)
    E: float = element(default=1.0)
    sM: PositiveFloat | NegativeFloat = element(default=1.0)
    sm: PositiveFloat | NegativeFloat = element(default=2.0)


class HillElement(BaseXmlModel, tag="discrete_material", validate_assignment=True):
    id: int = attr()
    name: str = attr()
    type: Literal["Hill"] = attr(default="Hill", frozen=True)
    Vmax: float = element(default=1.0)
    ac: float = element(default=0.0)
    Fmax: float = element(default=1.0)
    Ksh: float = element(default=1.0)
    Lmax: float = element(default=1.0)
    L0: Literal[0] | float = element(default=0)
    Sv: Scale | None = element(default=None)
    Ftl: Scale | None = element(default=None)
    Fvl: Scale | None = element(default=None)


DiscreteMaterialType = NonlinearSpring | Spring | TensionOnlyLinearSpring | HillElement | ExperimentalSpring


class DiscreteEntry(BaseXmlModel, tag="discrete", validate_assignment=True):
    dmat: int = attr()
    discrete_set: str = attr()


class Discrete(BaseXmlModel, validate_assignment=True):
    discrete_materials: tuple[DiscreteMaterialType, ...] = element(default=())
    discrete_elements: tuple[DiscreteEntry, ...] = element(default=())

    def add_discrete_material(self, new_material: DiscreteMaterialType):
        self.discrete_materials += (new_material,)

    def add_discrete_element(self, new_element: DiscreteEntry):
        self.discrete_elements += (new_element,)
