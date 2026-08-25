from typing import Literal

from pydantic_xml import BaseXmlModel, attr, element


class ConstraintSymmetryPlane(BaseXmlModel, validate_assignment=True):
    type: Literal["symmetry plane"] = attr(default="symmetry plane", frozen=True)
    laugon: Literal[0, 1] = element(default=1)
    tol: float = element(default=0.1)
    penalty: float = element(default=1)
    rhs: float = element(default=0)
    minaug: int = element(default=0)
    maxaug: int = element(default=50)


class ConstraintPrestrain(BaseXmlModel, validate_assignment=True):
    type: Literal["prestrain"] = attr(default="prestrain", frozen=True)
    update: Literal[0, 1] = element(default=1)
    tolerance: Literal[0] | float = element(default=0)
    min_iters: int = element(default=0)
    max_iters: int = element(default=-1)


class ConstraintInSituStretch(BaseXmlModel, validate_assignment=True):
    type: Literal["in-situ stretch"] = attr(default="in-situ stretch", frozen=True)
    update: Literal[0, 1] = element(default=1)
    tolerance: Literal[0] | float = element(default=0)
    min_iters: int = element(default=0)
    max_iters: int = element(default=-1)
    max_stretch: Literal[0] | float = element(default=0)
    isochoric: Literal[0, 1] = element(default=1)


ConstraintTypes = ConstraintSymmetryPlane | ConstraintInSituStretch | ConstraintPrestrain


class Constraints(BaseXmlModel, tag="Constraints", validate_assignment=True):
    all_constraints: list[ConstraintTypes] = element(default=[], tag="constraint")

    def add_constraint(self, new_constraint: ConstraintTypes):
        assert isinstance(new_constraint, ConstraintTypes), "new_constraint must be a ConstraintTypes"
        self.all_constraints.append(new_constraint)
