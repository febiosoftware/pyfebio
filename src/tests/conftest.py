from pathlib import Path

import meshio
import pytest

from pyfebio import mesh

GMSH_DIR = Path(__file__).parent.joinpath("../../assets/gmsh")

SOLID_SETS = ["bottom-layer", "top-layer"]
SURFACE_ELEMENTS = ["bottom", "top", "left", "right", "front", "back"]


@pytest.fixture(scope="session")
def tet4_meshio() -> meshio.Mesh:
    return meshio.gmsh.read(GMSH_DIR.joinpath("tet4.msh"))


@pytest.fixture(scope="session")
def tet10_meshio() -> meshio.Mesh:
    return meshio.gmsh.read(GMSH_DIR.joinpath("tet10.msh"))


@pytest.fixture(scope="session")
def hex8_meshio() -> meshio.Mesh:
    return meshio.gmsh.read(GMSH_DIR.joinpath("hex8.msh"))


@pytest.fixture(scope="session")
def hex20_meshio() -> meshio.Mesh:
    return meshio.gmsh.read(GMSH_DIR.joinpath("hex20.msh"))


@pytest.fixture(scope="session")
def hex27_meshio() -> meshio.Mesh:
    return meshio.gmsh.read(GMSH_DIR.joinpath("hex27.msh"))


@pytest.fixture(scope="session")
def tet4_febmesh(tet4_meshio) -> mesh.Mesh:
    return mesh.translate_meshio(tet4_meshio)


@pytest.fixture(scope="session")
def tet10_febmesh(tet10_meshio) -> mesh.Mesh:
    return mesh.translate_meshio(tet10_meshio)


@pytest.fixture(scope="session")
def hex8_febmesh(hex8_meshio) -> mesh.Mesh:
    return mesh.translate_meshio(hex8_meshio)


@pytest.fixture(scope="session")
def hex20_febmesh(hex20_meshio) -> mesh.Mesh:
    return mesh.translate_meshio(hex20_meshio)


@pytest.fixture(scope="session")
def hex27_febmesh(hex27_meshio) -> mesh.Mesh:
    return mesh.translate_meshio(hex27_meshio)


@pytest.fixture(scope="session")
def tet4_contact_febmesh() -> mesh.Mesh:
    mesh_obj = meshio.gmsh.read(GMSH_DIR.joinpath("tet4_contact.msh"))
    return mesh.translate_meshio(mesh_obj)


@pytest.fixture(scope="session")
def tet10_contact_febmesh() -> mesh.Mesh:
    mesh_obj = meshio.gmsh.read(GMSH_DIR.joinpath("tet10_contact.msh"))
    return mesh.translate_meshio(mesh_obj)


@pytest.fixture(scope="session")
def hex8_contact_febmesh() -> mesh.Mesh:
    mesh_obj = meshio.read(GMSH_DIR.joinpath("hex8_contact.msh"), file_format="gmsh")
    return mesh.translate_meshio(mesh_obj)


@pytest.fixture(scope="session")
def hex20_contact_febmesh() -> mesh.Mesh:
    mesh_obj = meshio.gmsh.read(GMSH_DIR.joinpath("hex20_contact.msh"))
    return mesh.translate_meshio(mesh_obj)


@pytest.fixture(scope="session")
def hex27_contact_febmesh() -> mesh.Mesh:
    mesh_obj = meshio.gmsh.read(GMSH_DIR.joinpath("hex27_contact.msh"))
    return mesh.translate_meshio(mesh_obj)


@pytest.fixture(scope="session")
def beam2_febmesh() -> mesh.Mesh:
    node_list = [[0.0, 0.0, 0.0], [0.5, 0.0, 0.0], [1.0, 0.0, 0.0], [0.25, 1.0, 0.0], [0.75, 1.0, 0.0]]
    element_list = [[1, 2], [2, 3], [1, 4], [4, 5], [4, 2], [5, 2], [5, 3]]
    mesh_obj = mesh.Mesh(
        nodes=[mesh.Nodes(all_nodes=[mesh.Node(id=i + 1, text=",".join(map(str, node))) for (i, node) in enumerate(node_list)])]
    )
    mesh_obj.elements = [
        mesh.Elements(
            type="line2",
            name="beam",
            all_elements=[mesh.Line2Element(id=i + 1, text=",".join(map(str, elem))) for i, elem in enumerate(element_list)],
        )
    ]
    mesh_obj.node_sets = [mesh.NodeSet(name="bottom", text="1,2,3"), mesh.NodeSet(name="top", text="4,5")]
    return mesh_obj


@pytest.fixture(scope="session")
def beam3_febmesh() -> mesh.Mesh:
    mesh_obj = mesh.Mesh(
        nodes=[
            mesh.Nodes(
                all_nodes=[mesh.Node(id=1, text="0.0,0.0,0.0"), mesh.Node(id=2, text="0.5,0.0,0.0"), mesh.Node(id=3, text="1.0,0.0,0.0")]
            )
        ]
    )
    mesh_obj.elements = [mesh.Elements(type="line3", name="beam", all_elements=[mesh.Line3Element(id=1, text="1,3,2")])]
    mesh_obj.node_sets = [mesh.NodeSet(name="left", text="1"), mesh.NodeSet(name="right", text="3")]
    return mesh_obj


@pytest.fixture(scope="session")
def rigid_body_febmesh():
    nodes = [
        [0.0, 0.0, 0.0],
        [2.0, 0.0, 0.0],
        [2.0, 1.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 4.0],
        [2.0, 0.0, 4.0],
        [2.0, 1.0, 4.0],
        [0.0, 1.0, 4.0],
        [0.0, 0.0, 5.0],
        [2.0, 0.0, 5.0],
        [2.0, 1.0, 5.0],
        [0.0, 1.0, 5.0],
        [0.0, 0.0, 9.0],
        [2.0, 0.0, 9.0],
        [2.0, 1.0, 9.0],
        [0.0, 1.0, 9.0],
    ]
    part1 = [1, 2, 3, 4, 5, 6, 7, 8]
    part2 = [9, 10, 11, 12, 13, 14, 15, 16]

    mesh_obj = mesh.Mesh(nodes=[mesh.Nodes(all_nodes=[mesh.Node(id=i + 1, text=",".join(map(str, node))) for i, node in enumerate(nodes)])])

    mesh_obj.elements = [
        mesh.Elements(type="hex8", name="bodyA", all_elements=[mesh.Hex8Element(id=1, text=",".join(map(str, part1)))]),
        mesh.Elements(type="hex8", name="bodyB", all_elements=[mesh.Hex8Element(id=2, text=",".join(map(str, part2)))]),
    ]

    mesh_obj.node_sets = [
        mesh.NodeSet(name="bodyA_top", text="5,6,7,8"),
        mesh.NodeSet(name="bodyA_bottom", text="1,2,3,4"),
        mesh.NodeSet(name="bodyB_bottom", text="9,10,11,12"),
        mesh.NodeSet(name="bodyB_top", text="13,14,15,16"),
    ]
    return mesh_obj
