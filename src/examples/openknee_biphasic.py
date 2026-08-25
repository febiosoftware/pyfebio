from pathlib import Path

import meshio

import pyfebio as feb

# Cartilage thickness (mm)
CARTILAGE_THICKNESS = 1.5

# Solid Phase Material Properties
# EFD NeoHookean
E = 1.0
v = 0.15
fiber_ksi = "10.0,10.0,10.0"
fiber_beta = "2.0,2.0,2.0"

# Fluid Phase Material Properties
# Constant Isotropic Permeability
perm = 1e-3

# Loading
FORCE = -500.0

# Time Parameters
RAMP_TIME = 1.0
HOLD_TIME = 600.0
INITIAL_STEP_SIZE = 0.01

# Must Point spacing increases by this ratio for each point during relaxation phase
INITIAL_MUST_POINT_RELAX_STEP = 1.0
MUST_POINT_RELAX_RATIO = 1.3

assert MUST_POINT_RELAX_RATIO > 1.0, "MUST_POINT_RELAX_RATIO must be greater than 1.0"
assert INITIAL_MUST_POINT_RELAX_STEP > 0.0, "INITIAL_MUST_POINT_RELAX_STEP must be greater than 0.0"

# Relative path to where the mesh files are
base_dir = Path(__file__).parent.joinpath("../../assets/openknee")

# Import the meshes using meshio and assemble into one mesh
element_offset = 0
node_offset = 0
assembled_mesh = feb.mesh.Mesh()
for meshfile in ("fmc.msh", "tbc-l.msh", "tbc-m.msh"):
    meshfile = base_dir.joinpath(meshfile)
    meshobj = meshio.gmsh.read(meshfile)

    febmesh = feb.mesh.translate_meshio(
        meshobj,
        nodeoffset=node_offset,
        elementoffset=element_offset,
        shell_sets=["cartilage"],
        nodes_name=meshfile.stem,
    )

    element_offset += febmesh.elements[-1].all_elements[-1].id
    node_offset += febmesh.nodes[-1].all_nodes[-1].id
    for node in febmesh.nodes:
        assembled_mesh.add_node_domain(node)

    for i, element in enumerate(febmesh.elements):
        if i > 0:
            element.name = f"{meshfile.stem}_{i + 2}"
        else:
            element.name = meshfile.stem
        assembled_mesh.add_element_domain(element)

# Part lists for boundary conditions and contact definition later
assembled_mesh.add_part_list(feb.mesh.PartList(name="fmc_list", text="fmc"))
assembled_mesh.add_part_list(feb.mesh.PartList(name="tbc", text="tbc-l,tbc-m"))


## Instatiate a BiphasicModel
# -------------------------------

# mixed_formulation = 1 makes solid phase shape functions quadratic,
#      but fluid phase shape functions linear. This demonstrated better behavior
# ls_check_jacobians = 1 does not abort if a negative Jacobian is detected during
#      the line search. Often the line search step adjustment can overcome this.
# BroydenMethod() quasi-Newton method for solving the nonlinear system due to
#      having a non-symmetric stiffness matrix

model = feb.model.BiphasicModel(
    mesh_=assembled_mesh,
    control_=feb.control.Control(
        analysis="TRANSIENT",
        solver=feb.control.BiphasicSolver(mixed_formulation=1, ls_check_jacobians=1, qn_method=feb.control.BroydenMethod()),
        step_size=INITIAL_STEP_SIZE,
        time_steps=int((HOLD_TIME + RAMP_TIME) / INITIAL_STEP_SIZE + 0.5),
        time_stepper=feb.control.TimeStepper(dtmax=feb.control.TimeStepValue(lc=1)),
        plot_level="PLOT_MUST_POINTS",
    ),
)
# ----------------------------------


## Material Definition
# ----------------------------------
# Loop over Elements() and assign materials
for i, element in enumerate(model.mesh_.elements[1:3]):
    solid = feb.material.EllipsoidalFiberDistributionNeoHookean(
        E=feb.material.MaterialParameter(text=E),
        v=feb.material.MaterialParameter(text=v),
        ksi=feb.material.MaterialParameter(text=fiber_ksi),
        beta=feb.material.MaterialParameter(text=fiber_beta),
    )

    mat = feb.material.BiphasicMaterial(
        name=element.name,
        id=i + 1,
        permeability=feb.material.ConstantIsoPerm(
            perm=feb.material.MaterialParameter(text=perm),
        ),
        solid=solid,
    )
    model.material_.add_material(mat)
    model.meshdomains_.add_shell_domain(
        feb.meshdomains.ShellDomain(name=element.name, mat=element.name, shell_thickness=CARTILAGE_THICKNESS)
    )

# Assign a rigid body material to the femoral cartilage
# Note material properties and thicknesses are used when
# calculating the auto_penalty for contact
mat = feb.material.RigidBody(
    name="fmc",
    id=3,
    center_of_mass="0.0,0.0,0.0",
    E=feb.material.MaterialParameter(text=E * 5.0),
    v=feb.material.MaterialParameter(text=v),
)
model.material_.add_material(mat)
model.meshdomains_.add_shell_domain(feb.meshdomains.ShellDomain(name="fmc", mat="fmc", shell_thickness=CARTILAGE_THICKNESS))
# ----------------------------------

# Fix bottom nodes of tibial cartilage shells in space
model.boundary_.add_bc(feb.boundary.BCZeroShellDisplacement(node_set="@part_list:tbc", sx_dof=1, sy_dof=1, sz_dof=1))

# Fix the fmc rigid body in all DoFs but z
model.rigid_.add_rigid_bc(feb.rigid.RigidFixed(rb="fmc", Rx_dof=1, Ry_dof=1, Rz_dof=0, Ru_dof=1, Rw_dof=1, Rv_dof=1))

# Apply a compressive force to the fmc rigid body in the z direction
model.rigid_.add_rigid_load(feb.rigid.RigidForceLoad(rb="fmc", dof="Rz", value=feb.rigid.Value(lc=2, text=FORCE), load_type=1))


## Add Biphasic Sliding Contact Constraint
# -----------------------------------------

# Surface Pair for Biphasic Sliding Contact Constraint
model.mesh_.add_surface_pair(feb.mesh.SurfacePair(name="fmc_tbc", primary="@part_list:tbc", secondary="@part_list:fmc_list"))

# Biphasic Sliding Contact Constraint
# gaptol is fairly strict at 0.1mm
# this yielded better behavior than softer contact enforcement
model.contact_.add_contact(
    feb.contact.SlidingBiphasic(
        surface_pair="fmc_tbc",
        auto_penalty=1,
        laugon="AUGLAG",
        gaptol=0.1,
        tolerance=0,
        symmetric_stiffness=0,
        search_radius=2.0,
        two_pass=1,
    )
)
# -----------------------------------------

# Load Curves
# -----------------------------------------

# Must Point Load Curve Definition
must_points = [f"{RAMP_TIME},{RAMP_TIME}"]
elapsed_time = RAMP_TIME
step = INITIAL_MUST_POINT_RELAX_STEP
elapsed_time += step
terminate = 1
while terminate >= 0:
    must_points.append(f"{elapsed_time},{step}")
    step *= MUST_POINT_RELAX_RATIO
    elapsed_time += step
    if elapsed_time > RAMP_TIME + HOLD_TIME:
        elapsed_time = RAMP_TIME + HOLD_TIME
        terminate -= 1


model.loaddata_.add_load_curve(
    feb.loaddata.LoadCurve(id=1, interpolate="STEP", extend="CONSTANT", points=feb.loaddata.CurvePoints(points=must_points))
)

# Force Load Curve Definition
model.loaddata_.add_load_curve(
    feb.loaddata.LoadCurve(
        id=2,
        interpolate="LINEAR",
        extend="CONSTANT",
        points=feb.loaddata.CurvePoints(points=["0.0,0.0", f"{RAMP_TIME},1.0", f"{RAMP_TIME + HOLD_TIME},1.0"]),
    )
)
# -----------------------------------------

# Requested Plot Variables
model.output_.add_plotfile(
    feb.output.OutputPlotfile(
        all_vars=[
            feb.output.Var(type="shell strain"),
            feb.output.Var(type="stress"),
            feb.output.Var(type="shell relative volume"),
            feb.output.Var(type="contact pressure"),
            feb.output.Var(type="contact gap"),
            feb.output.Var(type="effective fluid pressure"),
            feb.output.Var(type="fluid flux"),
            feb.output.Var(type="displacement"),
        ]
    )
)


# Save and run the model
model.save("openknee_biphasic.feb")
_ = feb.model.run_model(filepath="openknee_biphasic.feb")
