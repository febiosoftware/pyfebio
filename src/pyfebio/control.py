from typing import Literal

from pydantic_xml import BaseXmlModel, attr, element


class TimeStepValue(BaseXmlModel, validate_assignment=True):
    lc: int | None = attr(default=None)
    text: float = 1.0


class TimeStepper(BaseXmlModel, validate_assignment=True):
    type: Literal["default"] = attr(default="default", frozen=True)
    max_retries: int = element(default=5, ge=0)
    opt_iter: int = element(default=11, ge=0)
    dtmin: float = element(default=0.0, ge=0.0)
    dtmax: TimeStepValue = element(default=TimeStepValue())
    aggressiveness: Literal[0, 1] = element(default=0)
    cutback: float = element(default=0.5, ge=0.0, le=1.0)
    dtforce: Literal[0, 1] = element(default=0)


class LinearSolver(BaseXmlModel, validate_assignment=True):
    type: Literal["pardiso", "mkl_dss"] = attr(default="pardiso")


class BFGSMethod(BaseXmlModel, validate_assignment=True):
    type: Literal["BFGS"] = attr(default="BFGS", frozen=True)
    max_ups: int = element(default=10, ge=0)
    max_buffer_size: int = element(default=0, ge=0)
    cycle_buffer: Literal[0, 1] = element(default=1)
    cmax: float = element(default=1.0e5)


class BroydenMethod(BaseXmlModel, validate_assignment=True):
    type: Literal["Broyden"] = attr(default="Broyden", frozen=True)
    max_ups: int = element(default=10, ge=0)
    max_buffer_size: int = element(default=0, ge=0)
    cycle_buffer: Literal[0, 1] = element(default=1)
    cmax: float = element(default=1.0e5)


class JFNKMethod(BaseXmlModel, validate_assignment=True):
    type: Literal["JFNK"] = attr(default="JFNK", frozen=True)
    jfnk_eps: float = element(default=1.0e-6, ge=0)


class FullNewtonMethod(BaseXmlModel, validate_assignment=True):
    type: Literal["full Newton"] = attr(default="full Newton", frozen=True)


class ModifiedNewtonMethod(BaseXmlModel, validate_assignment=True):
    type: Literal["modified Newton"] = attr(default="modified Newton", frozen=True)


QuasiNewtonMethod = BFGSMethod | BroydenMethod | JFNKMethod | FullNewtonMethod | ModifiedNewtonMethod


class _BaseSolver(BaseXmlModel, validate_assignment=True, skip_empty=True):
    """
    Class for Non-Linear Solver settings. Currently, only supporting
    "solid" and "biphasic" analyses, and direct linear solvers "pardiso"
    and "mkl_dss".

    More nuanced parameters can be added as needed.
    """

    symmetric_stiffness: Literal["symmetric", "non-symmetric", "symmetric-structure", "preferred"] = element(default="preferred")
    equation_scheme: Literal["staggered", "block"] = element(default="staggered")
    equation_order: Literal["default", "reverse", "febio2"] = element(default="default")
    optimize_bw: Literal[0, 1] = element(default=0)
    lstol: float = element(default=0.9, ge=0)
    lsmin: float = element(default=0.01, gt=0)
    lsiter: int = element(default=5, ge=0)
    ls_check_jacobians: Literal[0, 1] = element(default=0)
    max_refs: int = element(default=15, ge=0)
    check_zero_diagonal: Literal[0, 1] = element(default=0)
    zero_diagonal_tol: Literal[0] | float = element(default=0, ge=0)
    force_partition: Literal[0, 1] = element(default=0)
    reform_each_time_step: Literal[0, 1] = element(default=1)
    reform_augment: Literal[0, 1] = element(default=0)
    diverge_reform: Literal[0, 1] = element(default=1)
    min_residual: float = element(default=1e-20, gt=0.0)
    max_residual: Literal[0] | float = element(default=0, ge=0)
    qn_method: QuasiNewtonMethod = element(default=BFGSMethod())
    linear_solver: LinearSolver = element(default=LinearSolver())


class SolidSolver(_BaseSolver, validate_assignment=True, skip_empty=True):
    type: Literal["solid"] = attr(default="solid", frozen=True)
    dtol: float = element(default=0.001, gt=0)
    etol: float = element(default=0.01, ge=0)
    rtol: float = element(default=0, ge=0)
    rhoi: float = element(default=-2)
    alpha: float = element(default=1)
    beta: float = element(default=0.25)
    gamma: float = element(default=0.5)
    logSolve: Literal[0, 1] = element(default=0)
    arc_length: int = element(default=0)
    arc_length_scale: float = element(default=0)


class BiphasicSolver(_BaseSolver, validate_assignment=True, skip_empty=True):
    type: Literal["biphasic"] = attr(default="biphasic", frozen=True)
    dtol: float = element(default=0.001, gt=0)
    etol: float = element(default=0.01, ge=0)
    rtol: float = element(default=0, ge=0)
    ptol: float = element(default=0.01, ge=0)
    ctol: float = element(default=0, ge=0)
    mixed_formulation: Literal[0, 1] = element(default=0)


class MultiphasicSolver(_BaseSolver, validate_assignment=True, skip_empty=True):
    type: Literal["multiphasic"] = attr(default="multiphasic", frozen=True)
    dtol: float = element(default=0.001, gt=0)
    etol: float = element(default=0.01, ge=0)
    rtol: float = element(default=0, ge=0)
    ptol: float = element(default=0.01, ge=0)
    ctol: float = element(default=0.01, ge=0)
    force_positive_concentrations: Literal[0, 1] = element(default=1)


class MultiphasicFSISolver(_BaseSolver, validate_assignment=True, skip_empty=True):
    type: Literal["multiphasic"] = attr(default="multiphasic", frozen=True)
    dtol: float = element(default=0.001, gt=0)
    vtol: float = element(default=0.001, gt=0)
    ftol: float = element(default=0.001, gt=0)
    etol: float = element(default=0.01, ge=0)
    rtol: float = element(default=0.001, ge=0)
    ptol: float = element(default=0.01, ge=0)
    ctol: float = element(default=0.01, ge=0)
    rhoi: float = element(default=0, ge=0)
    predictor: Literal[0, 1] = element(default=0)
    min_volume_ratio: float = element(default=0, ge=0)
    order: Literal[1, 2] = element(default=2)
    force_positive_concentrations: Literal[0, 1] = element(default=1)


class ExplicitSolver(BaseXmlModel, validate_assignment=True, skip_empty=True):
    type: Literal["explicit-solid"] = attr(default="explicit-solid", frozen=True)
    mass_lumping: Literal[1, 2] = element(default=1)
    dyn_damping: Literal[1] | float = element(default=1)
    mixed_formulation: Literal[0, 1] | None = element(default=None, frozen=True)


class CGSolidSolver(BaseXmlModel, validate_assignment=True, skip_empty=True):
    type: Literal["CG-solid"] = attr(default="CG-solid", frozen=True)
    symmetric_stiffness: Literal["symmetric", "non-symmetric", "symmetric-structure", "preferred"] = element(default="non-symmetric")
    equation_scheme: Literal["staggered", "block"] = element(default="staggered")
    equation_order: Literal["default", "reverse", "febio2"] = element(default="default")
    optimize_bw: Literal[0, 1] = element(default=0)
    lstol: float = element(default=0.9, ge=0)
    lsmin: float = element(default=1e-15, gt=0)
    lsiter: int = element(default=10, ge=0)
    dtol: float = element(default=1e-6, gt=0)
    etol: float = element(default=0.01, ge=0)
    rtol: float = element(default=0, ge=0)
    min_residual: float = element(default=1e-20, gt=0.0)
    beta: float = element(default=0.25)
    gamma: float = element(default=0.5)
    cgmethod: Literal[0, 1] = element(default=0)
    preconditioner: Literal[0, 1] = element(default=0)


class Control(BaseXmlModel, tag="Control", validate_assignment=True):
    analysis: Literal["STATIC", "DYNAMIC", "STEADY-STATE", "TRANSIENT"] = element(default="STATIC")
    time_steps: int = element(default=10)
    step_size: float = element(default=0.1)
    plot_zero_state: Literal[0, 1] = element(default=0)
    plot_range: str = element(default="0,-1")
    plot_level: Literal["PLOT_NEVER", "PLOT_MAJOR_ITRS", "PLOT_MINOR_ITRS", "PLOT_MUST_POINTS"] = element(default="PLOT_MAJOR_ITRS")
    output_level: Literal["OUTPUT_NEVER", "OUTPUT_MAJOR_ITRS", "OUTPUT_MINOR_ITRS", "OUTPUT_MUST_POINTS", "OUTPUT_FINAL"] = element(
        default="OUTPUT_MAJOR_ITRS"
    )
    plot_stride: int = element(default=1)
    output_stride: int = element(default=1)
    adaptor_re_solve: int = element(default=1)
    time_stepper: TimeStepper | None = element(default=TimeStepper())
    solver: SolidSolver | BiphasicSolver | MultiphasicSolver | ExplicitSolver | CGSolidSolver = element(default=SolidSolver())
