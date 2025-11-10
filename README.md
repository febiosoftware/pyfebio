## Overview

This is a Python package for generating FEBio input files. We rely heavily on pydantic and pydantic-xml
for type validation and XML serialization. Many of FEBio's features are covered, but not all.

## Getting Started

- [Installation](#installation)
- [Testing](#testing)
- [Example](#example)
- [Documentation](https://febiosoftware.github.io/pyfebio/index.html)
- [Features](#features)

## Installation

We will build PyPi packages later. For now, you can install from source:

Clone with https:

```bash
git clone https://github.com/CompOrthoBiomech/pyfebio.git
```

Or,

Clone with ssh:

```bash
git clone git@github.com:CompOrthoBiomech/pyfebio.git
```

**Using uv (preferred):**

Install uv from [here](https://docs.astral.sh/uv/getting-started/installation/)

In top-level repository directory:

```bash
uv sync
```

This will create a virtual environment and install the package.

**Using pip:**

You'll need a python executable that is >=3.11.

In top-level repository directory:

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
pip install .
```

If you want to run the tests, additionally install the dev group dependencies:

```bash
pip install . --group dev
```

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

:white_check_mark: Implemented and tested

:ballot_box_with_check: Implemented but untested

:x: Not yet implemented

- Control
  - :white_check_mark: All control settings
- Mesh Section
  - :white_check_mark: Nodes
  - :white_check_mark: Solid Elements:
     - tet4, tet10, hex8, hex20, hex27, penta6
  - :ballot_box_with_check: Shell Elements:
     - tri3, tri6, quad4, quad8, quad9, q4ans, q4eas
  - :ballot_box_with_check: Beam Elements:
     - line2, line3
  - :white_check_mark: Node, Element, Surface Sets
- MeshDomain
  - :white_check_mark: Solid Domain
  - :ballot_box_with_check: Shell Domain
  - :ballot_box_with_check: Beam Domain
  - :ballot_box_with_check: Granular control for integration schemes, etc.
- MeshData Section
  - :ballot_box_with_check: Node Data
  - :ballot_box_with_check: Scalar
  - :ballot_box_with_check: Vector3
  - :ballot_box_with_check: Element Data
  - :ballot_box_with_check: Scalar
  - :ballot_box_with_check: Vector3
  - :x: Surface Data
    - :x: Scalar
    - :x: Vector3
- MeshAdaptor
  - :ballot_box_with_check: Erosion
  - :white_check_mark: MMG3d Remeshing
  - :white_check_mark: hex_refine
  - :white_check_mark: hex_refine2d
  - :ballot_box_with_check: Criteria
  - :ballot_box_with_check: element selection
  - :ballot_box_with_check: math
  - :ballot_box_with_check: min-max filter
  - :white_check_mark: relative error
  - :white_check_mark: stress
  - :ballot_box_with_check: contact gap
  - :ballot_box_with_check: damage
  - :ballot_box_with_check: max variable
- Material
  - :white_check_mark: Most Unconstrained Formulation Materials
  - :white_check_mark: Most Uncoupled Formulation Materials
  - :ballot_box_with_check: Prestrain Material
  - :ballot_box_with_check: Fiber models
  - :white_check_mark: Material Axis
    - :white_check_mark: Vector Definition
    - :white_check_mark: Fiber Vector
  - :ballot_box_with_check: Continuous Fiber Distributions
  - :ballot_box_with_check: Integration Schemes
  - :ballot_box_with_check: Element-wise, mapped, or math parameter defintion
  - :white_check_mark: Biphasic Materials
  - :white_check_mark: Viscoelastic Materials
  - :x: Multiphasic Materials
  - :x: Biphasic-solute Materials
  - :x: Chemical Reactions
  - :x: Active Contraction Materials
  - :x: Damage Materials
  - :x: First-order Homogenization
- Rigid
  - :ballot_box_with_check: Fixed Displacement and Rotation
  - :ballot_box_with_check: Prescribed Displacement and Rotation
  - :ballot_box_with_check: Precribed Rotation about Vector
  - :ballot_box_with_check: Prescribed Euler Rotation
  - :ballot_box_with_check: All Connectors
  - :ballot_box_with_check: Follower Loads
- Initial
  - :ballot_box_with_check: Initial Velocity
  - :ballot_box_with_check: Initial Pre-strain
- Loads
  - :ballot_box_with_check: Nodal Loads
  - :ballot_box_with_check: Traction Loads (surface)
  - :ballot_box_with_check: Pressure Loads (surface)
  - :ballot_box_with_check: Fluid Flux (surface)
  - :ballot_box_with_check: Fluid Pressure (surface)
- LoadData
  - :white_check_mark: Load Curves
    - :balloit_box_with_check: All Options
  - :ballot_box_with_check: PID Controllers
  - :ballot_box_with_check: Math Controllers
- Boundary
  - :white_check_mark: Fixed Displacement (solid)
  - :white_check_mark: Prescribed Displacement (solid)
  - :ballot_box_with_check: Fixed Displacement (shell)
  - :ballot_box_with_check: Prescribed Displacement (shell)
  - :ballot_box_with_check: Precribed Deformation Gradient
  - :ballot_box_with_check: Displacement Along Normals
  - :ballot_box_with_check: Fix to Rigid Body
  - :white_check_mark: Rigid Node Set Deformation (rotation about axis)
  - :white_check_mark: Zero Fluid Pressure
  - :ballot_box_with_check: Prescribed Fluid Pressure
- Constraints
  - :ballot_box_with_check: Symmetry Plane
  - :ballot_box_with_check: Prestrain
  - :ballot_box_with_check: In-Situ Stretch
- Contact
  - :ballot_box_with_check: Sliding
  - :ballot_box_with_check: Elastic
  - :ballot_box_with_check: Facet-Facet
  - :ballot_box_with_check: Node-Facet
  - :ballot_box_with_check: Biphasic
  - :ballot_box_with_check: Sliding2
  - :ballot_box_with_check: Contact Potential Formulation
  - :ballot_box_with_check: Tie
  - :ballot_box_with_check: Elastic
  - :ballot_box_with_check: Facet-Facet
  - :ballot_box_with_check: Node-Facet
  - :ballot_box_with_check: Biphasic
- Step
  - :ballot_box_with_check: Multistep Analysis
- Output
  - :ballot_box_with_check: Log File Configuration
  - :ballot_box_with_check: Plot File Configuration
  - :ballot_box_with_check: Node Variables
  - :ballot_box_with_check: Element Variables
  - :ballot_box_with_check: Rigid Body Variables
  - :ballot_box_with_check: Rigid Connector Variables
