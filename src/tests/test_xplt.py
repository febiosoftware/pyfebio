from pathlib import Path

from pyfebio import xplt


def test_read_xplt(tmp_path):
    xplt.to_hdf5(Path(__file__).parent.joinpath("../../assets/elastic_hex20.xplt").as_posix(), tmp_path / "elastic_hex20.hdf5")


def test_read_xplt_unnamed_domains(rigid_body_febmesh, tmp_path):
    """
    FEBio names only solid domains in the plot file. Discrete and shell domains do not have
    names. We are using the names as keys in our data dictionary, and thus things were breaking for discrete
    and shell domains. For shell and discrete data, we now simply enumerate the key based on its domain index.
    """
    import h5py

    import pyfebio as feb

    model = feb.model.Model(mesh_=rigid_body_febmesh)
    body_a, body_b = (element.name for element in model.mesh_.elements)
    model.material_.add_material(feb.material.RigidBody(name=body_b))  # material 1 -> second domain
    model.material_.add_material(feb.material.NeoHookean(name=body_a))  # material 2 -> first domain
    for name in (body_a, body_b):
        model.meshdomains_.add_solid_domain(feb.meshdomains.SolidDomain(name=name, mat=name))
    model.mesh_.add_node_set(feb.mesh.NodeSet(name="base", text="1,2,3,4"))
    model.boundary_.add_bc(feb.boundary.BCZeroDisplacement(node_set="base", x_dof=1, y_dof=1, z_dof=1))
    model.rigid_.add_rigid_bc(feb.rigid.RigidFixed(rb=body_b, Rx_dof=1, Ry_dof=1, Ru_dof=1, Rv_dof=1, Rw_dof=1))
    model.rigid_.add_rigid_bc(feb.rigid.RigidPrescribed(rb=body_b, dof="z", value=feb.rigid.Value(lc=1, text=1.0)))
    model.loaddata_.add_load_curve(feb.loaddata.LoadCurve(id=1, points=feb.loaddata.CurvePoints(points=["0.0,0.0", "1.0,0.5"])))
    springs = [feb.mesh.DiscreteElement(text=f"{a},{a + 4}") for a in (5, 6, 7, 8)]  # body_a top to body_b bottom
    model.mesh_.add_discrete_set(feb.mesh.DiscreteSet(name="spring", elements=springs))
    model.discrete_.add_discrete_material(feb.discrete.Spring(id=1, name="spring"))
    model.discrete_.add_discrete_element(feb.discrete.DiscreteEntry(dmat=1, discrete_set="spring"))
    plot_vars = ("displacement", "stress", "discrete element force")
    model.output_.add_plotfile(feb.output.OutputPlotfile(all_vars=[feb.output.Var(type=v) for v in plot_vars]))
    model_path = tmp_path / "unnamed_domains.feb"
    model.save(model_path)
    assert feb.model.run_model(model_path, silent=True) == 0

    xplt.to_hdf5(model_path.with_suffix(".xplt").as_posix(), tmp_path / "unnamed_domains.hdf5")
    with h5py.File(tmp_path / "unnamed_domains.hdf5") as f:
        names = set(f["meshes/0/domains"])
        assert {body_a, body_b} <= names
        unnamed = [n for n in names if n.startswith("domain")]
        assert len(unnamed) == 1, names
        last = f["states"][max(f["states"], key=int)]
        # Only the deformable body has stress, and it must be filed under its own name.
        assert set(last["element_data/stress"]) == {body_a}
        assert set(last["element_data/discrete element force"]) == set(unnamed)
        assert last[f"element_data/discrete element force/{unnamed[0]}"].shape == (4, 3)


def test_read_xplt_large_surface(tmp_path):
    """
    A surface's face list should have been a dataset, not an attribute as before:
    HDF5 attributes are limited to 64 KiB, which a surface of a few thousand faces exceeds.
    """
    import h5py
    import numpy as np

    import pyfebio as feb

    n = 60  # 60 x 60 = 3600 quad faces on top of a one-element-thick plate
    xs = np.linspace(0.0, 1.0, n + 1)
    grid = np.array([[x, y] for y in xs for x in xs])
    points = np.vstack([np.column_stack([grid, np.zeros(len(grid))]), np.column_stack([grid, np.full(len(grid), 0.1)])])
    layer = (n + 1) ** 2
    corners = np.array(
        [
            [j * (n + 1) + i + 1, j * (n + 1) + i + 2, (j + 1) * (n + 1) + i + 2, (j + 1) * (n + 1) + i + 1]
            for j in range(n)
            for i in range(n)
        ]
    )
    hexes = np.hstack([corners, corners + layer])
    model = feb.model.Model()
    model.mesh_.add_node_domain(feb.mesh.numpy_to_nodes(points, name="plate"))
    model.mesh_.add_element_domain(feb.mesh.numpy_to_elements(hexes, "hex8", name="plate"))
    model.mesh_.add_surface(feb.mesh.Surface(name="top", all_quad4=feb.mesh.numpy_to_surface_list(corners + layer, "quad4")))
    model.mesh_.add_node_set(feb.mesh.NodeSet(name="bottom", text=",".join(map(str, np.unique(corners)))))
    model.material_.add_material(feb.material.NeoHookean(name="plate"))
    model.meshdomains_.add_solid_domain(feb.meshdomains.SolidDomain(name="plate", mat="plate"))
    model.boundary_.add_bc(feb.boundary.BCZeroDisplacement(node_set="bottom", x_dof=1, y_dof=1, z_dof=1))
    model.loaddata_.add_load_curve(feb.loaddata.LoadCurve(id=1, points=feb.loaddata.CurvePoints(points=["0.0,0.0", "1.0,1.0"])))
    model.loads_.add_surface_load(feb.loads.PressureLoad(surface="top", pressure=feb.loads.Scale(lc=1, text=0.01)))
    model.output_.add_plotfile(feb.output.OutputPlotfile(all_vars=[feb.output.Var(type="displacement")]))
    model_path = tmp_path / "large_surface.feb"
    model.save(model_path)
    assert feb.model.run_model(model_path, silent=True) == 0

    xplt.to_hdf5(model_path.with_suffix(".xplt").as_posix(), tmp_path / "large_surface.hdf5")
    with h5py.File(tmp_path / "large_surface.hdf5") as f:
        assert len(f["meshes/0/surfaces/top"]) == n * n
