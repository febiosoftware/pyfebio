import meshio

import pyfebio as feb

# import an 8 node hex mesh in gmsh format
from_gmsh = meshio.gmsh.read("../../assets/gmsh/hex8.msh")

# convert the meshio object to febio mesh
mesh = feb.mesh.translate_meshio(from_gmsh, node_sets_from_surfaces=True)

# crete a base febio model but override the control section to have constant time step
my_model = feb.model.Model(mesh_=mesh, control_=feb.control.Control(time_steps=10, step_size=0.1, time_stepper=None))

# loop over all Elements in the mesh and assign materials and solid domains
for i, part in enumerate(my_model.mesh_.elements):
    mat = feb.material.NeoHookean(
        name=part.name,
        E=feb.material.MaterialParameter(text=10.0 * (i + 1)),
        v=feb.material.MaterialParameter(text=0.3),
    )
    my_model.material_.add_material(mat)
    my_model.meshdomains_.add_solid_domain(feb.meshdomains.SolidDomain(name=part.name, mat=part.name))

# fix the bottom nodes
fix_bottom = my_model.boundary_.add_bc(feb.boundary.BCZeroDisplacement(node_set="bottom", x_dof=1, y_dof=1, z_dof=1))

# displace the top nodes in z by -0.5 mm
move_top = my_model.boundary_.add_bc(
    feb.boundary.BCPrescribedDisplacement(node_set="top", dof="z", value=feb.boundary.Value(lc=1, text=0.5))
)

# load curve controlling the top nodes displacement
my_model.loaddata_.add_load_curve(feb.loaddata.LoadCurve(id=1, points=feb.loaddata.CurvePoints(points=["0.0,0.0", "1.0,1.0"])))

# creat are mesh adaptor to refine the mesh based
# on the stress error criterion
adaptor = feb.meshadaptor.HexRefineAdaptor(
    elem_set="bottom-layer",
    max_iters=1,
    max_elements=10000,
    criterion=feb.meshadaptor.RelativeErrorCriterion(error=0.01, data=feb.meshadaptor.StressCriterion()),
)
my_model.meshadaptor_.add_adaptor(adaptor)

# we have to add the stress error output to the plotfile so our mesh
# adaptor works
my_model.output_.add_plotfile(
    feb.output.OutputPlotfile(
        all_vars=[
            feb.output.Var(type="displacement"),
            feb.output.Var(type="stress error"),
        ]
    )
)

# save our madel to disk
my_model.save("mesh_adapt.feb")
# run the model
feb.model.run_model("mesh_adapt.feb")
