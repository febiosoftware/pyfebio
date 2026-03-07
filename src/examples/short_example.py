import pyfebio

# Instantiate a model tree with default values
# This contains empty mesh, material, loads, boundary, etc. sections
my_model = pyfebio.model.Model()

# Let's create a single hex8 element explicitly
# Normally, you would use the meshio functions to import
nodes_list = [
    [0.0, 0.0, 0.0],
    [1.0, 0.0, 0.0],
    [1.0, 1.0, 0.0],
    [0.0, 1.0, 0.0],
    [0.0, 0.0, 1.0],
    [1.0, 0.0, 1.0],
    [1.0, 1.0, 1.0],
    [0.0, 1.0, 1.0],
]

elements_list = [[1, 2, 3, 4, 5, 6, 7, 8]]

# Add Nodes to an pyfebio.Nodes object
nodes = pyfebio.mesh.Nodes(name="nodes")
for i, node in enumerate(nodes_list):
    nodes.add_node(pyfebio.mesh.Node(id=i + 1, text=",".join(map(str, node))))

# Add Elements to an pyfebio.Elements object
elements = pyfebio.mesh.Elements(name="box", type="hex8")
for i, element in enumerate(elements_list):
    elements.add_element(pyfebio.mesh.Hex8Element(id=i + 1, text=",".join(map(str, element))))

# Append nodes and elements to the model's mesh section
my_model.mesh_.nodes += (nodes,)
my_model.mesh_.elements.append(elements)

# Let's make a node set for top and bottom
bottom_nodes = [1, 2, 3, 4]
top_nodes = [5, 6, 7, 8]
top_node_set = pyfebio.mesh.NodeSet(name="top", text=",".join(map(str, top_nodes)))
bottom_node_set = pyfebio.mesh.NodeSet(name="bottom", text=",".join(map(str, bottom_nodes)))

# Append the node sets to the model's mesh section
my_model.mesh_.node_sets.append(top_node_set)
my_model.mesh_.node_sets.append(bottom_node_set)

# We need a material
# the use of pyfebio.material.MaterialParameter is our solution
# to handle mapped, math, or directly specified values
my_material = pyfebio.material.CoupledMooneyRivlin(
    id=1,
    name="cartilage",
    c1=pyfebio.material.MaterialParameter(text=10.0),
    c2=pyfebio.material.MaterialParameter(text=1.0),
    k=pyfebio.material.MaterialParameter(text=1000.0),
)

# Define a solid domain for the box to assign the material
solid_domain = pyfebio.meshdomains.SolidDomain(name="box", mat="cartilage")

# add the solid domain
my_model.meshdomains_.add_solid_domain(solid_domain)

# add the material
my_model.material_.add_material(my_material)

# Fix the bottom nodes (1 means BC DoF is active)
fixed_bottom = pyfebio.boundary.BCZeroDisplacement(node_set="bottom", x_dof=1, y_dof=1, z_dof=1)

# Displace the top nodes in z
# We need to create a boundary.Value object that references a load curve
displacement_value = pyfebio.boundary.Value(lc=1, text=-0.2)
move_top = pyfebio.boundary.BCPrescribedDisplacement(node_set="top", dof="z", value=displacement_value)

# Add boundary conditions
my_model.boundary_.add_bc(fixed_bottom)
my_model.boundary_.add_bc(move_top)

# Now, create the loadcurve 1 we referenced
curve_points = pyfebio.loaddata.CurvePoints(points=["0.0,0.0", "1.0,1.0"])
load_curve1 = pyfebio.loaddata.LoadCurve(id=1, points=curve_points)
# And, add it to model
my_model.loaddata_.add_load_curve(load_curve1)

# Save the model to disk
my_model.save("my_model.feb")

# And run it
pyfebio.model.run_model("my_model.feb")
