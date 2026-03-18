import meshio

import pyfebio as feb

# read a 27 node hex mesh in gmsh format
from_gmsh = meshio.gmsh.read("../../assets/gmsh/hex27_contact.msh")
# translate gmsh meshio object to an febio mesh
mesh = feb.mesh.translate_meshio(from_gmsh, node_sets_from_surfaces=True)

# initialize and febio model with default settings
my_model = feb.model.Model(mesh_=mesh)

# loop over the mesh Elements (parts) and assign materials
# and solid domains
for part in my_model.mesh_.elements:
    mat = feb.material.NeoHookean(
        name=part.name,
        E=feb.material.MaterialParameter(text=1.0),
        v=feb.material.MaterialParameter(text=0.3),
    )
    my_model.material_.add_material(mat)
    my_model.meshdomains_.add_solid_domain(feb.meshdomains.SolidDomain(name=part.name, mat=part.name))

# add a surface pair for the contact definition
my_model.mesh_.add_surface_pair(feb.mesh.SurfacePair(name="contact", primary="bottom-box-top", secondary="top-box-bottom"))

# fix the bottom nodes of the bottom box in space
my_model.boundary_.add_bc(feb.boundary.BCZeroDisplacement(node_set="bottom-box-bottom", x_dof=1, y_dof=1, z_dof=1))

# fix the top nodes of the top box in the y dimension
my_model.boundary_.add_bc(feb.boundary.BCZeroDisplacement(node_set="top-box-top", x_dof=0, y_dof=1, z_dof=0))

# move the top nodes of the top box in the the dimension
my_model.boundary_.add_bc(
    feb.boundary.BCPrescribedDisplacement(node_set="top-box-top", dof="z", value=feb.boundary.Value(lc=1, text=-0.15))
)

# move the top nodes of the top box in the x dimension
my_model.boundary_.add_bc(feb.boundary.BCPrescribedDisplacement(node_set="top-box-top", dof="x", value=feb.boundary.Value(lc=1, text=0.3)))
# add a sliding contact definition. enforce it with augmented lagrangian multiplier
my_model.contact_.add_contact(
    feb.contact.SlidingElastic(name="sliding_contact", surface_pair="contact", auto_penalty=1, laugon="AUGLAG", two_pass=1)
)

# load curve controlling the top nodes displacement
my_model.loaddata_.add_load_curve(feb.loaddata.LoadCurve(id=1, points=feb.loaddata.CurvePoints(points=["0,0", "1,1"])))

# add variables to the plotfile output
my_model.output_.add_plotfile(
    feb.output.OutputPlotfile(
        all_vars=[
            feb.output.Var(type="displacement"),
            feb.output.Var(type="contact pressure"),
            feb.output.Var(type="contact gap"),
            feb.output.Var(type="Lagrange strain"),
        ]
    )
)
# save the model to disk
my_model.save("contact.feb")
# run the model
feb.model.run_model("contact.feb")
