from pathlib import Path

import pyfebio as feb


def test_instantiate_model():
    my_model = feb.model.Model()
    assert isinstance(my_model, feb.model.Model)


def test_tet4_model(tet4_febmesh: feb.mesh.Mesh, tmp_path: Path):
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


def test_tet10_model(tet10_febmesh: feb.mesh.Mesh, tmp_path: Path):
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


def test_tet15_model(tet15_febmesh: feb.mesh.Mesh, tmp_path: Path):
    my_model = feb.model.Model(mesh_=tet15_febmesh)
    for i, element in enumerate(my_model.mesh_.elements):
        my_model.material_.add_material(feb.material.NeoHookean(name=element.name, id=i + 1))
        my_model.meshdomains_.add_solid_domain(feb.meshdomains.SolidDomain(name=element.name, mat=element.name))
    my_model.boundary_.add_bc(feb.boundary.BCZeroDisplacement(node_set="bottom", x_dof=1, y_dof=1, z_dof=1))
    my_model.boundary_.add_bc(feb.boundary.BCZeroDisplacement(node_set="top", x_dof=1, y_dof=1))
    my_model.boundary_.add_bc(feb.boundary.BCPrescribedDisplacement(node_set="top", dof="z", value=feb.boundary.Value(lc=1, text=-0.25)))
    my_model.loaddata_.add_load_curve(feb.loaddata.LoadCurve(id=1, points=feb.loaddata.CurvePoints(points=["0,0", "1,1"])))

    my_model.save(tmp_path.joinpath("model.feb"))
    result = feb.model.run_model(f"{tmp_path.joinpath('model.feb')}")
    assert result == 0


def test_hex8_model(hex8_febmesh: feb.mesh.Mesh, tmp_path: Path):
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


def test_hex20_model(hex20_febmesh: feb.mesh.Mesh, tmp_path: Path):
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


def test_hex27_model(hex27_febmesh: feb.mesh.Mesh, tmp_path: Path):
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


def test_penta6_model(penta6_febmesh: feb.mesh.Mesh, tmp_path: Path):
    my_model = feb.model.Model(mesh_=penta6_febmesh)
    for i, element in enumerate(my_model.mesh_.elements):
        my_model.material_.add_material(feb.material.NeoHookean(name=element.name, id=i + 1))
        my_model.meshdomains_.add_solid_domain(feb.meshdomains.SolidDomain(name=element.name, mat=element.name))
    my_model.boundary_.add_bc(feb.boundary.BCZeroDisplacement(node_set="bottom", x_dof=1, y_dof=1, z_dof=1))
    my_model.boundary_.add_bc(feb.boundary.BCPrescribedDisplacement(node_set="top", dof="z", value=feb.boundary.Value(lc=1, text=-0.2)))
    my_model.loaddata_.add_load_curve(feb.loaddata.LoadCurve(id=1, points=feb.loaddata.CurvePoints(points=["0,0", "1,1"])))

    my_model.save(tmp_path.joinpath("model.feb"))
    result = feb.model.run_model(f"{tmp_path.joinpath('model.feb')}")
    assert result == 0


def test_pyra5_model(pyra5_febmesh: feb.mesh.Mesh, tmp_path: Path):
    my_model = feb.model.Model(mesh_=pyra5_febmesh)
    for i, element in enumerate(my_model.mesh_.elements):
        my_model.material_.add_material(feb.material.NeoHookean(name=element.name, id=i + 1))
        my_model.meshdomains_.add_solid_domain(feb.meshdomains.SolidDomain(name=element.name, mat=element.name))
    my_model.boundary_.add_bc(feb.boundary.BCZeroDisplacement(node_set="bottom", x_dof=1, y_dof=1, z_dof=1))
    my_model.boundary_.add_bc(feb.boundary.BCZeroDisplacement(node_set="top", x_dof=1, y_dof=1))
    my_model.boundary_.add_bc(feb.boundary.BCPrescribedDisplacement(node_set="top", dof="z", value=feb.boundary.Value(lc=1, text=-0.25)))
    my_model.loaddata_.add_load_curve(feb.loaddata.LoadCurve(id=1, points=feb.loaddata.CurvePoints(points=["0,0", "1,1"])))

    my_model.save(tmp_path.joinpath("model.feb"))
    result = feb.model.run_model(f"{tmp_path.joinpath('model.feb')}")
    assert result == 0


def test_tri3_model(shell_tri3: feb.mesh.Mesh, tmp_path: Path):
    my_model = feb.model.Model(mesh_=shell_tri3)
    for i, element in enumerate(my_model.mesh_.elements):
        my_model.material_.add_material(feb.material.NeoHookean(name=element.name, id=i + 1))
        my_model.meshdomains_.add_shell_domain(feb.meshdomains.ShellDomain(name=element.name, mat=element.name))
    my_model.boundary_.add_bc(feb.boundary.BCZeroDisplacement(node_set="bottom", x_dof=1, y_dof=1, z_dof=1))
    my_model.boundary_.add_bc(feb.boundary.BCPrescribedDisplacement(node_set="top-left", dof="y", value=feb.boundary.Value(lc=1, text=0.5)))
    my_model.boundary_.add_bc(
        feb.boundary.BCPrescribedDisplacement(node_set="top-right", dof="y", value=feb.boundary.Value(lc=1, text=-0.5))
    )
    my_model.loaddata_.add_load_curve(feb.loaddata.LoadCurve(id=1, points=feb.loaddata.CurvePoints(points=["0,0", "1,1"])))
    my_model.output_.add_plotfile(
        feb.output.OutputPlotfile(all_vars=[feb.output.Var(type="shell strain"), feb.output.Var(type="displacement")])
    )
    my_model.save(tmp_path.joinpath("model.feb"))
    result = feb.model.run_model(f"{tmp_path.joinpath('model.feb')}", silent=False)
    assert result == 0, "Tri3 shell model failed"


def test_tri6_model(shell_tri6: feb.mesh.Mesh, tmp_path: Path):
    my_model = feb.model.Model(mesh_=shell_tri6)
    for i, element in enumerate(my_model.mesh_.elements):
        my_model.material_.add_material(feb.material.NeoHookean(name=element.name, id=i + 1))
        my_model.meshdomains_.add_shell_domain(feb.meshdomains.ShellDomain(name=element.name, mat=element.name))
    my_model.boundary_.add_bc(feb.boundary.BCZeroDisplacement(node_set="bottom", x_dof=1, y_dof=1, z_dof=1))
    my_model.boundary_.add_bc(feb.boundary.BCPrescribedDisplacement(node_set="top-left", dof="y", value=feb.boundary.Value(lc=1, text=0.5)))
    my_model.boundary_.add_bc(
        feb.boundary.BCPrescribedDisplacement(node_set="top-right", dof="y", value=feb.boundary.Value(lc=1, text=-0.5))
    )
    my_model.loaddata_.add_load_curve(feb.loaddata.LoadCurve(id=1, points=feb.loaddata.CurvePoints(points=["0,0", "1,1"])))
    my_model.output_.add_plotfile(
        feb.output.OutputPlotfile(all_vars=[feb.output.Var(type="shell strain"), feb.output.Var(type="displacement")])
    )
    my_model.save(tmp_path.joinpath("model.feb"))
    result = feb.model.run_model(f"{tmp_path.joinpath('model.feb')}", silent=False)
    assert result == 0, "Tri6 shell model failed"


def test_quad4_model(shell_quad4: feb.mesh.Mesh, tmp_path: Path):
    for etype, displacement in zip(("quad4", "q4ans", "q4eas"), (0.2, 0.01, 0.2)):
        my_model = feb.model.Model(mesh_=shell_quad4)
        for i, element in enumerate(my_model.mesh_.elements):
            element.type = etype
            my_model.material_.add_material(feb.material.MooneyRivlinUC(name=element.name, id=i + 1))
            my_model.meshdomains_.add_shell_domain(feb.meshdomains.ShellDomain(name=element.name, mat=element.name, shell_thickness=0.1))
        my_model.boundary_.add_bc(feb.boundary.BCZeroDisplacement(node_set="bottom", x_dof=1, y_dof=1, z_dof=1))
        my_model.boundary_.add_bc(
            feb.boundary.BCPrescribedDisplacement(node_set="top-left", dof="y", value=feb.boundary.Value(lc=1, text=displacement))
        )
        my_model.boundary_.add_bc(
            feb.boundary.BCPrescribedDisplacement(node_set="top-right", dof="y", value=feb.boundary.Value(lc=1, text=-displacement))
        )
        my_model.loaddata_.add_load_curve(feb.loaddata.LoadCurve(id=1, points=feb.loaddata.CurvePoints(points=["0,0", "1,1"])))
        my_model.output_.add_plotfile(
            feb.output.OutputPlotfile(all_vars=[feb.output.Var(type="shell strain"), feb.output.Var(type="displacement")])
        )
        my_model.save(tmp_path.joinpath(f"{etype}.feb"))
        result = feb.model.run_model(f"{tmp_path.joinpath(etype)}.feb", silent=False)
        assert result == 0, f"{etype} shell model failed"


def test_quad8_model(shell_quad8: feb.mesh.Mesh, tmp_path: Path):
    my_model = feb.model.Model(mesh_=shell_quad8)
    for i, element in enumerate(my_model.mesh_.elements):
        my_model.material_.add_material(feb.material.NeoHookean(name=element.name, id=i + 1))
        my_model.meshdomains_.add_shell_domain(feb.meshdomains.ShellDomain(name=element.name, mat=element.name, shell_thickness=0.1))
    my_model.boundary_.add_bc(feb.boundary.BCZeroDisplacement(node_set="bottom", x_dof=1, y_dof=1, z_dof=1))
    my_model.boundary_.add_bc(feb.boundary.BCPrescribedDisplacement(node_set="top-left", dof="y", value=feb.boundary.Value(lc=1, text=0.5)))
    my_model.boundary_.add_bc(
        feb.boundary.BCPrescribedDisplacement(node_set="top-right", dof="y", value=feb.boundary.Value(lc=1, text=-0.5))
    )
    my_model.loaddata_.add_load_curve(feb.loaddata.LoadCurve(id=1, points=feb.loaddata.CurvePoints(points=["0,0", "1,1"])))
    my_model.output_.add_plotfile(
        feb.output.OutputPlotfile(all_vars=[feb.output.Var(type="shell strain"), feb.output.Var(type="displacement")])
    )
    my_model.save(tmp_path.joinpath("model.feb"))
    result = feb.model.run_model(f"{tmp_path.joinpath('model.feb')}", silent=False)
    assert result == 0, "Quad8 shell model failed"


def test_beam2_model(beam2_febmesh: feb.mesh.Mesh, tmp_path: Path):
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


def test_beam3_model(beam3_febmesh: feb.mesh.Mesh, tmp_path: Path):
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


def test_rigid_fixed_bc(hex20_contact_febmesh: feb.mesh.Mesh, tmp_path: Path):
    my_model = feb.model.Model(mesh_=hex20_contact_febmesh)
    rigid_material = feb.material.RigidBody(name="bodyA", id=1)
    deformable_material = feb.material.NeoHookean(name="deformableBody", id=2)
    for part, mat in zip(my_model.mesh_.elements, (rigid_material, deformable_material)):
        my_model.material_.add_material(mat)
        my_model.meshdomains_.add_solid_domain(feb.meshdomains.SolidDomain(name=f"{part.name}", mat=f"{mat.name}"))

    my_model.boundary_.add_bc(feb.boundary.BCZeroDisplacement(node_set="top-box-top", x_dof=1, y_dof=1, z_dof=1))
    my_model.boundary_.add_bc(feb.boundary.BCRigid(node_set="top-box-bottom", rb="bodyA"))
    my_model.rigid_.add_rigid_bc(
        feb.rigid.RigidPrescribed(type="rigid_rotation", rb="bodyA", dof="Rw", value=feb.rigid.Value(lc=1, text=1.57))
    )
    my_model.rigid_.add_rigid_bc(feb.rigid.RigidFixed(rb="bodyA", Rx_dof=1, Ry_dof=1, Rz_dof=1, Ru_dof=1, Rv_dof=1))
    my_model.loaddata_.add_load_curve(feb.loaddata.LoadCurve(id=1, points=feb.loaddata.CurvePoints(points=["0,0", "1,1"])))

    my_model.save(tmp_path.joinpath("model.feb"))
    result = feb.model.run_model(f"{tmp_path.joinpath('model.feb')}")
    assert result == 0


def test_prescribed_deformation_gradient_bc(hex8_febmesh: feb.mesh.Mesh, tmp_path: Path):
    my_model = feb.model.Model(mesh_=hex8_febmesh)
    my_model.mesh_.add_node_set(
        feb.mesh.NodeSet(name="all", text=",".join([str(i + 1) for i, _ in enumerate(hex8_febmesh.nodes[0].all_nodes)]))
    )
    for i, element in enumerate(my_model.mesh_.elements):
        my_model.material_.add_material(feb.material.NeoHookean(name=element.name, id=i + 1))
        my_model.meshdomains_.add_solid_domain(feb.meshdomains.SolidDomain(name=element.name, mat=element.name))
    my_model.boundary_.add_bc(
        feb.boundary.BCPrescribedDeformation(
            node_set="all", scale=feb.boundary.Value(lc=1, text=1.0), F="4.0,0.0,0.0,0.0,0.5,0.0,0.0,0.0,0.5"
        )
    )
    my_model.loaddata_.add_load_curve(feb.loaddata.LoadCurve(id=1, points=feb.loaddata.CurvePoints(points=["0,0", "1,1"])))
    my_model.output_.add_plotfile(
        feb.output.OutputPlotfile(
            all_vars=[
                feb.output.Var(type="deformation gradient"),
                feb.output.Var(type="displacement"),
                feb.output.Var(type="relative volume"),
            ]
        )
    )

    my_model.save(tmp_path.joinpath("PrescribedDeformationGradient.feb"))
    result = feb.model.run_model(f"{tmp_path.joinpath('PrescribedDeformationGradient.feb')}")
    assert result == 0, "PrescribedDeformationGradient.feb failed to run."


def test_displacement_along_normals(hex8_febmesh: feb.mesh.Mesh, tmp_path: Path):
    my_model = feb.model.Model(mesh_=hex8_febmesh)
    for i, element in enumerate(my_model.mesh_.elements):
        my_model.material_.add_material(feb.material.NeoHookean(name=element.name, id=i + 1))
        my_model.meshdomains_.add_solid_domain(feb.meshdomains.SolidDomain(name=element.name, mat=element.name))
    my_model.boundary_.add_bc(feb.boundary.BCZeroDisplacement(node_set="bottom", x_dof=1, y_dof=1, z_dof=1))
    my_model.boundary_.add_bc(feb.boundary.BCNormalDisplacement(surface="top", scale=feb.boundary.Value(lc=1, text=1.0)))
    my_model.loaddata_.add_load_curve(feb.loaddata.LoadCurve(id=1, points=feb.loaddata.CurvePoints(points=["0,0", "1,1"])))
    my_model.output_.add_plotfile(
        feb.output.OutputPlotfile(
            all_vars=[
                feb.output.Var(type="displacement"),
            ]
        )
    )

    my_model.save(tmp_path.joinpath("DisplacementAlongNormals.feb"))
    result = feb.model.run_model(f"{tmp_path.joinpath('DisplacementAlongNormals.feb')}")
    assert result == 0, "DisplacementAlongNormals.feb failed to run."


def test_prescribed_fluid_pressure(hex20_febmesh: feb.mesh.Mesh, tmp_path: Path):
    my_model = feb.model.BiphasicModel(mesh_=hex20_febmesh)
    for i, element in enumerate(my_model.mesh_.elements):
        my_model.material_.add_material(feb.material.BiphasicMaterial(name=element.name, id=i + 1, solid=feb.material.NeoHookean()))
        my_model.meshdomains_.add_solid_domain(feb.meshdomains.SolidDomain(name=element.name, mat=element.name))

    my_model.boundary_.add_bc(feb.boundary.BCZeroDisplacement(node_set="bottom", x_dof=1, y_dof=1, z_dof=1))
    my_model.boundary_.add_bc(feb.boundary.BCZeroFluidPressure(node_set="bottom"))
    my_model.boundary_.add_bc(feb.boundary.BCPrescribedFluidPressure(node_set="top", value=feb.boundary.Value(lc=1, text=1.0e-1)))
    my_model.loaddata_.add_load_curve(feb.loaddata.LoadCurve(id=1, points=feb.loaddata.CurvePoints(points=["0,0", "1.0,1", "10.0,0.0"])))
    my_model.output_.add_plotfile(
        feb.output.OutputPlotfile(
            all_vars=[
                feb.output.Var(type="effective fluid pressure"),
                feb.output.Var(type="displacement"),
                feb.output.Var(type="nodal fluid flux"),
            ]
        )
    )
    my_model.save(tmp_path.joinpath("PrescribedFluidPressure.feb"))
    result = feb.model.run_model(f"{tmp_path.joinpath('PrescribedFluidPressure.feb')}")
    assert result == 0, "PrescribedFluidPressure.feb failed to run."


def test_multistep_model(hex8_febmesh: feb.mesh.Mesh, tmp_path: Path):
    my_model = feb.model.Model(mesh_=hex8_febmesh)
    for i, element in enumerate(my_model.mesh_.elements):
        my_model.material_.add_material(feb.material.NeoHookean(name=element.name, id=i + 1))
        my_model.meshdomains_.add_solid_domain(feb.meshdomains.SolidDomain(name=element.name, mat=element.name))
    my_model.boundary_.add_bc(feb.boundary.BCZeroDisplacement(node_set="bottom", x_dof=1, y_dof=1, z_dof=1))
    displacement_bcs = feb.boundary.Boundary()
    displacement_bcs.add_bc(feb.boundary.BCPrescribedDisplacement(node_set="top", dof="z", value=feb.boundary.Value(lc=1, text=0.1)))
    my_model.step_.add_step(feb.step.StepEntry(id=1, name="displacement", boundary=displacement_bcs))
    force_step_loads = feb.loads.Loads()
    force_step_loads.add_nodal_load(feb.loads.NodalLoad(node_set="top", relative=1, dof="z", scale=feb.loads.Scale(lc=2, text=0.05)))
    my_model.step_.add_step(feb.step.StepEntry(id=2, name="force", loads=force_step_loads))
    my_model.loaddata_.add_load_curve(feb.loaddata.LoadCurve(id=1, points=feb.loaddata.CurvePoints(points=["0,0", "1.0,1"])))
    my_model.loaddata_.add_load_curve(feb.loaddata.LoadCurve(id=2, points=feb.loaddata.CurvePoints(points=["1,0", "2.0,1"])))
    my_model.save(tmp_path.joinpath("MultistepModel.feb"))
    result = feb.model.run_model(f"{tmp_path.joinpath('MultistepModel.feb')}", silent=False)
    assert result == 0, "MultistepModel.feb failed to run."
