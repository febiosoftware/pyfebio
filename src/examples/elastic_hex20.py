import meshio

import pyfebio as feb

# import a mesh from gmsh format
from_gmsh = meshio.gmsh.read("../../assets/gmsh/hex20.msh")
# use translation function to convert meshio object to an febio mesh
mesh = feb.mesh.translate_meshio(from_gmsh, node_sets_from_surfaces=True)

# creat a base febio model
my_model = feb.model.Model(mesh_=mesh)

# loop over the discovered Elements (parts) and assign materials
# and solid domains
for i, part in enumerate(my_model.mesh_.elements):
    mat = feb.material.NeoHookean(
        name=part.name,
        E=feb.material.MaterialParameter(text=1.0 * (i + 1)),
        v=feb.material.MaterialParameter(text=0.3),
    )
    my_model.material_.add_material(mat)
    my_model.meshdomains_.add_solid_domain(feb.meshdomains.SolidDomain(name=part.name, mat=part.name))

# fix the bottom nodes in space
fix_bottom = my_model.boundary_.add_bc(feb.boundary.BCZeroDisplacement(node_set="bottom", x_dof=1, y_dof=1, z_dof=1))

# let's twist the top nodes by pi radians about their central z-axis
twist_top = my_model.boundary_.add_bc(
    feb.boundary.BCRigidDeformation(node_set="top", pos="0.5,0.5,0.0", rot=feb.boundary.Value(lc=1, text="0.0,0.0,3.14"))
)

# the load curve for our twist
my_model.loaddata_.add_load_curve(feb.loaddata.LoadCurve(id=1, points=feb.loaddata.CurvePoints(points=["0.0,0.0", "1.0,1.0"])))

# save the model
my_model.save("elastic_hex20.feb")

# run the model
feb.model.run_model("elastic_hex20.feb")
