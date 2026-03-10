from typing import get_args

import pyfebio as feb


def test_unconstrained_material(hex8_febmesh, tmp_path):
    for material_cls in get_args(feb.material.UnconstrainedMaterials):
        my_model = feb.model.Model(mesh_=hex8_febmesh)
        for i, element in enumerate(my_model.mesh_.elements):
            my_mat = material_cls(name=element.name, id=i + 1)
            if hasattr(my_mat, "mat_axis"):
                my_mat.mat_axis = feb.material.MaterialAxisVector()
            elif hasattr(my_mat, "fiber"):
                my_mat.fiber = feb.material.FiberVector()
            my_model.material_.add_material(my_mat)
            my_model.meshdomains_.add_solid_domain(feb.meshdomains.SolidDomain(name=element.name, mat=element.name))
        model_file = tmp_path.joinpath(f"{my_model.material_.all_materials[0].type.replace(' ', '_')}.feb")
        my_model.save(model_file)
        result = feb.model.run_model(model_file)
        assert result == 0, f"{material_cls.__name__} failed"


def test_efd_donnan_equilibrium(hex8_febmesh, tmp_path):
    my_model = feb.model.Model(mesh_=hex8_febmesh)
    for i, element in enumerate(my_model.mesh_.elements):
        my_mat = feb.material.EllipsoidalFiberDistributionDonnanEquilibrium(
            name=element.name, id=i + 1, cF0=feb.material.DynamicMaterialParameter(lc=i + 1, text=1)
        )
        my_model.material_.add_material(my_mat)
        my_model.meshdomains_.add_solid_domain(feb.meshdomains.SolidDomain(name=element.name, mat=element.name))
        my_model.loaddata_.add_load_curve(feb.loaddata.LoadCurve(id=i + 1, points=feb.loaddata.CurvePoints(points=["0,0", "1,150"])))
    my_model.boundary_.add_bc(feb.boundary.BCZeroDisplacement(node_set="bottom", x_dof=1, y_dof=1, z_dof=1))
    model_file = tmp_path.joinpath(f"{my_model.material_.all_materials[0].type.replace(' ', '_')}.feb")
    my_model.save(model_file)
    result = feb.model.run_model(model_file, silent=True)
    assert result == 0


def test_osmotic_virial_pressure(hex20_febmesh, tmp_path):
    my_model = feb.model.Model(mesh_=hex20_febmesh)
    for i, element in enumerate(my_model.mesh_.elements):
        my_mat = feb.material.SolidMixture(name=element.name, id=i + 1)
        my_mat.add_solid(feb.material.OsmoticVirialPressure(id=i + 1, cr=feb.material.DynamicMaterialParameter(lc=i + 1, text=5000.0)))
        my_mat.add_solid(feb.material.ContinuousFiberDistribution())
        my_model.material_.add_material(my_mat)
        my_model.meshdomains_.add_solid_domain(feb.meshdomains.SolidDomain(name=element.name, mat=element.name))
        my_model.loaddata_.add_load_curve(
            feb.loaddata.LoadCurve(
                id=i + 1,
                interpolate="SMOOTH",
                points=feb.loaddata.CurvePoints(points=["0,0", "1,1"]),
            )
        )
    my_model.boundary_.add_bc(feb.boundary.BCZeroDisplacement(node_set="bottom", x_dof=1, y_dof=1, z_dof=1))
    model_file = tmp_path.joinpath(f"{my_model.material_.all_materials[0].type.replace(' ', '_')}.feb")
    my_model.save(model_file)
    result = feb.model.run_model(model_file, silent=False)
    assert result == 0


def test_perfect_osmometer(hex20_febmesh, tmp_path):
    my_model = feb.model.Model(mesh_=hex20_febmesh)
    for i, element in enumerate(my_model.mesh_.elements):
        my_mat = feb.material.SolidMixture(name=element.name, id=i + 1)
        my_mat.add_solid(
            feb.material.PerfectOsmometer(
                id=i + 1,
                phiw0=feb.material.MaterialParameter(text=0.8),
                iosm=feb.material.MaterialParameter(text=300.0),
                bosm=feb.material.DynamicMaterialParameter(lc=i + 1, text=1.0),
            )
        )
        my_mat.add_solid(
            feb.material.NeoHookean(
                id=i + 1,
                E=feb.material.MaterialParameter(text=1.0),
                v=feb.material.MaterialParameter(text=0.0),
            )
        )
        my_model.material_.add_material(my_mat)
        my_model.meshdomains_.add_solid_domain(feb.meshdomains.SolidDomain(name=element.name, mat=element.name))
        my_model.loaddata_.add_load_curve(feb.loaddata.LoadCurve(id=i + 1, points=feb.loaddata.CurvePoints(points=["0,300", "1,1500"])))
    my_model.globals_.constants.T = 310
    my_model.boundary_.add_bc(feb.boundary.BCZeroDisplacement(node_set="bottom", x_dof=1, y_dof=1, z_dof=1))
    model_file = tmp_path.joinpath(f"{my_model.material_.all_materials[0].type.replace(' ', '_')}.feb")
    my_model.save(model_file)
    result = feb.model.run_model(model_file, silent=False)
    assert result == 0


def test_uncoupled_material(hex8_febmesh, tmp_path):
    for material_cls in get_args(feb.material.UncoupledMaterials):
        my_model = feb.model.Model(mesh_=hex8_febmesh)
        for i, element in enumerate(my_model.mesh_.elements):
            my_mat = material_cls(name=element.name, id=i + 1)
            if hasattr(my_mat, "mat_axis"):
                my_mat.mat_axis = feb.material.MaterialAxisVector()
            elif hasattr(my_mat, "fiber"):
                my_mat.fiber = feb.material.FiberVector()
            my_model.material_.add_material(my_mat)
            my_model.meshdomains_.add_solid_domain(feb.meshdomains.SolidDomain(name=element.name, mat=element.name))
        model_file = tmp_path.joinpath(f"{my_model.material_.all_materials[0].type.replace(' ', '_')}.feb")
        my_model.save(model_file)
        result = feb.model.run_model(model_file, silent=True)
        assert result == 0, f"{material_cls.__name__} failed"


def test_biphasic_material(hex20_febmesh, tmp_path):
    for perm_cls in get_args(feb.material.PermeabilityType):
        my_model = feb.model.BiphasicModel(
            mesh_=hex20_febmesh,
        )
        for i, element in enumerate(my_model.mesh_.elements):
            my_mat = feb.material.BiphasicMaterial(name=element.name, id=i + 1, permeability=perm_cls())
            my_model.material_.add_material(my_mat)
            my_model.meshdomains_.add_solid_domain(feb.meshdomains.SolidDomain(name=element.name, mat=element.name))
        model_file = tmp_path.joinpath(f"{perm_cls.__name__}.feb")
        fixed_bottom = feb.boundary.BCZeroDisplacement(node_set="bottom", x_dof=1, y_dof=1, z_dof=1)
        move_top = feb.boundary.BCPrescribedDisplacement(node_set="top", dof="z", value=feb.boundary.Value(lc=1, text=-0.5))
        fix_top = feb.boundary.BCZeroDisplacement(node_set="top", x_dof=1, y_dof=1, z_dof=0)
        draining_surface = feb.boundary.BCZeroFluidPressure(node_set="top")
        my_model.boundary_.add_bc(fixed_bottom)
        my_model.boundary_.add_bc(move_top)
        my_model.boundary_.add_bc(fix_top)
        my_model.boundary_.add_bc(draining_surface)
        my_model.loaddata_.add_load_curve(
            feb.loaddata.LoadCurve(id=1, points=feb.loaddata.CurvePoints(points=["0,0", "0.1,1.0", "1.0,1.0"]))
        )
        my_model.output_.add_plotfile(
            feb.output.OutputPlotfile(
                all_vars=[
                    feb.output.Var(type="displacement"),
                    feb.output.Var(type="fluid pressure"),
                    feb.output.Var(type="fluid flux"),
                ]
            )
        )

        my_model.save(model_file)
        result = feb.model.run_model(model_file, silent=False)
        assert result == 0, f"{perm_cls.__name__} failed"


def test_unconstrained_fiber_materials(hex8_febmesh, tmp_path):
    for fiber_model in get_args(feb.material.FiberModel):
        my_model = feb.model.Model(mesh_=hex8_febmesh)
        for i, element in enumerate(my_model.mesh_.elements):
            ground = feb.material.CoupledMooneyRivlin(
                c1=feb.material.MaterialParameter(text=0.1),
                c2=feb.material.MaterialParameter(text=0.0),
                k=feb.material.MaterialParameter(text=10.0),
            )
            fibers = fiber_model(fiber=feb.material.FiberVector())
            mat = feb.material.SolidMixture(id=i + 1, name=element.name, solid_list=[ground, fibers])
            my_model.material_.add_material(mat)
            my_model.meshdomains_.add_solid_domain(feb.meshdomains.SolidDomain(name=element.name, mat=element.name))
        fixed_bottom = feb.boundary.BCZeroDisplacement(node_set="bottom", x_dof=1, y_dof=1, z_dof=1)
        move_top = feb.boundary.BCPrescribedDisplacement(node_set="top", dof="z", value=feb.boundary.Value(lc=1, text=-0.5))
        move_top_lc = feb.loaddata.LoadCurve(id=1, points=feb.loaddata.CurvePoints(points=["0,0", "1,1"]))
        my_model.boundary_.add_bc(fixed_bottom)
        my_model.boundary_.add_bc(move_top)
        my_model.loaddata_.add_load_curve(move_top_lc)
        model_file = tmp_path.joinpath(f"{fiber_model.__name__}.feb")
        my_model.save(model_file)
        result = feb.model.run_model(model_file, silent=False)
        assert result == 0, f"{fiber_model.__name__} failed"


def test_uncoupled_fiber_materials(hex8_febmesh, tmp_path):
    for fiber_model in get_args(feb.material.FiberModelUC):
        my_model = feb.model.Model(mesh_=hex8_febmesh)
        for i, element in enumerate(my_model.mesh_.elements):
            ground = feb.material.MooneyRivlinUC(
                c1=feb.material.MaterialParameter(text=0.1), c2=feb.material.MaterialParameter(text=0.0), k=None
            )
            fibers = fiber_model(fiber=feb.material.FiberVector())
            mat = feb.material.SolidMixtureUC(
                id=i + 1, name=element.name, solid_list=[ground, fibers], k=feb.material.MaterialParameter(text=10.0)
            )
            my_model.material_.add_material(mat)
            my_model.meshdomains_.add_solid_domain(feb.meshdomains.SolidDomain(name=element.name, mat=element.name))
        fixed_bottom = feb.boundary.BCZeroDisplacement(node_set="bottom", x_dof=1, y_dof=1, z_dof=1)
        move_top = feb.boundary.BCPrescribedDisplacement(node_set="top", dof="z", value=feb.boundary.Value(lc=1, text=-0.5))
        move_top_lc = feb.loaddata.LoadCurve(id=1, points=feb.loaddata.CurvePoints(points=["0,0", "1,1"]))
        my_model.boundary_.add_bc(fixed_bottom)
        my_model.boundary_.add_bc(move_top)
        my_model.loaddata_.add_load_curve(move_top_lc)
        model_file = tmp_path.joinpath(f"{fiber_model.__name__}.feb")
        my_model.save(model_file)
        result = feb.model.run_model(model_file, silent=False)
        assert result == 0, f"{fiber_model.__name__} failed"


def test_viscoelastic_material(hex20_febmesh, tmp_path):
    my_model = feb.model.Model(
        mesh_=hex20_febmesh,
    )
    for i, element in enumerate(my_model.mesh_.elements):
        my_mat = feb.material.ViscoelasticMaterial(
            name=element.name,
            id=i + 1,
            g1=feb.material.MaterialParameter(text=0.95),
            t1=feb.material.MaterialParameter(text=0.01),
        )
        my_model.material_.add_material(my_mat)
        my_model.meshdomains_.add_solid_domain(feb.meshdomains.SolidDomain(name=element.name, mat=element.name))
    model_file = tmp_path.joinpath("viscoelastic.feb")
    fixed_bottom = feb.boundary.BCZeroDisplacement(node_set="bottom", x_dof=1, y_dof=1, z_dof=1)
    move_top = feb.boundary.BCPrescribedDisplacement(node_set="top", dof="z", value=feb.boundary.Value(lc=1, text=-0.5))
    my_model.boundary_.add_bc(fixed_bottom)
    my_model.boundary_.add_bc(move_top)
    my_model.loaddata_.add_load_curve(
        feb.loaddata.LoadCurve(
            id=1,
            interpolate="SMOOTH",
            points=feb.loaddata.CurvePoints(points=["0,0", "0.1,1.0", "0.3,-1.0", "0.5,1.0", "0.7,-1.0", "0.9,1.0", "1.0,0.0"]),
        )
    )

    my_model.save(model_file)
    result = feb.model.run_model(model_file, silent=False)
    assert result == 0


def test_viscoelastic_uc_material(hex20_febmesh, tmp_path):
    my_model = feb.model.Model(
        mesh_=hex20_febmesh,
    )
    for i, element in enumerate(my_model.mesh_.elements):
        my_mat = feb.material.ViscoelasticMaterialUC(
            name=element.name,
            id=i + 1,
            g1=feb.material.MaterialParameter(text=0.95),
            t1=feb.material.MaterialParameter(text=0.01),
        )
        my_model.material_.add_material(my_mat)
        my_model.meshdomains_.add_solid_domain(feb.meshdomains.SolidDomain(name=element.name, mat=element.name))
    model_file = tmp_path.joinpath("viscoelastic_uc.feb")
    fixed_bottom = feb.boundary.BCZeroDisplacement(node_set="bottom", x_dof=1, y_dof=1, z_dof=1)
    move_top = feb.boundary.BCPrescribedDisplacement(node_set="top", dof="z", value=feb.boundary.Value(lc=1, text=-0.5))
    my_model.boundary_.add_bc(fixed_bottom)
    my_model.boundary_.add_bc(move_top)
    my_model.loaddata_.add_load_curve(
        feb.loaddata.LoadCurve(
            id=1,
            interpolate="SMOOTH",
            points=feb.loaddata.CurvePoints(points=["0,0", "0.1,1.0", "0.3,-1.0", "0.5,1.0", "0.7,-1.0", "0.9,1.0", "1.0,0.0"]),
        )
    )

    my_model.save(model_file)
    result = feb.model.run_model(model_file, silent=False)
    assert result == 0


def test_multiphasic_model(hex20_febmesh, tmp_path):
    my_model = feb.model.MultiphasicModel(
        mesh_=hex20_febmesh,
    )
    my_model.control_.analysis = "STEADY-STATE"
    my_model.control_.time_steps = 10
    my_model.control_.step_size = 0.1
    my_model.globals_.solutes = feb.globals.Solutes(
        solute=[feb.globals.Solute(id=1, name="Na", charge_number=1), feb.globals.Solute(id=2, name="Cl", charge_number=-1)]
    )
    for i, element in enumerate(my_model.mesh_.elements):
        my_mat = feb.material.MultiphasicMaterial(
            id=i + 1,
            permeability=feb.material.ConstantIsoPerm(perm=feb.material.MaterialParameter(text=9.14e-4)),
            fixed_charge_density=feb.material.DynamicMaterialParameter(lc=3, text=1),
            name=element.name,
            solute=[
                feb.material.Solute(
                    sol=1,
                    diffusivity=feb.material.Diffusivity(
                        free_diff=feb.material.MaterialParameter(text=5.0e-4), diff=feb.material.MaterialParameter(text=5e-4)
                    ),
                    solubility=feb.material.Solubility(),
                ),
                feb.material.Solute(
                    sol=2,
                    diffusivity=feb.material.Diffusivity(
                        free_diff=feb.material.MaterialParameter(text=8.0e-4), diff=feb.material.MaterialParameter(text=8e-4)
                    ),
                    solubility=feb.material.Solubility(),
                ),
            ],
        )
        my_model.material_.add_material(my_mat)
        my_model.meshdomains_.add_solid_domain(feb.meshdomains.SolidDomain(name=element.name, mat=element.name))
    my_model.mesh_.add_node_set(
        feb.mesh.NodeSet(name="all", text=",".join([str(i + 1) for i in range(len(my_model.mesh_.nodes[0].all_nodes))]))
    )
    ic_sodium = feb.initial.InitialConcentration(dof="c1", node_set="all", value=150.0)
    ic_calcium = feb.initial.InitialConcentration(dof="c2", node_set="all", value=150.0)
    my_model.initial_.add_initial_condition(ic_sodium)
    my_model.initial_.add_initial_condition(ic_calcium)
    fixed_bottom = feb.boundary.BCZeroDisplacement(node_set="bottom", x_dof=1, y_dof=1, z_dof=1)
    prescribed_conc_top1 = feb.boundary.BCPrescribedConcentration(node_set="top", dof="c1", value=feb.boundary.Value(lc=1, text=1))
    prescribed_conc_top2 = feb.boundary.BCPrescribedConcentration(node_set="top", dof="c2", value=feb.boundary.Value(lc=1, text=1))
    prescribed_fluid_pressure = feb.boundary.BCPrescribedFluidPressure(node_set="top", value=feb.boundary.Value(lc=2, text=1.0))
    my_model.boundary_.add_bc(fixed_bottom)
    my_model.boundary_.add_bc(prescribed_conc_top1)
    my_model.boundary_.add_bc(prescribed_conc_top2)
    my_model.boundary_.add_bc(prescribed_fluid_pressure)
    my_model.loaddata_.add_load_curve(
        feb.loaddata.LoadCurve(id=1, interpolate="STEP", points=feb.loaddata.CurvePoints(points=["0,0", "1.0,150.0"]))
    )
    my_model.loaddata_.add_load_curve(
        feb.loaddata.LoadCurve(id=2, interpolate="STEP", points=feb.loaddata.CurvePoints(points=["0,0", "1.0,-0.73084"]))
    )
    my_model.loaddata_.add_load_curve(
        feb.loaddata.LoadCurve(id=3, interpolate="LINEAR", points=feb.loaddata.CurvePoints(points=["0,0", "1.0,-200.0"]))
    )
    my_model.output_.add_plotfile(
        feb.output.OutputPlotfile(
            all_vars=[
                feb.output.Var(type="displacement"),
                feb.output.Var(type="fluid pressure"),
                feb.output.Var(type="fluid flux"),
                feb.output.Var(type="solute concentration"),
            ]
        )
    )
    model_file = tmp_path.joinpath("Multiphasic.feb")
    my_model.save(model_file)
    result = feb.model.run_model(model_file, silent=False)
    assert result == 0, "Multiphasic.feb failed"
