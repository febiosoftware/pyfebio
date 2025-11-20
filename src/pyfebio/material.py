from typing import Annotated, Literal, TypeAlias

from pydantic import AfterValidator, Field, PositiveInt
from pydantic.types import NonNegativeFloat
from pydantic_xml import BaseXmlModel, attr, element

from ._types import StringFloatVec3, StringFloatVec9


class MaterialAxisVector(BaseXmlModel, validate_assignment=True, extra="forbid"):
    type: Literal["vector"] = attr(default="vector", frozen=True)
    a: StringFloatVec3 = element(default="1.0,0.0,0.0")
    d: StringFloatVec3 = element(default="0.0,1.0,0.0")


class FiberVector(BaseXmlModel, validate_assignment=True, extra="forbid"):
    type: Literal["vector"] = attr(default="vector", frozen=True)
    text: StringFloatVec3 = "1.0,0.0,0.0"


class MaterialParameter(BaseXmlModel, validate_assignment=True, extra="forbid"):
    type: Literal["map", "math"] | None = attr(default=None)
    text: float | int | str = Field(union_mode="left_to_right")


class DynamicMaterialParameter(BaseXmlModel, validate_assignment=True, extra="forbid"):
    type: Literal["map", "math"] | None = attr(default=None)
    lc: int = attr(default=1, ge=1)
    text: float | int | str = Field(union_mode="left_to_right")


# Material Paramter Validators
def mat_is_positive_float(parameter: MaterialParameter) -> MaterialParameter:
    if parameter.type == "map" or parameter.type == "math":
        if not isinstance(parameter.text, str):
            raise ValueError(
                f"MaterialParameter {parameter.type=}, which requires parameter.text to be of type(str), but {parameter.text=}."
            )
        return parameter
    elif isinstance(parameter.text, float | int):
        if parameter.text <= 0.0:
            raise ValueError(f"{parameter.text=} must be greater than 0.0")
        return parameter
    else:
        raise ValueError(f"{parameter.text=} of type(str) but {parameter.type=} when it must be 'map' or 'math'")


def mat_is_non_negative_float(parameter: MaterialParameter) -> MaterialParameter:
    if parameter.type == "map" or parameter.type == "math":
        if not isinstance(parameter.text, str):
            raise ValueError(
                f"MaterialParameter {parameter.type=}, which requires parameter.text to be of type(str), but {parameter.text=}."
            )
        return parameter
    elif isinstance(parameter.text, float | int):
        if parameter.text < 0.0:
            raise ValueError(f"{parameter.text=} must be greater than or equal to 0.0")
        return parameter
    else:
        raise ValueError(f"{parameter.text=} of type(str) but {parameter.type=} when it must be 'map' or 'math'")


def mat_is_gte_one_float(parameter: MaterialParameter) -> MaterialParameter:
    if parameter.type == "map" or parameter.type == "math":
        if not isinstance(parameter.text, str):
            raise ValueError(
                f"MaterialParameter {parameter.type=}, which requires parameter.text to be of type(str), but {parameter.text=}."
            )
        return parameter
    elif isinstance(parameter.text, float | int):
        if parameter.text < 1.0:
            raise ValueError(f"{parameter.text=} must be greater than or equal to 1.0")
        return parameter
    else:
        raise ValueError(f"{parameter.text=} of type(str) but {parameter.type=} when it must be 'map' or 'math'")


def mat_is_gt_one_float(parameter: MaterialParameter) -> MaterialParameter:
    if parameter.type == "map" or parameter.type == "math":
        if not isinstance(parameter.text, str):
            raise ValueError(
                f"MaterialParameter {parameter.type=}, which requires parameter.text to be of type(str), but {parameter.text=}."
            )
        return parameter
    elif isinstance(parameter.text, float | int):
        if parameter.text <= 1.0:
            raise ValueError(f"{parameter.text=} must be greater than 1.0")
        return parameter
    else:
        raise ValueError(f"{parameter.text=} of type(str) but {parameter.type=} when it must be 'map' or 'math'")


def mat_is_gte_two_float(parameter: MaterialParameter) -> MaterialParameter:
    if parameter.type == "map" or parameter.type == "math":
        if not isinstance(parameter.text, str):
            raise ValueError(
                f"MaterialParameter {parameter.type=}, which requires parameter.text to be of type(str), but {parameter.text=}."
            )
        return parameter
    elif isinstance(parameter.text, float | int):
        if parameter.text < 2.0:
            raise ValueError(f"{parameter.text=} must be greater than or equal to 2.0")
        return parameter
    else:
        raise ValueError(f"{parameter.text=} of type(str) but {parameter.type=} when it must be 'map' or 'math'")


def mat_is_lte_onethird_gte_zero(parameter: MaterialParameter) -> MaterialParameter:
    if parameter.type == "map" or parameter.type == "math":
        if not isinstance(parameter.text, str):
            raise ValueError(
                f"MaterialParameter {parameter.type=}, which requires parameter.text to be of type(str), but {parameter.text=}."
            )
        return parameter
    elif isinstance(parameter.text, float | int):
        if parameter.text < 0.0 or parameter.text > 1.0 / 3.0:
            raise ValueError(f"{parameter.text=} must be in domain [0.0, 1./3.]")
        return parameter
    else:
        raise ValueError(f"{parameter.text=} of type(str) but {parameter.type=} when it must be 'map' or 'math'")


def mat_is_lte_90_gte_0(parameter: MaterialParameter) -> MaterialParameter:
    if parameter.type == "map" or parameter.type == "math":
        if not isinstance(parameter.text, str):
            raise ValueError(
                f"MaterialParameter {parameter.type=}, which requires parameter.text to be of type(str), but {parameter.text=}."
            )
        return parameter
    elif isinstance(parameter.text, float | int):
        if parameter.text < 0.0 or parameter.text > 90.0:
            raise ValueError(f"{parameter.text=} must be in domain [0.0, 90.0]")
        return parameter
    else:
        raise ValueError(f"{parameter.text=} of type(str) but {parameter.type=} when it must be 'map' or 'math'")


def mat_is_positive_int(parameter: MaterialParameter) -> MaterialParameter:
    if parameter.type == "map" or parameter.type == "math":
        if not isinstance(parameter.text, str):
            raise ValueError(
                f"MaterialParameter {parameter.type=}, which requires parameter.text to be of type(str), but {parameter.text=}."
            )
        return parameter
    elif isinstance(parameter.text, float):
        raise ValueError(f"{parameter.text=} must be type(int)")
    elif isinstance(parameter.text, int):
        if parameter.text < 1:
            raise ValueError(f"{parameter.text=} must be greater than 0")
        return parameter
    else:
        raise ValueError(f"{parameter.text=} of type(str) but {parameter.type=} when it must be 'map' or 'math'")


def mat_is_positive_int_mult10(parameter: MaterialParameter) -> MaterialParameter:
    if parameter.type == "map" or parameter.type == "math":
        if not isinstance(parameter.text, str):
            raise ValueError(
                f"MaterialParameter {parameter.type=}, which requires parameter.text to be of type(str), but {parameter.text=}."
            )
        return parameter
    elif isinstance(parameter.text, float):
        raise ValueError(f"{parameter.text=} must be type(int)")
    elif isinstance(parameter.text, int):
        if parameter.text % 10 != 0 and parameter.text > 0:
            raise ValueError(f"{parameter.text=} must be a multiple of 10 and greater than 0")
        return parameter
    else:
        raise ValueError(f"{parameter.text=} of type(str) but {parameter.type=} when it must be 'map' or 'math'")


def mat_is_string_float_vec3(parameter: MaterialParameter) -> MaterialParameter:
    if parameter.type == "map" or parameter.type == "math":
        if not isinstance(parameter.text, str):
            raise ValueError(
                f"MaterialParameter {parameter.type=}, which requires parameter.text to be of type(str), but {parameter.text=}."
            )
        return parameter
    elif parameter.text is StringFloatVec3:
        return parameter
    else:
        raise ValueError(f"{parameter.text=} must be of type(StringFloatVec3)")


def mat_is_string_float_vec9(parameter: MaterialParameter) -> MaterialParameter:
    if parameter.type == "map" or parameter.type == "math":
        if not isinstance(parameter.text, str):
            raise ValueError(
                f"MaterialParameter {parameter.type=}, which requires parameter.text to be of type(str), but {parameter.text=}."
            )
        return parameter
    elif parameter.text is StringFloatVec9:
        return parameter
    else:
        raise ValueError(f"{parameter.text=} must be of type(StringFloatVec9)")


MatPositiveFloat: TypeAlias = Annotated[MaterialParameter, AfterValidator(mat_is_positive_float)]
MatNonNegativeFloat: TypeAlias = Annotated[MaterialParameter, AfterValidator(mat_is_non_negative_float)]
MatGTEOneFloat: TypeAlias = Annotated[MaterialParameter, AfterValidator(mat_is_gte_one_float)]
MatGTOneFloat: TypeAlias = Annotated[MaterialParameter, AfterValidator(mat_is_gt_one_float)]
MatGTETwoFloat: TypeAlias = Annotated[MaterialParameter, AfterValidator(mat_is_gte_two_float)]
MatLTE_OneThird_GTE_Zero: TypeAlias = Annotated[MaterialParameter, AfterValidator(mat_is_lte_onethird_gte_zero)]
MatLTE_90_GTE_0: TypeAlias = Annotated[MaterialParameter, AfterValidator(mat_is_lte_90_gte_0)]
MatPositiveInt: TypeAlias = Annotated[MaterialParameter, AfterValidator(mat_is_positive_int)]
MatPositiveIntMult10: TypeAlias = Annotated[MaterialParameter, AfterValidator(mat_is_positive_int_mult10)]
MatStringFloatVec3: TypeAlias = Annotated[MaterialParameter, AfterValidator(mat_is_string_float_vec3)]
MatStringFloatVec9: TypeAlias = Annotated[MaterialParameter, AfterValidator(mat_is_string_float_vec9)]


class MaterialBase(BaseXmlModel, tag="material", extra="forbid"):
    name: str | None = attr(default=None)
    id: int | None = attr(default=None)
    density: MatPositiveFloat = element(default=MaterialParameter(text=1.0))


class MaterialBaseNoDensity(BaseXmlModel, tag="solid", extra="forbid"):
    name: str | None = attr(default=None)
    id: int | None = attr(default=None)


class ActiveContraction(BaseXmlModel, tag="active_contraction", extra="forbid"):
    type: Literal["active contraction"] = attr(default="active contraction", frozen=True)
    ascl: DynamicMaterialParameter = element(default=DynamicMaterialParameter(text=1.0))
    ca0: MatPositiveFloat = element(default=MaterialParameter(text=4.35))
    beta: MatPositiveFloat = element(default=MaterialParameter(text=4.75))
    l0: MatPositiveFloat = element(default=MaterialParameter(text=1.58))
    refl: MatPositiveFloat = element(default=MaterialParameter(text=2.04))


class SolidBoundMolecule(BaseXmlModel, tag="solid_bound", extra="forbid"):
    sbm: int = attr(default=1)
    rho0: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    rhomin: MatPositiveFloat = element(default=MaterialParameter(text=0.1))
    rhomax: MatPositiveFloat = element(default=MaterialParameter(text=5.0))


class ArrudaBoyce(MaterialBase, tag="material", extra="forbid"):
    type: Literal["Arruda-Boyce unconstrained"] = attr(default="Arruda-Boyce unconstrained", frozen=True)
    ksi: MatPositiveFloat = element(default=MaterialParameter(text=10.0))
    N: MatPositiveInt = element(default=MaterialParameter(text=5))
    n_term: int = element(default=3, ge=3, le=30)
    kappa: MatPositiveFloat = element(default=MaterialParameter(text=1.0))


class CarterHayes(MaterialBase, tag="solid", extra="forbid"):
    type: Literal["Carter-Hayes"] = attr(default="Carter-Hayes", frozen=True)
    E0: MatPositiveFloat = element(default=MaterialParameter(text=10000.0))
    rho0: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    gamma: MatPositiveFloat = element(default=MaterialParameter(text=2.0))
    v: MatNonNegativeFloat = element(default=MaterialParameter(text=0.3))
    sbm: MatPositiveInt = element(default=MaterialParameter(text=1))


class CellGrowth(MaterialBase, tag="material", extra="forbid"):
    type: Literal["cell growth"] = attr(default="cell growth", frozen=True)
    phir: MatPositiveFloat = element(default=DynamicMaterialParameter(text=10000.0))
    cr: MatPositiveFloat = element(default=DynamicMaterialParameter(text=1.0))
    ce: MatPositiveFloat = element(default=MaterialParameter(text=300.0))


class CubicCLE(MaterialBase, tag="material", extra="forbid"):
    type: Literal["cubic CLE"] = attr(default="cubic CLE", frozen=True)
    lp1: MatPositiveFloat = element(default=MaterialParameter(text=13.01))
    lm1: MatPositiveFloat = element(default=MaterialParameter(text=0.49))
    l2: MatPositiveFloat = element(default=MaterialParameter(text=0.66))
    mu: MatPositiveFloat = element(default=MaterialParameter(text=0.16))


class CoupledMooneyRivlin(MaterialBase, tag="material", extra="forbid"):
    type: Literal["coupled Mooney-Rivlin"] = attr(default="coupled Mooney-Rivlin", frozen=True)
    c1: MatPositiveFloat = element(default=MaterialParameter(text=10.0))
    c2: MatNonNegativeFloat = element(default=MaterialParameter(text=1.0))
    k: MatPositiveFloat = element(default=MaterialParameter(text=100.0))


class CoupledVerondaWestmann(MaterialBase, tag="material", extra="forbid"):
    type: Literal["coupled Veronda-Westmann"] = attr(default="coupled Veronda-Westmann", frozen=True)
    c1: MatPositiveFloat = element(default=MaterialParameter(text=10.0))
    c2: MatNonNegativeFloat = element(default=MaterialParameter(text=1.0))
    k: MatPositiveFloat = element(default=MaterialParameter(text=100.0))


class DonnanEquilibrium(BaseXmlModel, tag="solid", extra="forbid"):
    type: Literal["Donnan equilibrium"] = attr(default="Donnan equilibrium", frozen=True)
    phiw0: MatPositiveFloat = element(default=MaterialParameter(text=0.8))
    cF0: MatPositiveFloat = element(default=DynamicMaterialParameter(text=1.0))
    bosm: MatPositiveFloat = element(default=MaterialParameter(text=0.8))


class EllipsoidalFiberDistribution(BaseXmlModel, tag="solid", extra="forbid"):
    type: Literal["ellipsoidal fiber distribution"] = attr(default="ellipsoidal fiber distribution", frozen=True)
    ksi: MatStringFloatVec3 = element(default=MaterialParameter(text="10,12,15"))
    beta: MatStringFloatVec3 = element(default=MaterialParameter(text="2.5,3,3"))


class EllipsoidalFiberDistributionNeoHookean(MaterialBase, tag="material", extra="forbid"):
    type: Literal["EFD neo-Hookean"] = attr(default="EFD neo-Hookean", frozen=True)
    E: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    v: MatPositiveFloat = element(default=MaterialParameter(text=0.3))
    beta: MatStringFloatVec3 = element(default=MaterialParameter(text="2.5,3.0,3.0"))
    ksi: MatStringFloatVec3 = element(default=MaterialParameter(text="1.0,1.0,1.0"))


class EllipsoidalFiberDistributionDonnanEquilibrium(MaterialBase, tag="material", extra="forbid"):
    type: Literal["EFD Donnan equilibrium"] = attr(default="EFD Donnan equilibrium", frozen=True)
    phiw0: MatPositiveFloat = element(default=MaterialParameter(text=0.8))
    cF0: DynamicMaterialParameter = element(default=DynamicMaterialParameter(text=0.3))
    bosm: MaterialParameter = element(default=MaterialParameter(text=300))
    beta: MatStringFloatVec3 = element(default=MaterialParameter(text="2.5,3.0,3.0"))
    ksi: MatStringFloatVec3 = element(default=MaterialParameter(text="1.0,1.0,1.0"))


class FungOrthotropicCompressible(MaterialBase, tag="material", extra="forbid"):
    type: Literal["Fung-ortho-compressible"] = attr(default="Fung-ortho-compressible", frozen=True)
    E1: MatPositiveFloat = element(default=MaterialParameter(text=124.0))
    E2: MatPositiveFloat = element(default=MaterialParameter(text=124.0))
    E3: MatPositiveFloat = element(default=MaterialParameter(text=36.0))
    G12: MatPositiveFloat = element(default=MaterialParameter(text=67.0))
    G23: MatPositiveFloat = element(default=MaterialParameter(text=40.0))
    G31: MatPositiveFloat = element(default=MaterialParameter(text=40.0))
    v12: MatPositiveFloat = element(default=MaterialParameter(text=0.075))
    v23: MatPositiveFloat = element(default=MaterialParameter(text=0.87))
    v31: MatPositiveFloat = element(default=MaterialParameter(text=0.26))
    c: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    k: MatPositiveFloat = element(default=MaterialParameter(text=120.0))


class GentCompressible(MaterialBase, tag="material", extra="forbid"):
    type: Literal["compressible Gent"] = attr(default="compressible Gent", frozen=True)
    G: MatPositiveFloat = element(default=MaterialParameter(text=3.14))
    Jm: MatPositiveFloat = element(default=MaterialParameter(text=1.5))
    K: MatPositiveFloat = element(default=MaterialParameter(text=1e5))


class HolmesMow(MaterialBase, tag="material", extra="forbid"):
    type: Literal["Holmes-Mow"] = attr(default="Holmes-Mow", frozen=True)
    E: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    v: MatPositiveFloat = element(default=MaterialParameter(text=0.35))
    beta: MatPositiveFloat = element(default=MaterialParameter(text=0.25))


class HolzapfelGasserOgdenUnconstrained(MaterialBase, tag="material", extra="forbid"):
    type: Literal["HGO unconstrained"] = attr(default="HGO unconstrained", frozen=True)
    c: MatPositiveFloat = element(default=MaterialParameter(text=7.64))
    k1: MatPositiveFloat = element(default=MaterialParameter(text=996.6))
    k2: MatPositiveFloat = element(default=MaterialParameter(text=524.6))
    gamma: MatLTE_90_GTE_0 = element(default=MaterialParameter(text=49.98))
    kappa: MatLTE_OneThird_GTE_Zero = element(default=MaterialParameter(text=0.226))
    k: MatPositiveFloat = element(default=MaterialParameter(text=7.64e3))
    mat_axis: MaterialAxisVector | None = element(default=None)
    fiber: FiberVector | None = element(default=None)


class IsotropicElastic(MaterialBase, tag="material", extra="forbid"):
    type: Literal["isotropic elastic"] = attr(default="isotropic elastic", frozen=True)
    E: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    v: MatNonNegativeFloat = element(default=MaterialParameter(text=0.3))


class IsotropicHencky(MaterialBase, tag="material", extra="forbid"):
    type: Literal["isotropic Hencky"] = attr(default="isotropic Hencky", frozen=True)
    E: MatPositiveFloat = element(default=MaterialParameter(text=1000.0))
    v: MatPositiveFloat = element(default=MaterialParameter(text=0.45))


class KinematicGrowth(MaterialBase, tag="material", extra="forbid"):
    elastic: str = element()
    growth: Literal["volume", "growth", "area growth", "fiber growth"] = element(default="volume")


class LargePoissonRatioLigament(MaterialBase, tag="material", extra="forbid"):
    type: Literal["PRLig"] = attr(default="PRLig", frozen=True)
    c1: MatPositiveFloat = element(default=MaterialParameter(text=90.0))
    c2: MatPositiveFloat = element(default=MaterialParameter(text=160.0))
    mu: MatPositiveFloat = element(default=MaterialParameter(text=0.025))
    v0: MatPositiveFloat = element(default=MaterialParameter(text=5.85))
    m: MatPositiveFloat = element(default=MaterialParameter(text=100.0))
    k: MatPositiveFloat = element(default=MaterialParameter(text=1.55))


class Lung(MaterialBase, tag="material", extra="forbid"):
    type: Literal["lung"] = attr(default="lung", frozen=True)
    E: MatPositiveFloat = element(default=MaterialParameter(text=1913.7))
    v: MatPositiveFloat = element(default=MaterialParameter(text=0.3413))
    c1: MatPositiveFloat = element(default=MaterialParameter(text=278.2))
    c3: MatPositiveFloat = element(default=MaterialParameter(text=5.766))
    d1: MatPositiveFloat = element(default=MaterialParameter(text=3.0))
    d3: MatPositiveFloat = element(default=MaterialParameter(text=6.0))


class NaturalNeoHookean(MaterialBase, tag="material", extra="forbid"):
    type: Literal["natural neo-Hookean"] = attr(default="natural neo-Hookean", frozen=True)
    E: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    v: MatNonNegativeFloat = element(default=MaterialParameter(text=0.3))


class NeoHookean(MaterialBase, tag="material", extra="forbid"):
    type: Literal["neo-Hookean"] = attr(default="neo-Hookean", frozen=True)
    E: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    v: MatNonNegativeFloat = element(default=MaterialParameter(text=0.3))


class OrthotropicElastic(MaterialBase, tag="material", extra="forbid"):
    type: Literal["orthotropic elastic"] = attr(default="orthotropic elastic", frozen=True)
    E1: MatPositiveFloat = element(default=MaterialParameter(text=13.4))
    E2: MatPositiveFloat = element(default=MaterialParameter(text=14.1))
    E3: MatPositiveFloat = element(default=MaterialParameter(text=22.9))
    v12: MatNonNegativeFloat = element(default=MaterialParameter(text=0.42))
    v23: MatNonNegativeFloat = element(default=MaterialParameter(text=0.23))
    v31: MatNonNegativeFloat = element(default=MaterialParameter(text=0.38))
    G12: MatPositiveFloat = element(default=MaterialParameter(text=4.6))
    G23: MatPositiveFloat = element(default=MaterialParameter(text=6.2))
    G31: MatPositiveFloat = element(default=MaterialParameter(text=5.8))
    mat_axis: MaterialAxisVector | None = element(default=None)


class OrthotropicCLE(MaterialBase, tag="material", extra="forbid"):
    type: Literal["orthotropic CLE"] = attr(default="orthotropic CLE", frozen=True)
    lp11: MatPositiveFloat = element(default=MaterialParameter(text=13.01))
    lp22: MatPositiveFloat = element(default=MaterialParameter(text=13.01))
    lp33: MatPositiveFloat = element(default=MaterialParameter(text=13.01))
    lm11: MatPositiveFloat = element(default=MaterialParameter(text=0.49))
    lm22: MatPositiveFloat = element(default=MaterialParameter(text=0.49))
    lm33: MatPositiveFloat = element(default=MaterialParameter(text=0.49))
    l12: MatPositiveFloat = element(default=MaterialParameter(text=0.66))
    l23: MatPositiveFloat = element(default=MaterialParameter(text=0.66))
    l31: MatPositiveFloat = element(default=MaterialParameter(text=0.66))
    mu1: MatPositiveFloat = element(default=MaterialParameter(text=0.16))
    mu2: MatPositiveFloat = element(default=MaterialParameter(text=0.16))
    mu3: MatPositiveFloat = element(default=MaterialParameter(text=0.16))


class OsmoticVirialPressure(MaterialBaseNoDensity, tag="solid", extra="forbid"):
    type: Literal["osmotic virial expansion"] = attr(default="osmotic virial expansion", frozen=True)
    phiw0: MaterialParameter = element(default=MaterialParameter(text=0.8))
    cr: DynamicMaterialParameter = element(default=DynamicMaterialParameter(text=100.0))
    c1: MaterialParameter = element(default=MaterialParameter(text=2.436e-6))
    c2: MaterialParameter = element(default=MaterialParameter(text=0.0))
    c3: MaterialParameter = element(default=MaterialParameter(text=0.0))


class PerfectOsmometer(MaterialBaseNoDensity, tag="solid", extra="forbid"):
    type: Literal["perfect osmometer"] = attr(default="perfect osmometer", frozen=True)
    phiw0: MatPositiveFloat = element(default=MaterialParameter(text=0.8))
    iosm: MatPositiveFloat = element(default=MaterialParameter(text=300.0))
    bosm: DynamicMaterialParameter = element(default=DynamicMaterialParameter(text=1.0))


class PorousNeoHookean(MaterialBase, tag="material", extra="forbid"):
    type: Literal["porous neo-Hookean"] = attr(default="porous neo-Hookean", frozen=True)
    E: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    phi0: MatPositiveFloat = element(default=MaterialParameter(text=0.5))


class ShenoyWang(MaterialBase, tag="material", extra="forbid"):
    type: Literal["Shenoy"] = attr(default="Shenoy", frozen=True)
    mu: MatPositiveFloat = element(default=MaterialParameter(text=0.7692))
    k: MatPositiveFloat = element(default=MaterialParameter(text=1.667))
    Ef: MatPositiveFloat = element(default=MaterialParameter(text=134.6))
    lam_c: MatPositiveFloat = element(default=MaterialParameter(text=1.02))
    lam_t: MatPositiveFloat = element(default=MaterialParameter(text=0.255))
    n: MatPositiveFloat = element(default=MaterialParameter(text=5))
    m: MatPositiveFloat = element(default=MaterialParameter(text=30))


class SphericalFiberDistribution(MaterialBaseNoDensity, tag="solid", extra="forbid"):
    type: Literal["spherical fiber distribution"] = attr(default="spherical fiber distribution", frozen=True)
    ksi: MatPositiveFloat = element(default=MaterialParameter(text=10.0))
    alpha: MatNonNegativeFloat = element(default=MaterialParameter(text=0.0))
    beta: MatGTETwoFloat = element(default=MaterialParameter(text=2.5))


class SphericalFiberDistributionSBM(MaterialBaseNoDensity, tag="solid", extra="forbid"):
    type: Literal["spherical fiber distribution"] = attr(default="spherical fiber distribution sbm", frozen=True)
    alpha: MatNonNegativeFloat = element(default=MaterialParameter(text=0.0))
    beta: MatGTETwoFloat = element(default=MaterialParameter(text=2.5))
    ksi0: MatPositiveFloat = element(default=MaterialParameter(text=10.0))
    gamma: MatPositiveFloat = element(default=MaterialParameter(text=2.0))
    rho0: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    sbm: MatPositiveInt = element(default=MaterialParameter(text=1))


class TransIsoMooneyRivlin(MaterialBase, tag="material", extra="forbid"):
    type: Literal["coupled trans-iso Mooney-Rivlin"] = attr(default="coupled trans-iso Mooney-Rivlin", frozen=True)
    c1: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    c2: MatNonNegativeFloat = element(default=MaterialParameter(text=0.1))
    c3: MatNonNegativeFloat = element(default=MaterialParameter(text=0.0))
    c4: MatPositiveFloat = element(default=MaterialParameter(text=43.0))
    c5: MatPositiveFloat = element(default=MaterialParameter(text=3.0))
    lam_max: MatGTOneFloat = element(default=MaterialParameter(text=1.05))
    k: MatPositiveFloat = element(default=MaterialParameter(text=10.0))
    fiber: FiberVector | None = element(default=None)


class TransIsoVerondaWestmann(MaterialBase, tag="material", extra="forbid"):
    type: Literal["coupled trans-iso Veronda-Westmann"] = attr(default="coupled trans-iso Veronda-Westmann", frozen=True)
    c1: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    c2: MatNonNegativeFloat = element(default=MaterialParameter(text=0.1))
    c3: MatNonNegativeFloat = element(default=MaterialParameter(text=1.0))
    c4: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    c5: MatPositiveFloat = element(default=MaterialParameter(text=1.34))
    lam_max: MatGTOneFloat = element(default=MaterialParameter(text=1.3), alias="lambda")
    k: MatPositiveFloat = element(default=MaterialParameter(text=100.0))
    fiber: FiberVector | None = element(default=None)


class UnconstrainedOgden(MaterialBase, tag="material", extra="forbid"):
    type: Literal["Ogden unconstrained"] = attr(default="Ogden unconstrained", frozen=True)
    m1: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    c1: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    m2: MatPositiveFloat | None = element(default=None)
    c2: MatPositiveFloat | None = element(default=None)
    m3: MatPositiveFloat | None = element(default=None)
    c3: MatPositiveFloat | None = element(default=None)
    m4: MatPositiveFloat | None = element(default=None)
    c4: MatPositiveFloat | None = element(default=None)
    m5: MatPositiveFloat | None = element(default=None)
    c5: MatPositiveFloat | None = element(default=None)
    m6: MatPositiveFloat | None = element(default=None)
    c6: MatPositiveFloat | None = element(default=None)


UnconstrainedMaterials: TypeAlias = (
    ArrudaBoyce
    | CoupledMooneyRivlin
    | CoupledVerondaWestmann
    | CubicCLE
    | EllipsoidalFiberDistributionNeoHookean
    | FungOrthotropicCompressible
    | GentCompressible
    | HolmesMow
    | HolzapfelGasserOgdenUnconstrained
    | IsotropicElastic
    | IsotropicHencky
    | LargePoissonRatioLigament
    | Lung
    | NaturalNeoHookean
    | NeoHookean
    | PorousNeoHookean
    | OrthotropicElastic
    | OrthotropicCLE
    | ShenoyWang
    | TransIsoMooneyRivlin
    | TransIsoVerondaWestmann
    | UnconstrainedOgden
)

EvolvingUnconstrainedMaterials: TypeAlias = (
    EllipsoidalFiberDistributionDonnanEquilibrium | CellGrowth | OsmoticVirialPressure | PerfectOsmometer
)


class ArrudaBoyceUC(MaterialBase, tag="material", extra="forbid"):
    type: Literal["Arruda-Boyce"] = attr(default="Arruda-Boyce", frozen=True)
    mu: MatPositiveFloat = element(default=MaterialParameter(text=0.09))
    N: MatPositiveFloat = element(default=MaterialParameter(text=26.5))
    k: MatPositiveFloat = element(default=MaterialParameter(text=100.0))


class EllipsoidalFiberDistributionUC(MaterialBaseNoDensity, tag="solid", extra="forbid"):
    type: Literal["EFD uncoupled"] = attr(default="EFD uncoupled", frozen=True)
    ksi: MatStringFloatVec3 = element(default=MaterialParameter(text="10,12,15"))
    beta: MatStringFloatVec3 = element(default=MaterialParameter(text="2.5,3,3"))


class EllipsoidalFiberDistributionMooneyRivlinUC(MaterialBase, tag="material", extra="forbid"):
    type: Literal["EFD Mooney-Rivlin"] = attr(default="EFD Mooney-Rivlin", frozen=True)
    c1: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    c2: MatNonNegativeFloat = element(default=MaterialParameter(text=0.0))
    beta: MatStringFloatVec3 = element(default=MaterialParameter(text="4.5,4.5,4.5"))
    ksi: MatStringFloatVec3 = element(default=MaterialParameter(text="1,1,1"))
    k: MatPositiveFloat = element(default=MaterialParameter(text=1000.0))


class EllipsoidalFiberDistributionVerondaWestmannUC(MaterialBase, tag="material", extra="forbid"):
    type: Literal["EFD Veronda-Westmann"] = attr(default="EFD Veronda-Westmann", frozen=True)
    c1: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    c2: MatNonNegativeFloat = element(default=MaterialParameter(text=0.5))
    beta: MatStringFloatVec3 = element(default=MaterialParameter(text="4.5,4.5,4.5"))
    ksi: MatStringFloatVec3 = element(default=MaterialParameter(text="1,1,1"))
    k: MatPositiveFloat = element(default=MaterialParameter(text=1000.0))


class FungOrthotropicUC(MaterialBase, tag="material", extra="forbid"):
    type: Literal["Fung orthotropic"] = attr(default="Fung orthotropic", frozen=True)
    E1: MatPositiveFloat = element(default=MaterialParameter(text=124.0))
    E2: MatPositiveFloat = element(default=MaterialParameter(text=124.0))
    E3: MatPositiveFloat = element(default=MaterialParameter(text=36.0))
    G12: MatPositiveFloat = element(default=MaterialParameter(text=67.0))
    G23: MatPositiveFloat = element(default=MaterialParameter(text=40.0))
    G31: MatPositiveFloat = element(default=MaterialParameter(text=40.0))
    v12: MatPositiveFloat = element(default=MaterialParameter(text=0.075))
    v23: MatPositiveFloat = element(default=MaterialParameter(text=0.87))
    v31: MatPositiveFloat = element(default=MaterialParameter(text=0.26))
    c: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    k: MatPositiveFloat = element(default=MaterialParameter(text=120000.0))


class GentUC(MaterialBase, tag="material", extra="forbid"):
    type: Literal["Gent"] = attr(default="Gent", frozen=True)
    G: MatPositiveFloat = element(default=MaterialParameter(text=3.14))
    Jm: MatPositiveFloat = element(default=MaterialParameter(text=1.5))
    k: MatPositiveFloat = element(default=MaterialParameter(text=1e5))


class HolmesMowUC(MaterialBase, tag="material", extra="forbid"):
    type: Literal["uncoupled Holmes-Mow"] = attr(default="uncoupled Holmes-Mow", frozen=True)
    mu: MatPositiveFloat = element(default=MaterialParameter(text=0.5))
    beta: MatPositiveFloat = element(default=MaterialParameter(text=2.0))
    k: MatPositiveFloat = element(default=MaterialParameter(text=1000.0))


class HolzapfelGasserOgdenUC(MaterialBase, tag="material", extra="forbid"):
    type: Literal["Holzapfel-Gasser-Ogden"] = attr(default="Holzapfel-Gasser-Ogden", frozen=True)
    c: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    k1: MatPositiveFloat = element(default=MaterialParameter(text=10.0))
    k2: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    gamma: MatLTE_90_GTE_0 = element(default=MaterialParameter(text=45.0))
    kappa: MatLTE_OneThird_GTE_Zero = element(default=MaterialParameter(text=0.1))
    k: MatPositiveFloat = element(default=MaterialParameter(text=100.0))
    mat_axis: MaterialAxisVector | None = element(default=None)
    fiber: FiberVector | None = element(default=None)


class MooneyRivlinUC(MaterialBase, tag="material", extra="forbid"):
    type: Literal["Mooney-Rivlin"] = attr(default="Mooney-Rivlin", frozen=True)
    c1: MatPositiveFloat = element(default=MaterialParameter(text=10.0))
    c2: MatNonNegativeFloat = element(default=MaterialParameter(text=1.0))
    k: MatPositiveFloat = element(default=MaterialParameter(text=1000.0))


class MuscleUC(MaterialBase, tag="material", extra="forbid"):
    type: Literal["muscle material"] = attr(default="muscle material", frozen=True)
    g1: MatPositiveFloat = element(default=MaterialParameter(text=500.0))
    g2: MatPositiveFloat = element(default=MaterialParameter(text=500.0))
    p1: MatPositiveFloat = element(default=MaterialParameter(text=0.5))
    p2: MatPositiveFloat = element(default=MaterialParameter(text=6.6))
    smax: MatPositiveFloat = element(default=MaterialParameter(text=3e5))
    Lofl: MatGTOneFloat = element(default=MaterialParameter(text=1.07))
    lam_max: MatGTOneFloat = element(default=MaterialParameter(text=1.4))
    k: MatPositiveFloat = element(default=MaterialParameter(text=1e6))
    fiber: FiberVector = element(default=FiberVector())


class OgdenUC(MaterialBase, tag="material", extra="forbid"):
    type: Literal["Ogden"] = attr(default="Ogden", frozen=True)
    k: MatPositiveFloat = element(default=MaterialParameter(text=100.0))
    m1: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    c1: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    m2: MatPositiveFloat | None = element(default=None)
    c2: MatPositiveFloat | None = element(default=None)
    m3: MatPositiveFloat | None = element(default=None)
    c3: MatPositiveFloat | None = element(default=None)
    m4: MatPositiveFloat | None = element(default=None)
    c4: MatPositiveFloat | None = element(default=None)
    m5: MatPositiveFloat | None = element(default=None)
    c5: MatPositiveFloat | None = element(default=None)
    m6: MatPositiveFloat | None = element(default=None)
    c6: MatPositiveFloat | None = element(default=None)


class TendonUC(MaterialBase, tag="material", extra="forbid"):
    type: Literal["tendon material"] = attr(default="tendon material", frozen=True)
    g1: MatPositiveFloat = element(default=MaterialParameter(text=5e4))
    g2: MatNonNegativeFloat = element(default=MaterialParameter(text=5e4))
    l1: MatPositiveFloat = element(default=MaterialParameter(text=2.7e6))
    l2: MatPositiveFloat = element(default=MaterialParameter(text=46.4))
    lam_max: MatGTOneFloat = element(default=MaterialParameter(text=1.03))
    k: MatPositiveFloat = element(default=MaterialParameter(text=1e7))
    fiber: FiberVector = element(default=FiberVector())


class TensionCompressionNonlinearOrthoUC(MaterialBase, tag="material", extra="forbid"):
    type: Literal["TC nonlinear orthotropic"] = attr(default="TC nonlinear orthotropic", frozen=True)
    c1: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    c2: MatNonNegativeFloat = element(default=MaterialParameter(text=0.0))
    k: MatPositiveFloat = element(default=MaterialParameter(text=100))
    beta: MatStringFloatVec3 = element(default=MaterialParameter(text="4.3,4.3,4.3"))
    ksi: MatStringFloatVec3 = element(default=MaterialParameter(text="4525,4525,4525"))
    mat_axis: MaterialAxisVector = element(default=MaterialAxisVector())


class TransIsoMooneyRivlinUC(MaterialBase, tag="material", extra="forbid"):
    type: Literal["trans iso Mooney-Rivlin"] = attr(default="trans iso Mooney-Rivlin", frozen=True)
    c1: MatPositiveFloat = element(default=MaterialParameter(text=13.85))
    c2: MatNonNegativeFloat = element(default=MaterialParameter(text=0.0))
    c3: MatNonNegativeFloat = element(default=MaterialParameter(text=2.07))
    c4: MatPositiveFloat = element(default=MaterialParameter(text=61.44))
    c5: MatPositiveFloat = element(default=MaterialParameter(text=640.7))
    lam_max: MatGTOneFloat = element(default=MaterialParameter(text=1.03))
    k: MatPositiveFloat = element(default=MaterialParameter(text=100.0))
    fiber: FiberVector | None = element(default=None)
    active_contraction: ActiveContraction | None = element(default=None)


class TransIsoVerondaWestmannUC(MaterialBase, tag="material", extra="forbid"):
    type: Literal["trans iso Veronda-Westmann"] = attr(default="trans iso Veronda-Westmann", frozen=True)
    c1: MatPositiveFloat = element(default=MaterialParameter(text=13.85))
    c2: MatNonNegativeFloat = element(default=MaterialParameter(text=0.0))
    c3: MatNonNegativeFloat = element(default=MaterialParameter(text=2.07))
    c4: MatPositiveFloat = element(default=MaterialParameter(text=61.44))
    c5: MatPositiveFloat = element(default=MaterialParameter(text=640.7))
    lam_max: MatGTOneFloat = element(default=MaterialParameter(text=1.03))
    k: MatPositiveFloat = element(default=MaterialParameter(text=100.0))
    fiber: FiberVector | None = element(default=None)
    active_contraction: ActiveContraction | None = element(default=None)


class VerondaWestmannUC(MaterialBase, tag="material", extra="forbid"):
    type: Literal["Veronda-Westmann"] = attr(default="Veronda-Westmann", frozen=True)
    c1: MatPositiveFloat = element(default=MaterialParameter(text=1000.0))
    c2: MatNonNegativeFloat = element(default=MaterialParameter(text=2000.0))
    k: MatPositiveFloat = element(default=MaterialParameter(text=1000.0))


class MooneyRivlinVonMisesFibersUC(MaterialBase, tag="material", extra="forbid"):
    type: Literal["Mooney-Rivlin von Mises Fibers"] = attr(default="Mooney-Rivlin von Mises Fibers", frozen=True)
    c1: MatPositiveFloat = element(default=MaterialParameter(text=10.0))
    c2: MatNonNegativeFloat = element(default=MaterialParameter(text=0.0))
    c3: MatPositiveFloat = element(default=MaterialParameter(text=50.0))
    c4: MatPositiveFloat = element(default=MaterialParameter(text=5.0))
    c5: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    k: MatPositiveFloat = element(default=MaterialParameter(text=100000.0))
    kf: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    vmc: MatPositiveFloat = element(default=MaterialParameter(text=2.0))
    var_n: MatPositiveFloat = element(default=MaterialParameter(text=2.0))
    tp: MatNonNegativeFloat = element(default=MaterialParameter(text=0.0))
    gipt: MatPositiveIntMult10 = element(default=MaterialParameter(text=40))
    mat_axis: MaterialAxisVector = element(default=MaterialAxisVector())


class LeeSacksUC(MaterialBase, tag="material", extra="forbid"):
    type: Literal["uncoupled isotropic Lee-Sacks"] = attr(default="uncoupled isotropic Lee-Sacks", frozen=True)
    c0: MatPositiveFloat = element(default=MaterialParameter(text=10.0))
    c1: MatPositiveFloat = element(default=MaterialParameter(text=0.209))
    c2: MatNonNegativeFloat = element(default=MaterialParameter(text=9.046))
    tangent_scale: MatGTEOneFloat = element(default=MaterialParameter(text=1.0))
    k: MatPositiveFloat = element(default=MaterialParameter(text=1000.0))


class Yeoh(MaterialBase, tag="material", extra="forbid"):
    type: Literal["Yeoh"] = attr(default="Yeoh", frozen=True)
    c1: MatPositiveFloat = element(default=MaterialParameter(text=0.75))
    c2: MatNonNegativeFloat | None = element(default=None)
    c3: MatNonNegativeFloat | None = element(default=None)
    c4: MatNonNegativeFloat | None = element(default=None)
    c5: MatNonNegativeFloat | None = element(default=None)
    c6: MatNonNegativeFloat | None = element(default=None)
    k: MatPositiveFloat = element(default=MaterialParameter(text=100.0))


UncoupledMaterials: TypeAlias = (
    ArrudaBoyceUC
    | EllipsoidalFiberDistributionMooneyRivlinUC
    | EllipsoidalFiberDistributionVerondaWestmannUC
    | FungOrthotropicUC
    | GentUC
    | HolmesMowUC
    | HolzapfelGasserOgdenUC
    | MooneyRivlinUC
    | MuscleUC
    | OgdenUC
    | TendonUC
    | TensionCompressionNonlinearOrthoUC
    | TransIsoMooneyRivlinUC
    | TransIsoVerondaWestmannUC
    | MooneyRivlinVonMisesFibersUC
    | LeeSacksUC
    | Yeoh
)


class RigidBody(MaterialBase, tag="material", extra="forbid"):
    type: Literal["rigid body"] = attr(default="rigid body", frozen=True)
    center_of_mass: StringFloatVec3 | None = element(default=None)
    E: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    v: MatNonNegativeFloat = element(default=MaterialParameter(text=0.3))


# Unconstrained Fibers
class FiberExponentialPower(BaseXmlModel, tag="solid", extra="forbid"):
    type: str = attr(default="fiber-exp-pow", frozen=True)
    ksi: MatPositiveFloat = element(default=MaterialParameter(text=5.0))
    alpha: MatNonNegativeFloat = element(default=MaterialParameter(text=20.0))
    beta: MatGTETwoFloat = element(default=MaterialParameter(text=2.0))
    lam0: MatGTOneFloat = element(default=MaterialParameter(text=1.0))
    fiber: FiberVector | None = element(default=None)


class FiberNeoHookean(BaseXmlModel, tag="solid", extra="forbid"):
    type: str = attr(default="fiber-NH", frozen=True)
    mu: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    fiber: FiberVector | None = element(default=None)


class FiberNaturalNeoHookean(BaseXmlModel, tag="solid", extra="forbid"):
    type: str = attr(default="fiber-natural-NH", frozen=True)
    ksi: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    lam0: MatGTEOneFloat = element(default=MaterialParameter(text=1.0))
    fiber: FiberVector | None = element(default=None)


class FiberToeLinear(BaseXmlModel, tag="solid", extra="forbid"):
    type: str = attr(default="fiber-pow-linear", frozen=True)
    E: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    beta: MatGTETwoFloat = element(default=MaterialParameter(text=2.0))
    lam0: MatGTOneFloat = element(default=MaterialParameter(text=1.01))
    fiber: FiberVector | None = element(default=None)


class FiberExponentialPowerLinear(BaseXmlModel, tag="solid", extra="forbid"):
    type: str = attr(default="fiber-exp-pow-linear", frozen=True)
    E: MatPositiveFloat = element(default=MaterialParameter(text=1080.0))
    alpha: MatNonNegativeFloat = element(default=MaterialParameter(text=1400.0))
    beta: MatGTETwoFloat = element(default=MaterialParameter(text=2.73))
    lam0: MatGTOneFloat = element(default=MaterialParameter(text=1.01))
    fiber: FiberVector | None = element(default=None)


class FiberExponentialLinear(BaseXmlModel, tag="solid", extra="forbid"):
    type: str = attr(default="fiber-exp-linear", frozen=True)
    c3: MatNonNegativeFloat = element(default=MaterialParameter(text=0.0))
    c4: MatPositiveFloat = element(default=MaterialParameter(text=43.0))
    c5: MatPositiveFloat = element(default=MaterialParameter(text=3.0))
    lam0: MatGTOneFloat = element(default=MaterialParameter(text=1.05), tag="lambda")
    fiber: FiberVector | None = element(default=None)


class FiberEntropyChain(BaseXmlModel, tag="solid", extra="forbid"):
    type: str = attr(default="fiber-entropy-chain", frozen=True)
    ksi: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    N: MatGTOneFloat = element(default=MaterialParameter(text=2.0))
    n_term: MatPositiveInt = element(default=MaterialParameter(text=2))
    fiber: FiberVector | None = element(default=None)


FiberModel: TypeAlias = (
    FiberNeoHookean
    | FiberNaturalNeoHookean
    | FiberToeLinear
    | FiberEntropyChain
    | FiberExponentialPower
    | FiberExponentialLinear
    | FiberEntropyChain
)


# Uncoupled Fibers
class FiberExponentialPowerUC(BaseXmlModel, tag="solid", extra="forbid"):
    type: str = attr(default="fiber-exp-pow-uncoupled")
    ksi: MatPositiveFloat = element(default=MaterialParameter(text=5.0))
    alpha: MatNonNegativeFloat = element(default=MaterialParameter(text=20.0))
    beta: MatGTETwoFloat = element(default=MaterialParameter(text=3.0))
    fiber: FiberVector | None = element(default=None)


class FiberKiousisUC(BaseXmlModel, tag="solid", extra="forbid"):
    type: str = attr(default="fiber-Kiousis-uncoupled")
    d1: MatPositiveFloat = element(default=MaterialParameter(text=500.0))
    d2: MatGTOneFloat = element(default=MaterialParameter(text=2.25))
    n: MatNonNegativeFloat = element(default=MaterialParameter(text=3))
    fiber: FiberVector | None = element(default=None)


class FiberToeLinearUC(BaseXmlModel, tag="solid", extra="forbid"):
    type: str = attr(default="fiber-pow-linear-uncoupled", frozen=True)
    E: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    beta: MatGTETwoFloat = element(default=MaterialParameter(text=2.0))
    lam0: MatGTOneFloat = element(default=MaterialParameter(text=1.01))
    fiber: FiberVector | None = element(default=None)


class FiberExponentialLinearUC(BaseXmlModel, tag="solid", extra="forbid"):
    type: str = attr(default="uncoupled fiber-exp-linear", frozen=True)
    c3: MatNonNegativeFloat = element(default=MaterialParameter(text=0.0))
    c4: MatPositiveFloat = element(default=MaterialParameter(text=43.0))
    c5: MatPositiveFloat = element(default=MaterialParameter(text=3.0))
    lam0: MatGTOneFloat = element(default=MaterialParameter(text=1.05), tag="lambda")
    fiber: FiberVector | None = element(default=None)


class FiberEntropyChainUC(BaseXmlModel, tag="solid", extra="forbid"):
    type: str = attr(default="uncoupled fiber-entropy-chain", frozen=True)
    ksi: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    N: MatGTOneFloat = element(default=MaterialParameter(text=2.0))
    n_term: MatPositiveInt = element(default=MaterialParameter(text=2))
    fiber: FiberVector | None = element(default=None)


FiberModelUC: TypeAlias = FiberToeLinearUC | FiberKiousisUC | FiberExponentialPowerUC | FiberExponentialLinearUC | FiberEntropyChainUC


# Continuous Fiber Distribution Functions
class CFDSpherical(BaseXmlModel, tag="distribution", extra="forbid"):
    type: Literal["spherical"] = attr(default="spherical", frozen=True)


class CFDEllipsoidal(BaseXmlModel, tag="distribution", extra="forbid"):
    type: Literal["ellipsoidal"] = attr(default="ellipsoidal", frozen=True)
    spa: MatStringFloatVec3 = element(default=MaterialParameter(text="1.0,1.0,1.0"))


class CFDVonMises3d(BaseXmlModel, tag="distribution", extra="forbid"):
    type: Literal["von-Mises-3d"] = attr(default="von-Mises-3d")
    b: MatNonNegativeFloat = element(default=MaterialParameter(text=0.5))


class CFDCircular(BaseXmlModel, tag="distribution", extra="forbid"):
    type: Literal["circular"] = attr(default="circular")


class CFDElliptical(BaseXmlModel, tag="distribution", extra="forbid"):
    type: Literal["elliptical"] = attr(default="elliptical", frozen=True)
    spa1: MatNonNegativeFloat = element(default=MaterialParameter(text=1.0))
    spa2: MatNonNegativeFloat = element(default=MaterialParameter(text=1.0))


class CFDVonMises2d(BaseXmlModel, tag="distribution", extra="forbid"):
    type: Literal["von-Mises-2d"] = attr(default="von-Mises-2d")
    b: MatNonNegativeFloat = element(default=MaterialParameter(text=0.5))


CFDistributionModel: TypeAlias = CFDCircular | CFDSpherical | CFDVonMises3d | CFDVonMises2d | CFDEllipsoidal


# Continous Fiber Distribution Function Integration Schema
class GaussKronrodTrapezoidalIntegration(BaseXmlModel, tag="scheme", extra="forbid"):
    type: Literal["fibers-3d-gkt"] = attr(default="fibers-3d-gkt", frozen=True)
    nph: Literal[7, 11, 15, 19, 23, 27] = element(default=7)
    nth: PositiveInt = element(default=31)


class FiniteElementIntegration(BaseXmlModel, tag="scheme", extra="forbid"):
    type: Literal["fibers-3d-fei"] = attr(default="fibers-3d-fei", frozen=True)
    resolution: Literal[
        20,
        34,
        60,
        74,
        196,
        210,
        396,
        410,
        596,
        610,
        796,
        810,
        996,
        1010,
        1196,
        1210,
        1396,
        1410,
        1596,
        1610,
        1796,
    ] = element(default=1610)


class TrapezoidalRuleIntegration(BaseXmlModel, tag="scheme", extra="forbid"):
    type: Literal["fibers-2d-trapezoidal"] = attr(default="fibers-2d-trapezoidal", frozen=True)
    nth: PositiveInt = element(default=31)


IntegrationScheme: TypeAlias = GaussKronrodTrapezoidalIntegration | FiniteElementIntegration | TrapezoidalRuleIntegration


class ContinuousFiberDistribution(BaseXmlModel, tag="solid", extra="forbid"):
    type: Literal["continuous fiber distribution"] = attr(default="continuous fiber distribution", frozen=True)
    fibers: FiberModel = element(default=FiberNaturalNeoHookean(), tag="fibers")
    distribution: CFDistributionModel = element(default=CFDSpherical())
    scheme: IntegrationScheme = element(default=GaussKronrodTrapezoidalIntegration())
    mat_axis: MaterialAxisVector | None = element(default=None)


class ContinuousFiberDistributionUC(BaseXmlModel, tag="solid", extra="forbid"):
    type: Literal["continuous fiber distribution uncoupled"] = attr(default="continuous fiber distribution uncoupled", frozen=True)
    fibers: FiberModelUC = element(default=FiberToeLinearUC(), tag="fibers")
    distribution: CFDistributionModel = element(default=CFDSpherical())
    scheme: IntegrationScheme = element(default=GaussKronrodTrapezoidalIntegration())
    mat_axis: MaterialAxisVector | None = element(default=None)


# Solid Mixture
class SolidMixture(MaterialBaseNoDensity, tag="material", extra="forbid"):
    type: Literal["solid mixture"] = attr(default="solid mixture", frozen=True)
    solid_list: list[UnconstrainedMaterials | FiberModel | ContinuousFiberDistribution | EvolvingUnconstrainedMaterials] = element(
        tag="solid", default=[]
    )

    def add_solid(
        self,
        new_solid: UnconstrainedMaterials | FiberModel | ContinuousFiberDistribution | EvolvingUnconstrainedMaterials,
    ):
        self.solid_list.append(new_solid)


# Uncoupled Solid Mixture
class SolidMixtureUC(MaterialBaseNoDensity, tag="material", extra="forbid"):
    type: Literal["solid mixture"] = attr(default="uncoupled solid mixture", frozen=True)
    solid_list: list[UncoupledMaterials | FiberModelUC | ContinuousFiberDistributionUC] = element(tag="solid", default=[])

    def add_solid(self, new_solid: UncoupledMaterials | FiberModelUC | ContinuousFiberDistributionUC):
        self.solid_list.append(new_solid)


# Viscoelastic Material
class ViscoelasticMaterial(MaterialBaseNoDensity, tag="material", extra="forbid"):
    type: Literal["viscoelastic"] = attr(default="viscoelastic", frozen=True)
    g0: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    g1: MatNonNegativeFloat = element(default=MaterialParameter(text=0.0))
    g2: MatNonNegativeFloat = element(default=MaterialParameter(text=0.0))
    g3: MatNonNegativeFloat = element(default=MaterialParameter(text=0.0))
    g4: MatNonNegativeFloat = element(default=MaterialParameter(text=0.0))
    g5: MatNonNegativeFloat = element(default=MaterialParameter(text=0.0))
    g6: MatNonNegativeFloat = element(default=MaterialParameter(text=0.0))
    t1: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    t2: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    t3: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    t4: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    t5: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    t6: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    elastic: UnconstrainedMaterials | SolidMixture = element(default=NeoHookean(id=1), tag="elastic")


# Viscoelastic Material
class ViscoelasticMaterialUC(MaterialBaseNoDensity, tag="material", extra="forbid"):
    type: Literal["uncoupled viscoelastic"] = attr(default="uncoupled viscoelastic", frozen=True)
    k: MatPositiveFloat = element(default=MaterialParameter(text=10.0))
    g0: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    g1: MatNonNegativeFloat = element(default=MaterialParameter(text=0.0))
    g2: MatNonNegativeFloat = element(default=MaterialParameter(text=0.0))
    g3: MatNonNegativeFloat = element(default=MaterialParameter(text=0.0))
    g4: MatNonNegativeFloat = element(default=MaterialParameter(text=0.0))
    g5: MatNonNegativeFloat = element(default=MaterialParameter(text=0.0))
    g6: MatNonNegativeFloat = element(default=MaterialParameter(text=0.0))
    t1: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    t2: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    t3: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    t4: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    t5: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    t6: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    elastic: UncoupledMaterials | SolidMixtureUC = element(default=MooneyRivlinUC(id=1), tag="elastic")


# Prestrain
class InSituStretch(BaseXmlModel, tag="stretch", extra="forbid"):
    lc: int = attr(ge=1)
    type: Literal["map", "math"] | None = attr(default=None)
    text: str | float


class PrestrainInSituStretch(BaseXmlModel, tag="prestrain", extra="forbid"):
    type: Literal["in-situ stretch"] = attr(default="in-situ stretch", frozen=True)
    stretch: InSituStretch = element()
    ischoric: Literal[0, 1] = element(default=1)


class PrestrainRamp(BaseXmlModel, tag="ramp", extra="forbid"):
    lc: int = attr(ge=1)
    text: float = 1.0


class PrestrainGradient(BaseXmlModel, tag="prestrain", extra="forbid"):
    type: Literal["prestrain gradient"] = attr(default="prestrain gradient", frozen=True)
    ramp: PrestrainRamp = element()
    F0: MatStringFloatVec9 = element(default=MaterialParameter(text="1.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,1.0"))


class PrestrainElastic(MaterialBaseNoDensity, tag="material", extra="forbid"):
    type: Literal["prestrain elastic"] = attr(default="prestrain elastic", frozen=True)
    elastic: UnconstrainedMaterials | SolidMixture = element(default=TransIsoMooneyRivlin(id=1))
    prestrain: PrestrainInSituStretch | PrestrainGradient = element()


class PrestrainElasticUC(MaterialBaseNoDensity, tag="material", extra="forbid"):
    type: Literal["prestrain elastic"] = attr(default="prestrain elastic", frozen=True)
    elastic: UncoupledMaterials | SolidMixtureUC = element(default=TransIsoMooneyRivlin(id=1))
    prestrain: PrestrainInSituStretch | PrestrainGradient = element()


class ConstantIsoPerm(BaseXmlModel, tag="permeability", extra="forbid"):
    type: Literal["perm-const-iso"] = attr(default="perm-const-iso", frozen=True)
    perm: MatPositiveFloat = element(default=MaterialParameter(text=1e-3))


class ExponentialIsoPerm(BaseXmlModel, tag="permeability", extra="forbid"):
    type: Literal["perm-exp-iso"] = attr(default="perm-exp-iso", frozen=True)
    perm: MatPositiveFloat = element(default=MaterialParameter(text=1e-3))
    M: MatPositiveFloat = element(default=MaterialParameter(text=1.5))


class HolmesMowPerm(BaseXmlModel, tag="permeability", extra="forbid"):
    type: Literal["perm-Holmes-Mow"] = attr(default="perm-Holmes-Mow", frozen=True)
    perm: MatPositiveFloat = element(default=MaterialParameter(text=1e-3))
    M: MatNonNegativeFloat = element(default=MaterialParameter(text=1.5))
    alpha: MatNonNegativeFloat = element(default=MaterialParameter(text=2.0))


class RefIsoPerm(BaseXmlModel, tag="permeability", extra="forbid"):
    type: Literal["perm-ref-iso"] = attr(default="perm-ref-iso", frozen=True)
    perm0: MatPositiveFloat = element(default=MaterialParameter(text=1e-3))
    perm1: MatPositiveFloat = element(default=MaterialParameter(text=5e-3))
    perm2: MatPositiveFloat = element(default=MaterialParameter(text=2e-3))
    M: MatNonNegativeFloat = element(default=MaterialParameter(text=1.5))
    alpha: MatNonNegativeFloat = element(default=MaterialParameter(text=2.0))


class RefOrthoPerm(BaseXmlModel, tag="permeability", extra="forbid"):
    type: Literal["perm-ref-ortho"] = attr(default="perm-ref-ortho", frozen=True)
    perm0: MatPositiveFloat = element(default=MaterialParameter(text=1e-3))
    perm1: MatStringFloatVec3 = element(default=MaterialParameter(text="0.01,0.02,0.03"))
    perm2: MatStringFloatVec3 = element(default=MaterialParameter(text="0.001,0.002,0.003"))
    M0: MatNonNegativeFloat = element(default=MaterialParameter(text=0.5))
    M: MatStringFloatVec3 = element(default=MaterialParameter(text="1.5,2.0,2.5"))
    alpha0: MatNonNegativeFloat = element(default=MaterialParameter(text=2.0))
    alpha: MatStringFloatVec3 = element(default=MaterialParameter(text="2.0,2.5,3.0"))


class RefTransIsoPerm(BaseXmlModel, tag="permeability", extra="forbid"):
    type: Literal["perm-ref-trans-iso"] = attr(default="perm-ref-trans-iso", frozen=True)
    perm0: MatPositiveFloat = element(default=MaterialParameter(text=2e-3))
    perm1A: MatPositiveFloat = element(default=MaterialParameter(text=1e-2))
    perm2A: MatPositiveFloat = element(default=MaterialParameter(text=1e-2))
    perm1T: MatPositiveFloat = element(default=MaterialParameter(text=1e-3))
    perm2T: MatPositiveFloat = element(default=MaterialParameter(text=5e-2))
    M0: MatNonNegativeFloat = element(default=MaterialParameter(text=1.0))
    MA: MatNonNegativeFloat = element(default=MaterialParameter(text=0.5))
    MT: MatNonNegativeFloat = element(default=MaterialParameter(text=1.5))
    alpha0: MatNonNegativeFloat = element(default=MaterialParameter(text=1.0))
    alphaA: MatNonNegativeFloat = element(default=MaterialParameter(text=0.5))
    alphaT: MatNonNegativeFloat = element(default=MaterialParameter(text=2.0))


def tension_only_nonlinear_spring(slack: float, e0: float, k: float) -> str:
    """
    Blankevoort 1991 ligament model

    :param slack: engineering strain representing amount of slack (will not produce force until slack strain is reached)
    :param e0: engineering strain where fibers are fully straigtened (start of linear region)
    :param k: elastic modulus of linear region

    :return: A string expression of fiber force equation compatible with FEBio math interpreter
    """

    toe_region = f"H(x - {slack:.5f}) * ({0.5 / e0 * k:.5f} * (x - {slack:.5f}) ^ 2) * (1.0 - H(x -{slack + e0:.5f}))"
    linear_region = f"H(x - {slack + e0:.5f}) * {k:.5f} * (x - {slack} - {e0 / 2.0:.5f})"

    return " + ".join([toe_region, linear_region])


PermeabilityType = ConstantIsoPerm | ExponentialIsoPerm | HolmesMowPerm | RefIsoPerm | RefOrthoPerm | RefTransIsoPerm


class SolventSupply(BaseXmlModel, tag="solvent_supply", extra="forbid"):
    type: Literal["Starling"] = attr(default="Starling", frozen=True)
    kp: MatPositiveFloat = element(default=0.001)
    pv: MatPositiveFloat = element(default=0.1)


class BiphasicMaterial(MaterialBaseNoDensity, tag="material", extra="forbid"):
    type: Literal["biphasic"] = attr(default="biphasic", frozen=True)
    fluid_density: MatPositiveFloat = element(default=MaterialParameter(text=1.0))
    phi0: MatPositiveFloat = element(default=MaterialParameter(text=0.2))
    tau: NonNegativeFloat | None = element(default=None)
    solid: UnconstrainedMaterials | UncoupledMaterials | SolidMixture | SolidMixtureUC = element(default=NeoHookean(id=1), tag="solid")
    permeability: PermeabilityType = element(default=ConstantIsoPerm())
    solvent_supply: SolventSupply | None = element(default=None)


MaterialType = (
    UnconstrainedMaterials
    | EvolvingUnconstrainedMaterials
    | UncoupledMaterials
    | RigidBody
    | SolidMixture
    | SolidMixtureUC
    | BiphasicMaterial
    | ViscoelasticMaterial
    | ViscoelasticMaterialUC
)


class Material(BaseXmlModel, validate_assignment=True):
    all_materials: list[MaterialType] = element(tag="material", default=[])

    def add_material(self, material: MaterialType):
        material.id = len(self.all_materials) + 1
        self.all_materials.append(material)
