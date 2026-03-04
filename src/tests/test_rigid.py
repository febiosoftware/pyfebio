from copy import deepcopy

import pytest

import pyfebio as feb


@pytest.fixture(scope="module")
def base_model(rigid_body_febmesh) -> feb.model.Model:
    my_model = feb.model.Model(mesh_=rigid_body_febmesh)
    for i, element in enumerate(my_model.mesh_.elements):
        my_model.material_.add_material(feb.material.RigidBody(id=i + 1, name=element.name, center_of_mass="1.0,0.5,4.5"))
        my_model.meshdomains_.add_solid_domain(feb.meshdomains.SolidDomain(name=element.name, mat=element.name))
    my_model.rigid_.add_rigid_bc(feb.rigid.RigidFixed(rb="bodyA", Rx_dof=1, Ry_dof=1, Rz_dof=1, Ru_dof=1, Rv_dof=1, Rw_dof=1))
    return my_model


def test_prescribed_displacement_rotation(base_model, tmp_path):
    my_model = deepcopy(base_model)
    my_model.rigid_.add_rigid_bc(
        feb.rigid.RigidPrescribed(type="rigid_rotation", rb="bodyB", dof="Ru", value=feb.rigid.Value(lc=1, text=0.7535))
    )
    my_model.rigid_.add_rigid_bc(
        feb.rigid.RigidPrescribed(type="rigid_rotation", rb="bodyB", dof="Rv", value=feb.rigid.Value(lc=1, text=0.7535))
    )
    my_model.rigid_.add_rigid_bc(
        feb.rigid.RigidPrescribed(type="rigid_rotation", rb="bodyB", dof="Rw", value=feb.rigid.Value(lc=1, text=0.7535))
    )
    my_model.rigid_.add_rigid_bc(feb.rigid.RigidPrescribed(rb="bodyB", dof="x", value=feb.rigid.Value(lc=1, text=1.0)))
    my_model.rigid_.add_rigid_bc(feb.rigid.RigidPrescribed(rb="bodyB", dof="y", value=feb.rigid.Value(lc=1, text=1.0)))
    my_model.rigid_.add_rigid_bc(feb.rigid.RigidPrescribed(rb="bodyB", dof="z", value=feb.rigid.Value(lc=1, text=1.0)))
    my_model.loaddata_.add_load_curve(feb.loaddata.LoadCurve(id=1, points=feb.loaddata.CurvePoints(points=["0.0,0.0", "1.0,1.0"])))
    model_name = tmp_path / "RigidPrescribedDisplacementRotation.feb"
    my_model.save(model_name)
    assert feb.model.run_model(model_name, silent=False) == 0, "RigidPrescribedDisplacementRotation.feb failed to run"


def test_prescribed_rotation_about_vector(base_model, tmp_path):
    my_model = deepcopy(base_model)
    my_model.rigid_.add_rigid_bc(
        feb.rigid.RigidBodyRotationVector(
            rb="bodyB",
            vx=feb.rigid.RigidBodyRotationVector.X(lc=1, text=0.0),
            vy=feb.rigid.RigidBodyRotationVector.Y(lc=1, text=0.0),
            vz=feb.rigid.RigidBodyRotationVector.Z(lc=1, text=3.14),
        )
    )
    my_model.loaddata_.add_load_curve(feb.loaddata.LoadCurve(id=1, points=feb.loaddata.CurvePoints(points=["0.0,0.0", "1.0,1.0"])))
    model_name = tmp_path / "RigidPrescribedRotationAboutVector.feb"
    my_model.save(model_name)
    assert feb.model.run_model(model_name, silent=False) == 0, "RigidPrescribedRotationAboutVector.feb failed to run"


def test_prescribed_euler_rotation(base_model, tmp_path):
    my_model = deepcopy(base_model)
    my_model.rigid_.add_rigid_bc(
        feb.rigid.RigidBodyEulerAngle(
            rb="bodyB",
            Ex=feb.rigid.RigidBodyEulerAngle.X(lc=1, text=0.0),
            Ey=feb.rigid.RigidBodyEulerAngle.Y(lc=1, text=0.0),
            Ez=feb.rigid.RigidBodyEulerAngle.Z(lc=1, text=180.0),
        )
    )
    my_model.loaddata_.add_load_curve(feb.loaddata.LoadCurve(id=1, points=feb.loaddata.CurvePoints(points=["0.0,0.0", "1.0,1.0"])))
    model_name = tmp_path / "RigidEulerRotation.feb"
    my_model.save(model_name)
    assert feb.model.run_model(model_name, silent=False) == 0, "RigidEulerRotation.feb failed to run"


def test_rigid_spherical_joint(base_model, tmp_path):
    my_model = deepcopy(base_model)
    my_model.control_.time_steps = 20
    my_model.control_.step_size = 0.1
    my_model.control_.time_stepper = None
    spherical_joint = feb.rigid.RigidSphericalJoint(
        name="spherical_a-b",
        body_a="bodyA",
        body_b="bodyB",
        joint_origin="1.0,0.5,4.5",
        prescribed_rotation=1,
        rotation_x=feb.rigid.Value(lc=1, text=1.57),
        rotation_y=feb.rigid.Value(lc=1, text=1.57),
        rotation_z=feb.rigid.Value(lc=2, text=6.28),
    )
    my_model.rigid_.add_rigid_connector(spherical_joint)
    my_model.loaddata_.add_math_controller(feb.loaddata.MathController(id=1, math="sin(2*pi*t)"))
    my_model.loaddata_.add_load_curve(feb.loaddata.LoadCurve(id=2, points=feb.loaddata.CurvePoints(points=["0.0,0.0", "2.0,1.0"])))
    model_name = tmp_path / "RigidSphericalJoint.feb"
    my_model.save(model_name)
    assert feb.model.run_model(model_name, silent=True) == 0, "RigidSphericalJoint.feb failed to run"


def test_rigid_revolute_joint(base_model, tmp_path):
    my_model = deepcopy(base_model)
    my_model.control_.time_steps = 10
    my_model.control_.step_size = 0.1
    my_model.control_.time_stepper = None
    joint = feb.rigid.RigidRevoluteJoint(
        name="revolute_a-b",
        body_a="bodyA",
        body_b="bodyB",
        joint_origin="1.0,0.5,4.5",
        rotation_axis="1.0,0.0,0.0",
        prescribed_rotation=1,
        rotation=feb.rigid.Value(lc=1, text=6.28),
    )
    my_model.rigid_.add_rigid_connector(joint)
    my_model.loaddata_.add_load_curve(feb.loaddata.LoadCurve(id=1, points=feb.loaddata.CurvePoints(points=["0.0,0.0", "1.0,1.0"])))
    model_name = tmp_path / "RigidRevoluteJoint.feb"
    my_model.save(model_name)
    assert feb.model.run_model(model_name, silent=True) == 0, "RigidRevoluteJoint.feb failed to run"


def test_rigid_prismatic_joint(base_model, tmp_path):
    my_model = deepcopy(base_model)
    my_model.control_.time_steps = 10
    my_model.control_.step_size = 0.1
    my_model.control_.time_stepper = None
    joint = feb.rigid.RigidPrismaticJoint(
        name="revolute_a-b",
        body_a="bodyA",
        body_b="bodyB",
        joint_origin="1.0,0.5,4.5",
        translation_axis="1.0,0.0,0.0",
        transverse_axis="0.0,1.0,0.0",
        prescribed_translation=1,
        translation=feb.rigid.Value(lc=1, text=3.0),
    )
    my_model.rigid_.add_rigid_connector(joint)
    my_model.loaddata_.add_math_controller(feb.loaddata.MathController(id=1, math="sin(2*pi*t)"))
    model_name = tmp_path / "RigidPrismaticJoint.feb"
    my_model.save(model_name)
    assert feb.model.run_model(model_name, silent=True) == 0, "RigidPrismaticJoint.feb failed to run"


def test_rigid_cylindrical_joint(base_model, tmp_path):
    my_model = deepcopy(base_model)
    my_model.control_.time_steps = 10
    my_model.control_.step_size = 0.1
    my_model.control_.time_stepper = None
    joint = feb.rigid.RigidCylindricalJoint(
        name="revolute_a-b",
        body_a="bodyA",
        body_b="bodyB",
        joint_origin="1.0,0.5,4.5",
        joint_axis="1.0,0.0,0.0",
        transverse_axis="0.0,1.0,0.0",
        prescribed_translation=1,
        prescribed_rotation=1,
        rotation=feb.rigid.Value(lc=1, text=1.57),
        translation=feb.rigid.Value(lc=1, text=3.0),
    )
    my_model.rigid_.add_rigid_connector(joint)
    my_model.loaddata_.add_math_controller(feb.loaddata.MathController(id=1, math="sin(2*pi*t)"))
    model_name = tmp_path / "RigidCylindricalJoint.feb"
    my_model.save(model_name)
    assert feb.model.run_model(model_name, silent=True) == 0, "RigidCylindricalJoint.feb failed to run"


def test_rigid_planar_joint(base_model, tmp_path):
    my_model = deepcopy(base_model)
    my_model.control_.time_steps = 10
    my_model.control_.step_size = 0.1
    my_model.control_.time_stepper = None
    joint = feb.rigid.RigidPlanarJoint(
        name="revolute_a-b",
        body_a="bodyA",
        body_b="bodyB",
        joint_origin="1.0,0.5,4.5",
        rotation_axis="0.0,1.0,0.0",
        translation_axis_1="1.0,0.0,0.0",
        prescribed_rotation=1,
        rotation=feb.rigid.Value(lc=1, text=3 * 6.28),
        prescribed_translation_1=1,
        translation_1=feb.rigid.Value(lc=2, text=6.0),
        prescribed_translation_2=1,
        translation_2=feb.rigid.Value(lc=3, text=6.0),
    )
    my_model.rigid_.add_rigid_connector(joint)
    my_model.loaddata_.add_load_curve(feb.loaddata.LoadCurve(id=1, points=feb.loaddata.CurvePoints(points=["0.0,0.0", "1.0,1.0"])))
    my_model.loaddata_.add_math_controller(feb.loaddata.MathController(id=2, math="t*cos(6*pi*t)"))
    my_model.loaddata_.add_math_controller(feb.loaddata.MathController(id=3, math="t*sin(6*pi*t)"))
    model_name = tmp_path / "RigidCylindricalJoint.feb"
    my_model.save(model_name)
    assert feb.model.run_model(model_name, silent=True) == 0, "RigidCylindricalJoint.feb failed to run"


def test_rigid_lock(base_model, tmp_path):
    my_model = deepcopy(base_model)
    my_model.control_.time_steps = 1
    my_model.control_.step_size = 1.0
    my_model.control_.time_stepper = None
    joint = feb.rigid.RigidLock(
        name="lock_a-b",
        body_a="bodyA",
        body_b="bodyB",
        joint_origin="1.0,0.5,4.5",
        first_axis="0.0,1.0,0.0",
        second_axis="1.0,0.0,0.0",
    )
    my_model.rigid_.add_rigid_connector(joint)
    my_model.loaddata_.add_load_curve(feb.loaddata.LoadCurve(id=1, points=feb.loaddata.CurvePoints(points=["0.0,0.0", "1.0,1.0"])))
    model_name = tmp_path / "RigidLock.feb"
    my_model.save(model_name)
    assert feb.model.run_model(model_name, silent=True) == 0, "RigidLock.feb failed to run"


def test_rigid_spring(base_model, tmp_path):
    my_model = deepcopy(base_model)
    my_model.control_.solver = feb.control.ExplicitSolver()
    my_model.control_.analysis = "DYNAMIC"
    my_model.control_.time_steps = 64
    my_model.control_.step_size = 1 / 64.0
    my_model.control_.plot_stride = 8
    my_model.control_.time_stepper = None
    joint = feb.rigid.RigidSpring(
        name="spring_a-b",
        body_a="bodyA",
        body_b="bodyB",
        k=5.053237e-3,
        insertion_a="1.0,0.5,4.0",
        insertion_b="1.0,0.5,5.0",
        free_length=1.5,
    )
    my_model.rigid_.add_rigid_connector(joint)
    my_model.rigid_.add_rigid_bc(feb.rigid.RigidFixed(rb="bodyB", Rx_dof=1, Ry_dof=1, Ru_dof=1, Rv_dof=1, Rw_dof=1))
    my_model.loads_.add_body_load(feb.loads.ConstantBodyForce(z=feb.loads.Scale(text=-9.81)))
    model_name = tmp_path / "RigidSpring.feb"
    my_model.save(model_name)
    assert feb.model.run_model(model_name, silent=False) == 0, "RigidSpring.feb failed to run"


def test_rigid_spring_and_damper(base_model, tmp_path):
    c = 4.021238e-4 / 10.0
    my_model = deepcopy(base_model)
    my_model.control_.solver = feb.control.ExplicitSolver()
    my_model.control_.analysis = "DYNAMIC"
    my_model.control_.time_steps = 64
    my_model.control_.step_size = 1 / 64.0
    my_model.control_.plot_stride = 1
    my_model.control_.time_stepper = None
    spring = feb.rigid.RigidSpring(
        name="spring_a-b",
        body_a="bodyA",
        body_b="bodyB",
        k=5.053237e-3,
        insertion_a="1.0,0.5,4.0",
        insertion_b="1.0,0.5,5.0",
        free_length=1.5,
    )
    damper = feb.rigid.RigidDamper(
        name="spring_a-b",
        body_a="bodyA",
        body_b="bodyB",
        c=c,
        insertion_a="1.0,0.5,4.0",
        insertion_b="1.0,0.5,5.0",
    )
    my_model.rigid_.add_rigid_connector(spring)
    my_model.rigid_.add_rigid_connector(damper)
    my_model.rigid_.add_rigid_bc(feb.rigid.RigidFixed(rb="bodyB", Rx_dof=1, Ry_dof=1, Ru_dof=1, Rv_dof=1, Rw_dof=1))
    my_model.loads_.add_body_load(feb.loads.ConstantBodyForce(z=feb.loads.Scale(text=-9.81)))
    model_name = tmp_path / "RigidSpringDamper.feb"
    my_model.save(model_name)
    assert feb.model.run_model(model_name, silent=False) == 0, "RigidSpringDamper.feb failed to run"


def test_rigid_angular_damper(base_model, tmp_path):
    my_model = deepcopy(base_model)
    my_model.control_.analysis = "DYNAMIC"
    my_model.control_.time_steps = 10
    my_model.control_.step_size = 1.0

    my_model.rigid_.add_rigid_bc(feb.rigid.RigidFixed(rb="bodyB", Rv_dof=1, Rw_dof=1))

    joint = feb.rigid.RigidRevoluteJoint(
        name="revolute_a-b",
        body_a="bodyA",
        body_b="bodyB",
        joint_origin="1.0,0.5,4.5",
        auto_penalty=1,
        rotation_axis="1.0,0.0,0.0",
        transverse_axis="0.0,1.0,0.0",
        moment=feb.rigid.Value(text=1e-2),
        laugon=1,
    )
    damper = feb.rigid.RigidAngularDamper(name="angular_damper_a-b", body_a="bodyA", body_b="bodyB", c=1e-2)
    my_model.rigid_.add_rigid_connector(joint)
    my_model.rigid_.add_rigid_connector(damper)
    my_model.loaddata_.add_load_curve(feb.loaddata.LoadCurve(id=1, points=feb.loaddata.CurvePoints(points=["0.0,0.0", "10.0,1.0"])))
    my_model.output_.add_plotfile(
        feb.output.OutputPlotfile(all_vars=[feb.output.Var(type="displacement"), feb.output.Var(type="rigid torque")])
    )
    model_name = tmp_path / "RigidDampedCylindricalJoint.feb"
    my_model.save(model_name)
    assert feb.model.run_model(model_name, silent=True) == 0, "RigidDampedCylindricalJoint.feb failed to run"


def test_rigid_contractile_force(base_model, tmp_path):
    my_model = deepcopy(base_model)
    my_model.control_.analysis = "DYNAMIC"
    my_model.control_.time_steps = 10
    my_model.control_.step_size = 0.1
    my_model.control_.time_stepper = None
    joint = feb.rigid.RigidContractileForce(
        name="actuator_a-b",
        body_a="bodyA",
        body_b="bodyB",
        f0=feb.rigid.Value(text=1.0e-5),
        insertion_a="1.0,0.5,4.0",
        insertion_b="1.0,0.5,5.0",
    )
    my_model.rigid_.add_rigid_connector(joint)
    # my_model.loaddata_.add_load_curve(feb.loaddata.LoadCurve(id=1, points=feb.loaddata.CurvePoints(points=["0.0,0.0", "1.0,1.0"])))
    my_model.rigid_.add_rigid_bc(feb.rigid.RigidFixed(rb="bodyB", Rx_dof=1, Ry_dof=1, Ru_dof=1, Rv_dof=1, Rw_dof=1))
    model_name = tmp_path / "RigidContractileForce.feb"
    my_model.save(model_name)
    assert feb.model.run_model(model_name, silent=False) == 0, "RigidContractileForce.feb failed to run"
