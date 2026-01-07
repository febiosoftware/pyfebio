[![PyPI - Version](https://img.shields.io/pypi/v/pyfebio?logoColor=blue&color=blue)](https://pypi.org/project/pyfebio/)

## Overview

This is a Python package for generating FEBio input files and converting XPLT files to HDF5. We rely heavily on pydantic and pydantic-xml for type validation and XML serialization. Many of FEBio's features are covered, but not all.

## Getting Started

- [Installation](#installation)
- [Testing](#testing)
- [Example](#example)
- [Documentation](https://febiosoftware.github.io/pyfebio/index.html)
- [Features](#features)

## Installation

### From PyPi

With pip:

Create a virtual environment:

```bash
/path/to/compatible-python -m venv .venv
```

where /path/to/compatible-python is the path to a compatible python executable.

Activate the virtual environment:

On Linux or macOS:

```bash
source .venv/bin/activate
```

On Windows (cmd):

```bash
.\.venv\Scripts\activate.bat
```

On Windows (powershell):

```bash
.\.venv\Scripts\Activate.ps1
```

Install the package:

```bash
pip install pyfebio
```

### From Source (with uv manager)

Clone with https:

```bash
git clone https://github.com/CompOrthoBiomech/pyfebio.git
```

Or,

Clone with ssh:

```bash
git clone git@github.com:CompOrthoBiomech/pyfebio.git
```

**Install uv:**

Install uv from [here](https://docs.astral.sh/uv/getting-started/installation/)

**Sync the uv environment**

In top-level repository directory:

```bash
uv sync
```

This will create a virtual environment and install the package.

## Testing

We rely on FEBio to check our generated models are valid. Therefore, you will need to have FEBio installed and available in your PATH.

To run all the tests, execute the following command:

```bash
cd src
pytest
```

For tests that depend on running finite element simulations, you can find them in the pytest tmp_path directory, which varies by operating system.

For the latest run:

on Linux,

```bash
cd /tmp/pytest-of-[USER]/pytest-current/[TEST_FUNCTION_NAME]current
```

## Example

```python
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
my_model.mesh_.nodes.append(nodes)
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
```

![Short Example Simulation](assets/short_example.gif)


## Features

Brief overview, see module documentation for more details. Unchecked are not yet implemented.

✅ Implemented and tested

☑️ Implemented but untested

❌ Not yet implemented

- Control
  - ✅ All control settings
- Mesh Section
  - ✅ Nodes
  - ✅ Solid Elements:
     - tet4, tet10, hex8, hex20, hex27, penta6
  - ☑️ Shell Elements:
     - tri3, tri6, quad4, quad8, quad9, q4ans, q4eas
  - ☑️ Beam Elements:
     - line2, line3
  - ✅ Node, Element, Surface Sets
- MeshDomain
  - ✅ Solid Domain
  - ☑️ Shell Domain
  - ☑️ Beam Domain
  - ☑️ Granular control for integration schemes, etc.
- MeshData Section
  - ☑️ Node Data
  - ☑️ Scalar
  - ☑️ Vector3
  - ☑️ Element Data
  - ☑️ Scalar
  - ☑️ Vector3
  - ❌ Surface Data
    - ❌ Scalar
    - ❌ Vector3
- MeshAdaptor
  - ☑️ Erosion
  - ✅ MMG3d Remeshing
  - ✅ hex_refine
  - ✅ hex_refine2d
  - ☑️ Criteria
  - ☑️ element selection
  - ☑️ math
  - ☑️ min-max filter
  - ✅ relative error
  - ✅ stress
  - ☑️ contact gap
  - ☑️ damage
  - ☑️ max variable
- Material
  - ✅ Most Unconstrained Formulation Materials
  - ✅ Most Uncoupled Formulation Materials
  - ☑️ Prestrain Material
  - ☑️ Fiber models
  - ✅ Material Axis
    - ✅ Vector Definition
    - ✅ Fiber Vector
  - ☑️ Continuous Fiber Distributions
  - ☑️ Integration Schemes
  - ☑️ Element-wise, mapped, or math parameter defintion
  - ✅ Biphasic Materials
  - ✅ Viscoelastic Materials
  - ❌ Multiphasic Materials
  - ❌ Biphasic-solute Materials
  - ❌ Chemical Reactions
  - ❌ Active Contraction Materials
  - ❌ Damage Materials
  - ❌ First-order Homogenization
- Rigid
  - ☑️ Fixed Displacement and Rotation
  - ☑️ Prescribed Displacement and Rotation
  - ☑️ Precribed Rotation about Vector
  - ☑️ Prescribed Euler Rotation
  - ☑️ All Connectors
  - ☑️ Follower Loads
- Initial
  - ☑️ Initial Velocity
  - ☑️ Initial Pre-strain
- Loads
  - ☑️ Nodal Loads
  - ☑️ Traction Loads (surface)
  - ☑️ Pressure Loads (surface)
  - ☑️ Fluid Flux (surface)
  - ☑️ Fluid Pressure (surface)
- LoadData
  - ✅ Load Curves
    - ☑️ All Options
  - ☑️ PID Controllers
  - ☑️ Math Controllers
- Boundary
  - ✅ Fixed Displacement (solid)
  - ✅ Prescribed Displacement (solid)
  - ☑️ Fixed Displacement (shell)
  - ☑️ Prescribed Displacement (shell)
  - ☑️ Precribed Deformation Gradient
  - ☑️ Displacement Along Normals
  - ☑️ Fix to Rigid Body
  - ✅ Rigid Node Set Deformation (rotation about axis)
  - ✅ Zero Fluid Pressure
  - ☑️ Prescribed Fluid Pressure
- Constraints
  - ☑️ Symmetry Plane
  - ☑️ Prestrain
  - ☑️ In-Situ Stretch
- Contact
  - ☑️ Sliding
  - ☑️ Elastic
  - ☑️ Facet-Facet
  - ☑️ Node-Facet
  - ☑️ Biphasic
  - ☑️ Sliding2
  - ☑️ Contact Potential Formulation
  - ☑️ Tie
  - ☑️ Elastic
  - ☑️ Facet-Facet
  - ☑️ Node-Facet
  - ☑️ Biphasic
- Step
  - ☑️ Multistep Analysis
- Output
  - ☑️ Log File Configuration
  - ☑️ Plot File Configuration
  - ☑️ Node Variables
  - ☑️ Element Variables
  - ☑️ Rigid Body Variables
  - ☑️ Rigid Connector Variables
- XPLT
  - ✅ Convert XPLT to HDF5
