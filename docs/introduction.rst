Getting Started
===============

Installation
------------

From PyPi
~~~~~~~~~

With pip:

Create a virtual environment:

.. code-block:: bash

    /path/to/compatible-python -m venv .venv

where `/path/to/compatible-python` is the path to a compatible python executable.

Activate the virtual environment:

On Linux or macOS:

.. code-block:: bash

    source .venv/bin/activate

On Windows (cmd):

.. code-block:: bash

    .\.venv\Scripts\activate.bat

On Windows (powershell):

.. code-block:: bash

    .\.venv\Scripts\Activate.ps1

Install the package:

.. code-block:: bash

    pip install pyfebio

From Source (with uv manager)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Clone with https:

.. code-block:: bash

    git clone https://github.com/CompOrthoBiomech/pyfebio.git

Or,

Clone with ssh:

.. code-block:: bash

    git clone git@github.com:CompOrthoBiomech/pyfebio.git

**Using uv:**

Install uv from `here <https://docs.astral.sh/uv/getting-started/installation/>`_

In top-level repository directory:

.. code-block:: bash

    uv sync

This will create a virtual environment and install the package.

Testing
~~~~~~~

We rely on FEBio to check our generated models are valid. Therefore, you will need to have FEBio installed and available in your PATH.

To run all the tests, execute the following command:

.. code-block:: bash

    cd src
    pytest

For tests that depend on running finite element simulations, you can find them in the pytest tmp_path directory, which varies by operating system.

For the latest run:

on Linux,

.. code-block:: bash

    cd /tmp/pytest-of-[USER]/pytest-current/[TEST_FUNCTION_NAME]current

General Overview
----------------

pyfebio utilizes the pydantic-xml package, which extends the powerful type checking libary pydantic to support XML serialization.
An FEBio input file is an XML tree with the following top-level structure:

.. code-block:: xml

    <febio_spec version="4.0">
        <Module>
            ...
        </Module>
        <Globals>
            ...
        </Globals>
        <Control>
            ...
        </Control>
        <Material>
            ...
        </Material>
        <Mesh>
            ...
        </Mesh>
        <MeshDomains>
            ...
        </MeshDomains>
        <MeshData>
            ...
        </MeshData>
        <MeshAdaptor>
            ...
        </MeshAdaptor>
        <Initial>
            ...
        </Initial>
        <Boundary>
            ...
        </Boundary>
        <Loads>
            ...
        </Loads>
        <Contact>
            ...
        </Contact>
        <Constraints>
            ...
        </Constraints>
        <Rigid>
            ...
        </Rigid>
        <Discrete>
            ...
        </Discrete>
        <LoadData>
            ...
        </LoadData>
        <Step>
            ...
        </Step>
        <Output>
            ...
        </Output>
    </febio_spec>

The modules in pyfebio are divided and named based on this structure.

- module.py
- globals.py
- control.py
- material.py
- mesh.py
- meshdomains.py
- meshdata.py
- meshadaptor.py
- initial.py
- boundary.py
- loads.py
- contact.py
- constraints.py
- rigid.py
- discrete.py
- loaddata.py
- step.py
- output.py

We have three additional modules:

- model.py -- Assembles the XML tree
- xplt.py -- Converts XPLT files to HDF5
- _types.py -- Defines custom types used throughout the package

All XML elements of the FEBio model are defined as **BaseXmlModel** classes. These inherit from
the pydantic BaseModel class, but add support for XML serialization and deserialization. pydantic-xml
also provides the **element** and **attr** classes. These allow the definition of XML sub-elements and XML attributes of a
BaseXmlModel class, respectively.

For example, the **BCZeroDisplacement** class that defines a zero displacement boundary condition,

.. code-block:: python

    class BCZeroDisplacement(BaseXmlModel, validate_assignment=True):
        type: Literal["zero displacement"] = attr(default="zero displacement", frozen=True)
        node_set: str = attr()
        x_dof: Literal[0, 1] = element(default=0)
        y_dof: Literal[0, 1] = element(default=0)
        z_dof: Literal[0, 1] = element(default=0)

a boundary condition fixing x displacement is instantiated as,

.. code-block:: python

    fixed_displacment = BCDisplacement(node_set="my_node_set", x_dof=1)

yielding the XML element,

.. code-block:: xml

    <bc type="zero displacement" node_set="my_node_set">
        <x_dof>1</x_dof>
        <y_dof>0</y_dof>
        <z_dof>0</z_dof>
    </bc>

Note how the XML tag is the class attribute name (this can be overridden by setting the *alias* argument if needed).

The Python type hint following each attribute variable is enforced by pydantic at runtime. Therefore for the BCZeroDisplacement
class,

- type -- can only be "zero displacement"
- node_set -- must be a str and must also be provided at instantiation
- x_dof -- must be either 0 or 1
- y_dof -- must be either 0 or 1
- z_dof -- must be either 0 or 1

We could also place different constraints on the attribute values, such as requiring a float to be greater than zero, or even more elaborate
constraints via a validator function.

Often, we need to define sub-elements, which have there own sub-elements and attributes. We handle these cases, by defining BaseXmlModel classes
for these sub-elements.


For example, a load-curve is defined as,

.. code-block:: python

    class LoadCurve(BaseXmlModel, tag="load_controller", validate_assignment=True):
        id: int = attr()
        type: Literal["loadcurve"] = attr(default="loadcurve", frozen=True)
        interpolate: Literal["LINEAR", "STEP", "SMOOTH"] = element(default="LINEAR")
        extend: Literal["CONSTANT", "EXTRAPOLATE", "REPEAT", "REPEAT OFFSET"] = element(default="CONSTANT")
        points: CurvePoints = element()

Notice the *points* attribute is of type *CurvePoints*, which is defined as,

.. code-block:: python

    class CurvePoints(BaseXmlModel, tag="points", validate_assignment=True):
        points: list[StringFloatVec2] = element(default=[], tag="pt")

        def add_point(self, new_point: StringFloatVec2):
            self.points.append(new_point)

This has a few things to note:

- The *StringFloatVec2* is a custom type that enforces a regex constraint on a str such that it looks like "{float},{float}" including scientific notation.
- When the type is an iterable, pydantic-xml will automatically create an element entry for each item
- The add_point() function allows you to append additional points to the *points* attribute

Putting it all together, we can create a load curve via,

.. code-block:: python

    load_curve = LoadCurve(id=1, points=CurvePoints(points=["0.0,0.0", "0.1,1.0", "1.0,1.0")])

and add a point,

.. code-block:: python

    load_curve.points.add_point("2.0,2.0")

producing:

.. code-block:: xml

    <load_controller id="1" type="loadcurve" interpolate="LINEAR" extend="CONSTANT">
        <points>
            <pt>0.0,0.0</pt>
            <pt>0.1,1.0</pt>
            <pt>1.0,1.0</pt>
            <pt>2.0,2.0</pt>
        </points>
    </load_controller>

Coding Example Video
--------------------

.. youtube:: Wt3u5f-XhMI


Recommendations
---------------

Use an IDE
~~~~~~~~~~

pyfebio is type annotated, which enables an IDE (with language server protocol support) to provide intelligent code completion and error checking.
Popular IDEs that will mostly work out-of-the-box (possibly requiring extensions to be installed but with little to no configuration) include:

- PyCharm
- VSCode
- Zed

More customized solutions (where you'll need to handle LSP, linter, fomatter installation and config) include,

- neovim
- emacs (recommend doom emacs variant)
