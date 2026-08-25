Examples
========

.. _elastic_hex20:

Elastic Hex20
-------------

This example demonstrates how to convert a mesh from gmsh format
to a meshio object and then translate that to a pyfebio mesh. The
element and surface sets defined in the gmsh file are translated to lists of
pyfebio **Elements** and **Surfaces**. Node sets are also created from the surfaces.
A pyfebio **Model** is then instantiated with default values other than the mesh, which is
specified as our translated mesh.

Each **Elements** object represents a part. We loop over these parts and assign a **NeoHookean** material
and a **SolidDomain** to each. We assign a **BCZeroDispacement** boundary condition to the "bottom" node sets
with all degrees of freedom active (fixing the bottom nodes in space).

We twist the top face by applying a **BCRigidDeformation**. The **pos** argument is a point on the axis of
rotation, the **rot** argument is the rotation axis (its magnitude is the rotation angle, in this case :math:`\pi` radians).


.. literalinclude:: ../src/examples/elastic_hex20.py
    :language: python


.. figure:: _static/elastic_hex20.gif
    :width: 400px
    :align: center

    The maximum Green-Lagrange shear strain after twisting the top face by :math:`\pi` radians. Note the top layer is 2X stiffer than the bottom layer.

Biphasic Hex20
--------------

Most steps are similar to the :ref:`elastic_hex20` example. We instead instantiate
a pyfebio **BiphasicModel**, which sets the module to "biphasic", the analysis to "TRANSIENT",
and the solver type to "biphasic". We assign a **BiphasicMaterial** with a **NeoHookean** solid phase
and **ConstantIsoPerm** as the permeability. The bottom nodes are fixed in space, a **BCZeroFluidPressure** boundary
condition to allow free-draining on the top surface, and a **BCPrescribedDisplacement** in the z direction for
the top nodes.

.. literalinclude:: ../src/examples/biphasic_hex20.py
    :language: python

.. figure:: _static/biphasic_hex20.gif
    :width: 400px
    :align: center

    The effective fluid pressure after compressing the top face by 0.5mm in 0.1 seconds and then holding for 9.9 seconds. Note that
    the top element has twice the permeability of the bottom, hence the asymmetry in fluid pressure and deformation.

Sliding Contact
---------------

This example demonstrates sliding contact. This requires the definition of a **SurfacePair**, which is
then referenced in the **SlidingElastic** contact definition. We enforce the contact constraint with the
augmented Lagrange multiplier method by setting *laugon="AUGLAG"*. We also set *two_pass=1*, which helps
reduce penetration at the sharp edges of this very coarse mesh.

.. literalinclude:: ../src/examples/contact.py
    :language: python

.. figure:: _static/contact.gif
    :width: 400px
    :align: center

    The z-displacement resulting from the contact simulation. Note the nodal penetration near the sharp edge due to the coarse mesh size.
    This is more severe if the penalty method is used or two_pass is turned off.

Adaptive Remeshing
------------------

FEBio has several implementations of adaptive remeshing. This example demonstrates an adaptor that will refine a hex8 mesh to reduce the stress error in the bottom-layer.

.. literalinclude:: ../src/examples/mesh_adapt.py
    :language: python

.. figure:: _static/meshadapt.gif
    :width: 400px
    :align: center

    The hex mesh adaptively refines to reduce the stress error in the bottom-layer. Note the greatest refinement occurs
    at the necking corners.

Three Cylinder Joint
--------------------

This example demonstrates the use of rigid connectors to create a three cylinder linkage, which is a popular approach to modeling joint dynamics.

.. literalinclude:: ../src/examples/three_cylinder_joint.py
    :language: python

.. figure:: _static/three_cylinder_joint.gif
    :width: 400px
    :align: center

    Enforcing :math:`\pm \frac{\pi}{2}` radian rotations about the flexion-extension, varus-valgus, and internal-external rotation axes, and :math:`\pm 1.0` inferior-superior, medial-lateral, and anterior-posterior translations
    with rigid connectors. The GhostA and GhostB rigid bodies are hidden.

XPLT Conversion to HDF5
-----------------------

This example demonstrates the conversion of XPLT files to HDF5 format.

In a script:

.. literalinclude:: ../src/examples/xplt_to_hdf5.py
    :language: python

From the command line in `src/examples directory`:

.. code-block:: bash

    python -m pyfebio.xplt ../../assets/elastic_hex20.xplt elastic_hex20.hdf5

One can then interact with the HDF5 file using the `h5py` package.

For example,

.. literalinclude:: ../src/examples/view_hdf5.py
    :language: python

Output:

.. code-block:: bash

    meshes/0/domains/bottom-layer shape: (1, 21) dtype: int32
    meshes/0/domains/top-layer shape: (1, 21) dtype: int32
    meshes/0/elementsets/bottom-layer shape: (1,) dtype: int32
    meshes/0/elementsets/top-layer shape: (1,) dtype: int32
    meshes/0/nodes shape: (32,) dtype: [('id', '<i4'), ('x', '<f4'), ('y', '<f4'), ('z', '<f4')]
    meshes/0/nodesets/1 shape: (32,) dtype: int32
    meshes/0/nodesets/back shape: (13,) dtype: int32
    meshes/0/nodesets/bottom shape: (8,) dtype: int32
    meshes/0/nodesets/front shape: (13,) dtype: int32
    meshes/0/nodesets/left shape: (13,) dtype: int32
    meshes/0/nodesets/right shape: (13,) dtype: int32
    meshes/0/nodesets/top shape: (8,) dtype: int32
    meshes/0/surfaces/back shape: (2, 10) dtype: int32
    meshes/0/surfaces/bottom shape: (1, 10) dtype: int32
    meshes/0/surfaces/front shape: (2, 10) dtype: int32
    meshes/0/surfaces/left shape: (2, 10) dtype: int32
    meshes/0/surfaces/right shape: (2, 10) dtype: int32
    meshes/0/surfaces/top shape: (1, 10) dtype: int32
    states/0/element_data/stress/bottom-layer shape: (1, 6) dtype: float32
    states/0/element_data/stress/top-layer shape: (1, 6) dtype: float32
    states/0/mesh/element_state shape: (2,) dtype: int32
    states/0/node_data/displacement/1 shape: (32, 3) dtype: float32
    states/1/element_data/stress/bottom-layer shape: (1, 6) dtype: float32
    states/1/element_data/stress/top-layer shape: (1, 6) dtype: float32
    states/1/mesh/element_state shape: (2,) dtype: int32
    states/1/node_data/displacement/1 shape: (32, 3) dtype: float32
    states/2/element_data/stress/bottom-layer shape: (1, 6) dtype: float32
    states/2/element_data/stress/top-layer shape: (1, 6) dtype: float32
    states/2/mesh/element_state shape: (2,) dtype: int32
    states/2/node_data/displacement/1 shape: (32, 3) dtype: float32
    states/3/element_data/stress/bottom-layer shape: (1, 6) dtype: float32
    states/3/element_data/stress/top-layer shape: (1, 6) dtype: float32
    states/3/mesh/element_state shape: (2,) dtype: int32
    states/3/node_data/displacement/1 shape: (32, 3) dtype: float32
    states/4/element_data/stress/bottom-layer shape: (1, 6) dtype: float32
    states/4/element_data/stress/top-layer shape: (1, 6) dtype: float32
    states/4/mesh/element_state shape: (2,) dtype: int32
    states/4/node_data/displacement/1 shape: (32, 3) dtype: float32
    states/5/element_data/stress/bottom-layer shape: (1, 6) dtype: float32
    states/5/element_data/stress/top-layer shape: (1, 6) dtype: float32
    states/5/mesh/element_state shape: (2,) dtype: int32
    states/5/node_data/displacement/1 shape: (32, 3) dtype: float32

    Time at state 5
    [1.]

    Displacement at state 5
    [[ 0.0000000e+00  0.0000000e+00  0.0000000e+00]
    [ 1.1734079e+00  3.4618369e-01  4.2698154e-04]
    [ 3.4618369e-01 -1.1734079e+00  4.2698154e-04]
    [ 0.0000000e+00  0.0000000e+00  0.0000000e+00]
    [ 0.0000000e+00  0.0000000e+00  0.0000000e+00]
    [-3.4618369e-01  1.1734079e+00  4.2698154e-04]
    [-1.1734079e+00 -3.4618369e-01  4.2698154e-04]
    [ 0.0000000e+00  0.0000000e+00  0.0000000e+00]
    [ 1.0007957e+00  9.9920303e-01  0.0000000e+00]
    [ 9.9920303e-01 -1.0007957e+00  0.0000000e+00]
    [-9.9920303e-01  1.0007957e+00  0.0000000e+00]
    [-1.0007957e+00 -9.9920303e-01  0.0000000e+00]
    [ 6.8272942e-01 -1.3276277e-01 -1.4378540e-03]
    [ 7.6155305e-01 -4.1322845e-01  8.6941756e-03]
    [-1.3276277e-01 -6.8272942e-01 -1.4378540e-03]
    [ 0.0000000e+00  0.0000000e+00  0.0000000e+00]
    [ 1.3276277e-01  6.8272942e-01 -1.4378540e-03]
    [-7.6155305e-01  4.1322845e-01  8.6941756e-03]
    [-6.8272942e-01  1.3276277e-01 -1.4378540e-03]
    [ 0.0000000e+00  0.0000000e+00  0.0000000e+00]
    [ 0.0000000e+00  0.0000000e+00  0.0000000e+00]
    [ 4.1322845e-01  7.6155305e-01  8.6941756e-03]
    [ 0.0000000e+00  0.0000000e+00  0.0000000e+00]
    [-4.1322845e-01 -7.6155305e-01  8.6941756e-03]
    [ 1.1713763e+00  6.9261616e-01  2.4284013e-03]
    [ 9.9999934e-01 -7.9632644e-04  0.0000000e+00]
    [ 6.9261616e-01 -1.1713763e+00  2.4284013e-03]
    [-6.9261616e-01  1.1713763e+00  2.4284013e-03]
    [-9.9999934e-01  7.9632644e-04  0.0000000e+00]
    [-1.1713763e+00 -6.9261616e-01  2.4284013e-03]
    [ 7.9632644e-04  9.9999934e-01  0.0000000e+00]
    [-7.9632644e-04 -9.9999934e-01  0.0000000e+00]]

    Displacement at state 5 of first 2 nodes
    [[0.0000000e+00 0.0000000e+00 0.0000000e+00]
    [1.1734079e+00 3.4618369e-01 4.2698154e-04]]

OpenKnee Biphasic
-----------------

Overview
~~~~~~~~

This example uses geometry from the OpenKnee(s) project specimen 003.
The femoral and tibial cartilage have been simplified to quadratic
triangular (6 node) elements. This substantially reduces computational
cost but comes with some concessions. With the current shell capabilities, we
can only apply fixed boundary conditions to the bottom shell nodes. This enables
us to fix the bottom nodes of the tibial cartilage, since we assume the tibia
does not move.

We make the femoral cartilage rigid, so we can move it in the z-direction. Due to
this assumption and the lack of menisci, this model overestimates the articular
cartilage contact pressure.

Note that we do not include geometry for the femur or tibia, as these are not necessary
for this simulation.

Our model simulates creep under compressive loading applied to the femoral rigid
body. The default conditions are:

- Compressive femoral force of -500 N in the z-direction ramped linearly over 1.0 seconds
- -500 N force held constant for 600.0 additional seconds, as the tibial cartilage creeps.

Most simulation parameters are defined as variables at the beginning of the script. Variation
of these parameters can be explored, but note that convergence of biphasic analyses can be
challenging, so parameters should be changed reasonably.

Some important considerations:

- mixed_formulation=1 is defined in the Control section. This utilizes quadratic
  shape functions for solid displacements and forces, but linear shape functions
  for the fluid pressures and fluxes. This was found to provide better convergence
  than using quadratic shape functions for both phases. An argument for this is that
  Laplace's equation is of degree 2 while Darcy's Law is of degree 1.
- Broyden's method is used because our stiffness matrix is non-symmetric
- ls_check_jacobians=1 is defined in the Control section. This allows the line search
  to continue even if a negative Jacobian is encountered. Often a step size can be
  found to overcome the negative Jacobian(s).

Script
~~~~~~

Consult the script code and comments for more details.

.. literalinclude:: ../src/examples/openknee_biphasic.py
    :language: python

Example Results
~~~~~~~~~~~~~~~

.. figure:: _static/openknee_biphasic.webp
    :width: 1920px
    :align: center

    Simulations of -500 N compression applied over 1.0 seconds and held for 600 additional seconds.
    Notice the relative volume change of the tibial cartilage shell elements as the cartilage creeps.
    The vectors represent the current fluid fluxes dynamically scaled to the value range in each time step.
    Likewise, the relative volume colors are dynamically adjusted. Click the image for full-size.

OpenKnee Elastic
----------------

TL;DR
~~~~~

Run the example with default settings:

.. code-block:: bash

    python openknee_elastic.py

See help for CLI arguments:

.. code-block:: bash

    python openknee_elastic.py --help

Overview
~~~~~~~~

This example uses geometry from the OpenKnee(s) project specimen 003.
The femoral and tibial cartilage have been simplified to quadratic
triangular (6 node) elements. This substantially reduces computational
cost but comes with some concessions. With the current shell capabilities, we
can only apply fixed boundary conditions to the bottom shell nodes. This enables
us to fix the bottom nodes of the tibial cartilage, since we assume the tibia
does not move. The femoral geometry is included just for visualization, and has
no effect on then simulation.

We defined a pydantic BaseModel to configure the model parameters.
Possibly of interest , we have defined a flag to choose between 3 levels of mesh refinement:

- COARSE (3mm edge),
- MEDIUM (2mm edge), and
- FINE (1mm edge),

which have substantially differing computational cost.

FEBio Features Demonstrated:

- Multistep Analysis
- Shell Boundary Conditions
- Rigid Cylindrical Joints
- Discrete nonlinear spring definition

    - A Blankevoort spring model defined using the string expression with appropriate Heaviside functions
      to make tension-only with a toe region and allow for prestrain definition

Additional Techniques Demonstrated:

- Defining a pydantic BaseModel for this particular study configuration
- Creating a parser that allows for overriding some configuration parameters from the command line interface

Simulation Details:

- Global Settings and Components:

  - Contact between the femoral and tibial cartilage is defined as SlidingElastic and enforced with the
    augmented Lagrangian method
  - The tibia is fixed in space
  - The bottom nodes of the tibial cartilage shells are fixed in space.
  - The femoral cartilage is rigidly constrained to the femoral rigid body.
  - The ligaments are defined based on a LigamentConfig model. The default configuration
    is contained in `ligament.json`

- Step 1: A compressive load is applied to the femur in the Z-direction with rotation about the X-axis fixed
  and all other DoF free.

- Step 2: The compressive load from Step 1 is kept constant, but a chain of 3 cylindrical joints is defined to
  control relative rigid body motion in the convention of Grood and Suntay (1983).

  - The chain starts at the tibia rigid body, which is fixed in space.
  - The tibiaGhost rigid body is constrained to translate along and rotate about the IE_rot_IS_translation (E3)
    cylindrical axis relative to the tibia rigid body.
  - The femurGhost rigid body is constrained to translate along and rotate about the VV_rot_AS_translation (E2)
    cylindrical axis relative to the tibiaGhost rigid body.
  - The femur rigid body is constrained to translate along and rotate about the Flexion_rot_ML_translation (E1)
    cylindrical axis relative to the femurGhost rigid body.
  - The flexion angle is prescribed, while all other joint DoFs are left free.

Script
~~~~~~

Consult the script code and comments for more details:

.. literalinclude:: ../src/examples/openknee_elastic.py
   :language: python

Ligament Configuration
~~~~~~~~~~~~~~~~~~~~~~

The default ligament configuration is shown below:

.. literalinclude:: ../src/examples/ligaments.json
   :language: json

Example Results
~~~~~~~~~~~~~~~

.. figure:: _static/openknee_elastic.webp
    :width: 1920px
    :align: center

    Simulations using the FINE and COARSE meshes with default settings: -500 N compression, 45° flexion.
    Click the image for full-size.
