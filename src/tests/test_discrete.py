from copy import deepcopy

import pytest

import pyfebio as feb


@pytest.fixture(scope="module")
def base_model(rigid_body_febmesh):
    my_model = feb.model.Model(mesh_=rigid_body_febmesh)
    my_model.control_.time_steps = 100
    my_model.control_.step_size = 0.02
    my_model.control_.time_stepper = None
    for i, element in enumerate(my_model.mesh_.elements):
        my_model.material_.add_material(feb.material.RigidBody(id=i + 1, name=element.name))
        my_model.meshdomains_.add_solid_domain(feb.meshdomains.SolidDomain(name=element.name, mat=element.name))

    my_model.rigid_.add_rigid_bc(feb.rigid.RigidFixed(rb="bodyA", Rx_dof=1, Ry_dof=1, Rz_dof=1, Ru_dof=1, Rv_dof=1, Rw_dof=1))
    my_model.rigid_.add_rigid_bc(feb.rigid.RigidFixed(rb="bodyB", Rx_dof=1, Ry_dof=1, Rz_dof=0, Ru_dof=1, Rv_dof=1, Rw_dof=1))

    return my_model


def test_hill_element(base_model, tmp_path):
    my_model = deepcopy(base_model)
    discrete_elements = [
        feb.mesh.DiscreteElement(text="5,9"),
        feb.mesh.DiscreteElement(text="6,10"),
        feb.mesh.DiscreteElement(text="7,11"),
        feb.mesh.DiscreteElement(text="8,12"),
    ]
    my_model.mesh_.add_discrete_set(feb.mesh.DiscreteSet(name="muscle", elements=discrete_elements))
    force_length = feb.discrete.Scale(
        type="point",
        interpolate="smooth",
        points=feb.discrete.ScalePoints(pt=["0.0,0.0", "0.16,0.19", "0.8,0.95", "0.9,1.0", "1.1,1.0", "1.2,0.95", "1.84,0.19", "2.0,0.0"]),
    )
    muscle = feb.discrete.HillElement(id=1, name="muscle", Ksh=5.0, ac=1.0, Fmax=1.0, Ftl=force_length)
    my_model.discrete_.add_discrete_material(muscle)
    my_model.discrete_.add_discrete_element(feb.discrete.DiscreteEntry(dmat=1, discrete_set="muscle"))
    my_model.rigid_.add_rigid_bc(
        feb.rigid.RigidPrescribed(rb="bodyB", type="rigid_displacement", dof="z", value=feb.rigid.Value(lc=1, text=1.0))
    )
    my_model.loaddata_.add_load_curve(
        feb.loaddata.LoadCurve(id=1, points=feb.loaddata.CurvePoints(points=["0.0,0.0", "1.0,-1.0", "2.0,1.0"]))
    )
    plot_file = feb.output.OutputPlotfile(
        all_vars=[
            feb.output.Var(type="discrete element force"),
            feb.output.Var(type="discrete element stretch"),
            feb.output.Var(type="displacement"),
        ]
    )
    my_model.output_.add_plotfile(plot_file)
    model_path = tmp_path / "HillElement.feb"
    my_model.save(model_path)
    result = feb.model.run_model(model_path)
    assert result == 0, "HillElement.feb failed to run."
