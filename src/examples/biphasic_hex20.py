from meshio.gmsh import read

import pyfebio as feb

# import mesh from gmsh format
from_gmsh = read("../../assets/gmsh/hex20.msh")
# translate meshio mesh to febio mesh
mesh = feb.mesh.translate_meshio(from_gmsh, node_sets_from_surfaces=True)

# initialize a biphasic febio modelk
my_model = feb.model.BiphasicModel(mesh_=mesh)
assert my_model.control_ is not None
my_model.control_.step_size = 0.1
my_model.control_.time_stepper = feb.control.TimeStepper(dtmax=feb.control.TimeStepValue(text=1.0))

# loop over Elements (parts) and assign biphasic materials
# and also assign solid domains
for i, part in enumerate(my_model.mesh_.elements):
    mat = feb.material.BiphasicMaterial(
        name=part.name,
        solid=feb.material.NeoHookean(),
        permeability=feb.material.ConstantIsoPerm(perm=feb.material.MaterialParameter(text=1e-3 * (i + 1))),
    )
    my_model.material_.add_material(mat)
    my_model.meshdomains_.add_solid_domain(feb.meshdomains.SolidDomain(name=part.name, mat=part.name))

# fix the bottom nodes in space
fix_bottom = my_model.boundary_.add_bc(feb.boundary.BCZeroDisplacement(node_set="bottom", x_dof=1, y_dof=1, z_dof=1))

# set zero fluid pressure bc on bottom nodes to allow for free-draining
drain_bottom = my_model.boundary_.add_bc(feb.boundary.BCZeroFluidPressure(node_set="bottom"))

# set zero fluid pressure bc on top nodes to allow for free-draining
drain_top = my_model.boundary_.add_bc(feb.boundary.BCZeroFluidPressure(node_set="top"))

# displace the top nodes by -0.5 mm in z
move_top = my_model.boundary_.add_bc(
    feb.boundary.BCPrescribedDisplacement(node_set="top", dof="z", value=feb.boundary.Value(lc=1, text=-0.5))
)

# load curve to apply displacement
my_model.loaddata_.add_load_curve(feb.loaddata.LoadCurve(id=1, points=feb.loaddata.CurvePoints(points=["0.0,0.0", "0.1,1.0", "10.0,1.0"])))

# add some additonial variables to plotfile
my_model.output_.add_plotfile(
    feb.output.OutputPlotfile(
        all_vars=[
            feb.output.Var(type="displacement"),
            feb.output.Var(type="effective fluid pressure"),
            feb.output.Var(type="nodal fluid flux"),
            feb.output.Var(type="Lagrange strain"),
        ]
    )
)

# save the model to disk
my_model.save("biphasic_hex20.feb")
# run the model
feb.model.run_model("biphasic_hex20.feb")
