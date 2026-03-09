from typing import Literal

from pydantic_xml import BaseXmlModel, attr, element

from ._types import StringFloatVec2, StringUIntVec


class MaxVariableCriterion(BaseXmlModel, tag="criterion"):
    type: Literal["max_variable"] = attr(default="max_variable", frozen=True)
    dof: int = element(default=-1)


class ElementSelectionCriterion(BaseXmlModel, tag="criterion"):
    type: Literal["element_selection"] = attr(default="element_selection", frozen=True)
    element_list: StringUIntVec = element()


class ContactGapCriterion(BaseXmlModel, tag="criterion"):
    type: Literal["contact gap"] = attr(default="contact gap", frozen=True)
    gap: float = element(default=0.0)


class StressCriterion(BaseXmlModel, tag="criterion"):
    type: Literal["stress"] = attr(default="stress", frozen=True)
    metric: Literal[0, 1] = element(default=0, description="0=effective stress, 1=max principal stress")


class MathCriterion(BaseXmlModel, tag="criterion"):
    type: Literal["math"] = attr(default="math", frozen=True)
    math: str = element(default="1")


class DamageCriterion(BaseXmlModel, tag="criterion"):
    type: Literal["damage"] = attr(default="damage", frozen=True)
    damage: float = element(default=0.0)


class MinMaxFilterCriterion(BaseXmlModel, tag="criterion"):
    type: Literal["min-max filter"] = attr(default="min-max filter", frozen=True)
    min: float = element(default=-1e37)
    max: float = element(default=1e37)
    clamp: Literal[0, 1] = element(default=0)
    data: ContactGapCriterion | StressCriterion | DamageCriterion | MathCriterion = element(default=StressCriterion(), tag="data")


class RelativeErrorCriterion(BaseXmlModel, tag="criterion"):
    type: Literal["relative error"] = attr(default="relative error", frozen=True)
    error: Literal[0] | float = element(default=0)
    data: ContactGapCriterion | StressCriterion | DamageCriterion | MathCriterion = element(default=StressCriterion(), tag="data")


CriterionType = (
    MaxVariableCriterion
    | ElementSelectionCriterion
    | ContactGapCriterion
    | StressCriterion
    | MathCriterion
    | DamageCriterion
    | MinMaxFilterCriterion
    | RelativeErrorCriterion
)


class MMGStepSizeFunction(BaseXmlModel, tag="size_function"):
    type: Literal["step"] = attr(default="step", frozen=True)
    x0: float = element(default=0.0)
    left_val: float = element(default=0.0)
    right_val: float = element(default=1.0)


class MMGConstantSizeFunction(BaseXmlModel, tag="size_function"):
    type: Literal["const"] = attr(default="const", frozen=True)
    value: float = element(default=0.0)


class MMGLinearRampSizeFunction(BaseXmlModel, tag="size_function"):
    type: Literal["linear ramp"] = attr(default="linear ramp", frozen=True)
    slope: float = element(default=1.0)
    intercept: float = element(default=0.0)


class MMGMathSizeFunction(BaseXmlModel, tag="size_function"):
    type: Literal["math"] = attr(default="math", frozen=True)
    math: str = element(default="1")


class CurvePoints(BaseXmlModel, tag="points"):
    type: Literal["curve"] = attr(default="curve", frozen=True)
    pt: list[StringFloatVec2] = element(default=["0,0.25", "1,1"])


class MMGPointSizeFunction(BaseXmlModel, tag="size_function"):
    type: Literal["point"] = attr(default="point", frozen=True)
    interpolate: Literal["linear", "smooth", "step"] = element(default="linear")
    extend: Literal["constant", "extrapolate", "repeat", "repeat offset"] = element(default="constant")
    points: CurvePoints = element(default=CurvePoints())


MMGSizeFunctionType = MMGStepSizeFunction | MMGConstantSizeFunction | MMGLinearRampSizeFunction | MMGMathSizeFunction | MMGPointSizeFunction


class ErosionAdaptor(BaseXmlModel, tag="mesh_adaptor"):
    type: Literal["erosion"] = attr(default="erosion", frozen=True)
    elem_set: str | None = attr(default=None)
    max_iters: int = element(default=1)
    max_elements: int = element(default=3)
    remove_islands: Literal[0, 1] = element(default=0)
    sort: Literal[0, 1] = element(default=1)
    erode_surfaces: Literal["no", "yes", "grow", "reconstruct"] = element(default="no")
    criterion: CriterionType = element(default=MinMaxFilterCriterion(data=StressCriterion()))


class MMGRemeshAdaptor(BaseXmlModel, tag="mesh_adaptor"):
    type: Literal["mmg_remesh"] = attr(default="mmg_remesh", frozen=True)
    elem_set: str | None = attr(default=None)
    max_iters: int = element(default=1)
    max_elements: int = element(default=-1)
    min_element_size: float = element(default=0.1)
    hausdorff: float = element(default=0.01)
    gradation: float = element(default=1.3, gt=1.0)
    mesh_coarsen: Literal[0, 1] = element(default=0)
    normalize_data: Literal[0, 1] = element(default=0)
    relative_size: Literal[0, 1] = element(default=1)
    criterion: CriterionType = element(default=MinMaxFilterCriterion(data=StressCriterion()))
    size_function: MMGSizeFunctionType | None = element(default=None)


class HexRefine2dAdaptor(BaseXmlModel, tag="mesh_adaptor"):
    type: Literal["hex_refine2d"] = attr(default="hex_refine2d", frozen=True)
    elem_set: str | None = attr(default=None)
    max_iters: int = element(default=1)
    max_elements: int = element(default=-1)
    max_elem_refine: int = element(default=0)
    max_value: float = element(default=0.01)
    nnc: int = element(default=8)
    nsdim: int = element(default=3)
    criterion: CriterionType = element(default=RelativeErrorCriterion(data=StressCriterion()))


class HexRefineAdaptor(BaseXmlModel, tag="mesh_adaptor"):
    type: Literal["hex_refine"] = attr(default="hex_refine", frozen=True)
    elem_set: str | None = attr(default=None)
    max_iters: int = element(default=1)
    max_elements: int = element(default=-1)
    max_elem_refine: int = element(default=0)
    max_value: float = element(default=0.01)
    nnc: int = element(default=8)
    nsdim: int = element(default=3)
    criterion: CriterionType = element(default=RelativeErrorCriterion(data=StressCriterion()))


AdaptorType = ErosionAdaptor | MMGRemeshAdaptor | HexRefine2dAdaptor | HexRefineAdaptor


class MeshAdaptor(BaseXmlModel, tag="MeshAdaptor"):
    all_adaptors: list[AdaptorType] = element(default=[])

    def add_adaptor(self, adaptor: AdaptorType):
        assert isinstance(adaptor, AdaptorType), "adaptor must be an AdaptorType"
        self.all_adaptors.append(adaptor)
