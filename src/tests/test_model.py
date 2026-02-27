from typing import get_args

import pyfebio as feb


def test_instantiate_model():
    my_model = feb.model.Model()
    assert isinstance(my_model, feb.model.Model)


def test_tet4_model(tet4_febmesh, tmp_path):
    my_model = feb.model.Model(mesh_=tet4_febmesh)
    for i, element in enumerate(my_model.mesh_.elements):
        my_model.material_.add_material(feb.material.NeoHookean(name=element.name, id=i + 1))
        my_model.meshdomains_.add_solid_domain(feb.meshdomains.SolidDomain(name=element.name, mat=element.name))
    my_model.boundary_.add_bc(feb.boundary.BCZeroDisplacement(node_set="bottom", x_dof=1, y_dof=1, z_dof=1))
    my_model.boundary_.add_bc(
        feb.boundary.BCRigidDeformation(
            node_set="top",
            pos="0.5,0.5,0.0",
            rot=feb.boundary.Value(lc=1, text="0.0,0.0,3.14"),
        )
    )
    my_model.loaddata_.add_load_curve(feb.loaddata.LoadCurve(id=1, points=feb.loaddata.CurvePoints(points=["0,0", "1,1"])))
    my_model.save(tmp_path.joinpath("model.feb"))
    result = feb.model.run_model(f"{tmp_path.joinpath('model.feb')}")
    assert result == 0


def test_tet10_model(tet10_febmesh, tmp_path):
    my_model = feb.model.Model(mesh_=tet10_febmesh)
    for i, element in enumerate(my_model.mesh_.elements):
        my_model.material_.add_material(feb.material.NeoHookean(name=element.name, id=i + 1))
        my_model.meshdomains_.add_solid_domain(feb.meshdomains.SolidDomain(name=element.name, mat=element.name))
    my_model.boundary_.add_bc(feb.boundary.BCZeroDisplacement(node_set="bottom", x_dof=1, y_dof=1, z_dof=1))
    my_model.boundary_.add_bc(
        feb.boundary.BCRigidDeformation(
            node_set="top",
            pos="0.5,0.5,0.0",
            rot=feb.boundary.Value(lc=1, text="0.0,0.0,3.14"),
        )
    )
    my_model.loaddata_.add_load_curve(feb.loaddata.LoadCurve(id=1, points=feb.loaddata.CurvePoints(points=["0,0", "1,1"])))

    my_model.save(tmp_path.joinpath("model.feb"))
    result = feb.model.run_model(f"{tmp_path.joinpath('model.feb')}")
    assert result == 0


def test_hex8_model(hex8_febmesh, tmp_path):
    my_model = feb.model.Model(mesh_=hex8_febmesh)
    for i, element in enumerate(my_model.mesh_.elements):
        my_model.material_.add_material(feb.material.NeoHookean(name=element.name, id=i + 1))
        my_model.meshdomains_.add_solid_domain(feb.meshdomains.SolidDomain(name=element.name, mat=element.name))
    my_model.boundary_.add_bc(feb.boundary.BCZeroDisplacement(node_set="bottom", x_dof=1, y_dof=1, z_dof=1))
    my_model.boundary_.add_bc(
        feb.boundary.BCRigidDeformation(
            node_set="top",
            pos="0.5,0.5,0.0",
            rot=feb.boundary.Value(lc=1, text="0.0,0.0,3.14"),
        )
    )
    my_model.loaddata_.add_load_curve(feb.loaddata.LoadCurve(id=1, points=feb.loaddata.CurvePoints(points=["0,0", "1,1"])))

    my_model.save(tmp_path.joinpath("model.feb"))
    result = feb.model.run_model(f"{tmp_path.joinpath('model.feb')}")
    assert result == 0


def test_hex20_model(hex20_febmesh, tmp_path):
    my_model = feb.model.Model(mesh_=hex20_febmesh)
    for i, element in enumerate(my_model.mesh_.elements):
        my_model.material_.add_material(feb.material.NeoHookean(name=element.name, id=i + 1))
        my_model.meshdomains_.add_solid_domain(feb.meshdomains.SolidDomain(name=element.name, mat=element.name))
    my_model.boundary_.add_bc(feb.boundary.BCZeroDisplacement(node_set="bottom", x_dof=1, y_dof=1, z_dof=1))
    my_model.boundary_.add_bc(
        feb.boundary.BCRigidDeformation(
            node_set="top",
            pos="0.5,0.5,0.0",
            rot=feb.boundary.Value(lc=1, text="0.0,0.0,3.14"),
        )
    )
    my_model.loaddata_.add_load_curve(feb.loaddata.LoadCurve(id=1, points=feb.loaddata.CurvePoints(points=["0,0", "1,1"])))

    my_model.save(tmp_path.joinpath("model.feb"))
    result = feb.model.run_model(f"{tmp_path.joinpath('model.feb')}")
    assert result == 0


def test_hex27_model(hex27_febmesh, tmp_path):
    my_model = feb.model.Model(mesh_=hex27_febmesh)
    for i, element in enumerate(my_model.mesh_.elements):
        my_model.material_.add_material(feb.material.NeoHookean(name=element.name, id=i + 1))
        my_model.meshdomains_.add_solid_domain(feb.meshdomains.SolidDomain(name=element.name, mat=element.name))
    my_model.boundary_.add_bc(feb.boundary.BCZeroDisplacement(node_set="bottom", x_dof=1, y_dof=1, z_dof=1))
    my_model.boundary_.add_bc(
        feb.boundary.BCRigidDeformation(
            node_set="top",
            pos="0.5,0.5,0.0",
            rot=feb.boundary.Value(lc=1, text="0.0,0.0,3.14"),
        )
    )
    my_model.loaddata_.add_load_curve(feb.loaddata.LoadCurve(id=1, points=feb.loaddata.CurvePoints(points=["0,0", "1,1"])))

    my_model.save(tmp_path.joinpath("model.feb"))
    result = feb.model.run_model(f"{tmp_path.joinpath('model.feb')}")
    assert result == 0


def test_nodal_loads(hex8_febmesh, tmp_path):
    for nodal_load in get_args(feb.loads.NodalLoadType):
        my_model = feb.model.Model(mesh_=hex8_febmesh)
        for i, element in enumerate(my_model.mesh_.elements):
            my_model.material_.add_material(
                feb.material.NeoHookean(
                    name=element.name, id=i + 1, E=feb.material.MaterialParameter(text=100.0), v=feb.material.MaterialParameter(text=0.0)
                )
            )
            my_model.meshdomains_.add_solid_domain(feb.meshdomains.SolidDomain(name=element.name, mat=element.name))
        my_model.boundary_.add_bc(feb.boundary.BCZeroDisplacement(node_set="bottom", x_dof=1, y_dof=1, z_dof=1))
        my_model.loads_.add_nodal_load(nodal_load(node_set="top"))
        my_model.loaddata_.add_load_curve(feb.loaddata.LoadCurve(id=1, points=feb.loaddata.CurvePoints(points=["0.0,0.0", "1.0,-1.0"])))
        my_model.save(tmp_path.joinpath(f"{nodal_load.__name__}.feb"))
        result = feb.model.run_model(tmp_path.joinpath(f"{nodal_load.__name__}.feb"), silent=False)
        assert result == 0, f"{nodal_load.__name__} failed"


def test_surface_loads(hex20_febmesh, tmp_path):
    for surface_load in (feb.loads.PressureLoad, feb.loads.TractionLoad):
        my_model = feb.model.Model(mesh_=hex20_febmesh)
        for i, element in enumerate(my_model.mesh_.elements):
            my_model.material_.add_material(
                feb.material.NeoHookean(
                    name=element.name, id=i + 1, E=feb.material.MaterialParameter(text=10.0), v=feb.material.MaterialParameter(text=0.3)
                )
            )
            my_model.meshdomains_.add_solid_domain(feb.meshdomains.SolidDomain(name=element.name, mat=element.name))
        my_model.boundary_.add_bc(feb.boundary.BCZeroDisplacement(node_set="bottom", x_dof=1, y_dof=1, z_dof=1))
        my_model.loads_.add_surface_load(surface_load(surface="top"))
        my_model.loaddata_.add_load_curve(feb.loaddata.LoadCurve(id=1, points=feb.loaddata.CurvePoints(points=["0.0,0.0", "1.0,1.0"])))
        my_model.save(tmp_path.joinpath(f"{surface_load.__name__}.feb"))
        result = feb.model.run_model(tmp_path.joinpath(f"{surface_load.__name__}.feb"), silent=False)
        assert result == 0, f"{surface_load.__name__} failed"


def test_beam2_model(beam2_febmesh, tmp_path):
    # TODO: we can only test the elastic-truss version which behaves like the linear-truss but can use
    # FEBio materials
    my_model = feb.model.Model(mesh_=beam2_febmesh)
    my_model.material_.add_material(feb.material.NeoHookean(name="truss", id=1, E=feb.material.MaterialParameter(text=100.0)))
    my_model.meshdomains_.add_beam_domain(
        feb.meshdomains.BeamDomain(type="elastic-truss", name="beam", mat="truss", cross_sectional_area=0.5, v=0.3)
    )
    my_model.boundary_.add_bc(feb.boundary.BCZeroDisplacement(node_set="bottom", x_dof=1, y_dof=1, z_dof=1))
    my_model.boundary_.add_bc(feb.boundary.BCZeroDisplacement(node_set="top", x_dof=0, y_dof=0, z_dof=1))
    my_model.loads_.add_nodal_load(feb.loads.NodalLoad(node_set="top", dof="y", scale=feb.loads.Scale(lc=1, text="-25.0")))
    my_model.loaddata_.add_load_curve(feb.loaddata.LoadCurve(id=1, points=feb.loaddata.CurvePoints(points=["0,0", "1,1"])))

    my_model.save(tmp_path.joinpath("model.feb"))
    result = feb.model.run_model(f"{tmp_path.joinpath('model.feb')}")
    assert result == 0


def test_beam3_model(beam3_febmesh, tmp_path):
    # TODO: we can only test the elastic-truss version which behaves like the linear-truss but can use
    # FEBio materials
    # I'm not sure what materials are assigned to the other types. Likewise, there is no quadratic beam domain
    my_model = feb.model.Model(mesh_=beam3_febmesh)
    my_model.material_.add_material(feb.material.NeoHookean(name="truss", id=1))
    my_model.meshdomains_.add_beam_domain(
        feb.meshdomains.BeamDomain(type="elastic-truss", name="beam", mat="truss", cross_sectional_area=0.1, v=0.3)
    )
    my_model.boundary_.add_bc(feb.boundary.BCZeroDisplacement(node_set="left", x_dof=1, y_dof=1, z_dof=1))
    my_model.boundary_.add_bc(feb.boundary.BCPrescribedDisplacement(node_set="right", dof="x", value=feb.boundary.Value(lc=1, text="0.5")))
    my_model.loaddata_.add_load_curve(feb.loaddata.LoadCurve(id=1, points=feb.loaddata.CurvePoints(points=["0,0", "1,1"])))

    my_model.save(tmp_path.joinpath("model.feb"))
    result = feb.model.run_model(f"{tmp_path.joinpath('model.feb')}")
    assert result == 0
