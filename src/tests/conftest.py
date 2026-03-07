from pathlib import Path

import meshio
import numpy as np
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
def penta6_febmesh() -> mesh.Mesh:
    theta = np.linspace(0.0, 2 * np.pi, 8)
    x = np.cos(theta)
    y = np.sin(theta)
    nodes = [mesh.Node(id=i + 1, text=",".join(map(str, [x[i], y[i], 0.0]))) for i in range(len(x) - 1)]
    nodes += [mesh.Node(id=i + len(x), text=",".join(map(str, [x[i], y[i], 1.0]))) for i in range(len(x) - 1)]
    nodes += [mesh.Node(id=len(nodes) + 1, text="0.0,0.0,0.0"), mesh.Node(id=len(nodes) + 2, text="0.0,0.0,1.0")]

    elements = [
        [15, 1, 2, 16, 8, 9],
        [15, 2, 3, 16, 9, 10],
        [15, 3, 4, 16, 10, 11],
        [15, 4, 5, 16, 11, 12],
        [15, 5, 6, 16, 12, 13],
        [15, 6, 7, 16, 13, 14],
        [15, 7, 1, 16, 14, 8],
    ]
    elements = [mesh.Penta6Element(id=i + 1, text=",".join(map(str, elem))) for i, elem in enumerate(elements)]
    mesh_obj = mesh.Mesh(
        nodes=(mesh.Nodes(all_nodes=nodes),),
        elements=[mesh.Elements(name="penta_mesh", type="penta6", all_elements=elements)],  # type:ignore
    )
    mesh_obj.node_sets = [
        mesh.NodeSet(name="bottom", text="1,2,3,4,5,6,7,15"),
        mesh.NodeSet(name="top", text="8,9,10,11,12,13,14,16"),
    ]
    return mesh_obj


@pytest.fixture(scope="session")
def beam2_febmesh() -> mesh.Mesh:
    node_list = [[0.0, 0.0, 0.0], [0.5, 0.0, 0.0], [1.0, 0.0, 0.0], [0.25, 1.0, 0.0], [0.75, 1.0, 0.0]]
    element_list = [[1, 2], [2, 3], [1, 4], [4, 5], [4, 2], [5, 2], [5, 3]]
    mesh_obj = mesh.Mesh(
        nodes=(mesh.Nodes(all_nodes=[mesh.Node(id=i + 1, text=",".join(map(str, node))) for (i, node) in enumerate(node_list)]),)
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
        nodes=(
            mesh.Nodes(
                all_nodes=[mesh.Node(id=1, text="0.0,0.0,0.0"), mesh.Node(id=2, text="0.5,0.0,0.0"), mesh.Node(id=3, text="1.0,0.0,0.0")]
            ),
        )
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

    mesh_obj = mesh.Mesh(
        nodes=(mesh.Nodes(all_nodes=[mesh.Node(id=i + 1, text=",".join(map(str, node))) for i, node in enumerate(nodes)]),)
    )

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


@pytest.fixture(scope="session")
def shell_tri3():
    nodes = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0], [1.0, 0.0, 1.0]]
    elements = [[1, 2, 3], [2, 4, 3]]
    mesh_obj = mesh.Mesh(
        nodes=(mesh.Nodes(all_nodes=[mesh.Node(id=i + 1, text=",".join(map(str, node))) for i, node in enumerate(nodes)]),)
    )
    mesh_obj.elements = [
        mesh.Elements(
            type="tri3", all_elements=[mesh.Tri3Element(id=i + 1, text=",".join(map(str, elm))) for i, elm in enumerate(elements)]
        )
    ]
    mesh_obj.node_sets = [
        mesh.NodeSet(name="bottom", text="1,2"),
        mesh.NodeSet(name="top", text="3,4"),
        mesh.NodeSet(name="left", text="1,3"),
        mesh.NodeSet(name="right", text="2,4"),
        mesh.NodeSet(name="bottom-left", text="1"),
        mesh.NodeSet(name="bottom-right", text="2"),
        mesh.NodeSet(name="top-right", text="4"),
        mesh.NodeSet(name="top-left", text="3"),
    ]
    mesh_obj.edges = [
        mesh.Edge(name="bottom", all_line2=[mesh.Line2Element(id=1, text="1,2")]),
        mesh.Edge(name="top", all_line2=[mesh.Line2Element(id=2, text="4,3")]),
        mesh.Edge(name="left", all_line2=[mesh.Line2Element(id=3, text="3,1")]),
        mesh.Edge(name="right", all_line2=[mesh.Line2Element(id=4, text="2,4")]),
    ]
    return mesh_obj


@pytest.fixture(scope="session")
def shell_tri6():
    nodes = [
        [0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0],
        [0.5, 0.0, 0.0],
        [0.5, 0.0, 0.5],
        [0.0, 0.0, 0.5],
        [1.0, 0.0, 1.0],
        [1.0, 0.0, 0.5],
        [0.5, 0.0, 1.0],
    ]
    elements = [
        [1, 2, 3, 4, 5, 6],
        [2, 7, 3, 8, 9, 5],
    ]
    mesh_obj = mesh.Mesh(
        nodes=(mesh.Nodes(all_nodes=[mesh.Node(id=i + 1, text=",".join(map(str, node))) for i, node in enumerate(nodes)]),)
    )
    mesh_obj.elements = [
        mesh.Elements(
            type="tri6", all_elements=[mesh.Tri6Element(id=i + 1, text=",".join(map(str, elm))) for i, elm in enumerate(elements)]
        )
    ]
    mesh_obj.node_sets = [
        mesh.NodeSet(name="bottom", text="1,2,4"),
        mesh.NodeSet(name="top", text="3,4,9"),
        mesh.NodeSet(name="left", text="1,3,6"),
        mesh.NodeSet(name="right", text="2,4,8"),
        mesh.NodeSet(name="bottom-left", text="1"),
        mesh.NodeSet(name="bottom-right", text="2"),
        mesh.NodeSet(name="top-right", text="7"),
        mesh.NodeSet(name="top-left", text="3"),
    ]
    mesh_obj.edges = [
        mesh.Edge(name="bottom", all_line3=[mesh.Line3Element(id=1, text="1,2,4")]),
        mesh.Edge(name="top", all_line3=[mesh.Line3Element(id=2, text="4,3,9")]),
        mesh.Edge(name="left", all_line3=[mesh.Line3Element(id=3, text="3,1,6")]),
        mesh.Edge(name="right", all_line3=[mesh.Line3Element(id=4, text="2,4,8")]),
    ]
    return mesh_obj


@pytest.fixture(scope="session")
def shell_quad4():
    nodes = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 0.0, 1.0], [0.0, 0.0, 1.0]]
    elements = [[1, 2, 3, 4]]
    mesh_obj = mesh.Mesh(
        nodes=(mesh.Nodes(all_nodes=[mesh.Node(id=i + 1, text=",".join(map(str, node))) for i, node in enumerate(nodes)]),)
    )
    mesh_obj.elements = [
        mesh.Elements(
            type="quad4", all_elements=[mesh.Quad4Element(id=i + 1, text=",".join(map(str, elm))) for i, elm in enumerate(elements)]
        )
    ]
    mesh_obj.node_sets = [
        mesh.NodeSet(name="bottom", text="1,2"),
        mesh.NodeSet(name="top", text="3,4"),
        mesh.NodeSet(name="left", text="1,4"),
        mesh.NodeSet(name="right", text="2,3"),
        mesh.NodeSet(name="bottom-left", text="1"),
        mesh.NodeSet(name="bottom-right", text="2"),
        mesh.NodeSet(name="top-right", text="3"),
        mesh.NodeSet(name="top-left", text="4"),
    ]
    mesh_obj.edges = [
        mesh.Edge(name="bottom", all_line2=[mesh.Line2Element(id=1, text="1,2")]),
        mesh.Edge(name="top", all_line2=[mesh.Line2Element(id=2, text="3,4")]),
        mesh.Edge(name="left", all_line2=[mesh.Line2Element(id=3, text="4,1")]),
        mesh.Edge(name="right", all_line2=[mesh.Line2Element(id=4, text="2,3")]),
    ]
    return mesh_obj


@pytest.fixture(scope="session")
def shell_quad8():
    nodes = [
        [0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [1.0, 0.0, 1.0],
        [0.0, 0.0, 1.0],
        [0.5, 0.0, 0.0],
        [1.0, 0.0, 0.5],
        [0.5, 0.0, 1.0],
        [0.0, 0.0, 0.5],
    ]
    elements = [[1, 2, 3, 4, 5, 6, 7, 8]]
    mesh_obj = mesh.Mesh(
        nodes=(mesh.Nodes(all_nodes=[mesh.Node(id=i + 1, text=",".join(map(str, node))) for i, node in enumerate(nodes)]),)
    )
    mesh_obj.elements = [
        mesh.Elements(
            type="quad8", all_elements=[mesh.Quad8Element(id=i + 1, text=",".join(map(str, elm))) for i, elm in enumerate(elements)]
        )
    ]
    mesh_obj.node_sets = [
        mesh.NodeSet(name="bottom", text="1,2,5"),
        mesh.NodeSet(name="top", text="3,4,7"),
        mesh.NodeSet(name="left", text="1,4,8"),
        mesh.NodeSet(name="right", text="2,3,6"),
        mesh.NodeSet(name="bottom-left", text="1"),
        mesh.NodeSet(name="bottom-right", text="2"),
        mesh.NodeSet(name="top-right", text="3"),
        mesh.NodeSet(name="top-left", text="4"),
    ]
    mesh_obj.edges = [
        mesh.Edge(name="bottom", all_line3=[mesh.Line3Element(id=1, text="1,2,5")]),
        mesh.Edge(name="top", all_line3=[mesh.Line3Element(id=2, text="3,4,7")]),
        mesh.Edge(name="left", all_line3=[mesh.Line3Element(id=3, text="4,1,8")]),
        mesh.Edge(name="right", all_line3=[mesh.Line3Element(id=4, text="2,3,6")]),
    ]
    return mesh_obj


@pytest.fixture(scope="session")
def shell_quad9():
    nodes = [
        [0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [1.0, 0.0, 1.0],
        [0.0, 0.0, 1.0],
        [0.5, 0.0, 0.0],
        [1.0, 0.0, 0.5],
        [0.5, 0.0, 1.0],
        [0.0, 0.0, 0.5],
        [0.5, 0.0, 0.5],
    ]
    elements = [[1, 2, 3, 4, 5, 6, 7, 8, 9]]
    mesh_obj = mesh.Mesh(
        nodes=(mesh.Nodes(all_nodes=[mesh.Node(id=i + 1, text=",".join(map(str, node))) for i, node in enumerate(nodes)]),)
    )
    mesh_obj.elements = [
        mesh.Elements(
            type="quad9", all_elements=[mesh.Quad9Element(id=i + 1, text=",".join(map(str, elm))) for i, elm in enumerate(elements)]
        )
    ]
    mesh_obj.node_sets = [
        mesh.NodeSet(name="bottom", text="1,2,5"),
        mesh.NodeSet(name="top", text="3,4,7"),
        mesh.NodeSet(name="left", text="1,4,8"),
        mesh.NodeSet(name="right", text="2,3,6"),
        mesh.NodeSet(name="bottom-left", text="1"),
        mesh.NodeSet(name="bottom-right", text="2"),
        mesh.NodeSet(name="top-right", text="3"),
        mesh.NodeSet(name="top-left", text="4"),
    ]
    mesh_obj.edges = [
        mesh.Edge(name="bottom", all_line3=[mesh.Line3Element(id=1, text="1,2,5")]),
        mesh.Edge(name="top", all_line3=[mesh.Line3Element(id=2, text="3,4,7")]),
        mesh.Edge(name="left", all_line3=[mesh.Line3Element(id=3, text="4,1,8")]),
        mesh.Edge(name="right", all_line3=[mesh.Line3Element(id=4, text="2,3,6")]),
    ]
    return mesh_obj


@pytest.fixture(scope="session")
def tet15_febmesh():
    nodes = [
        np.array([-1, -1 / np.sqrt(3), -1]),
        np.array([1, -1 / np.sqrt(3), -1]),
        np.array([0, 2 / np.sqrt(3), -1]),
        np.array([0, 0, 1 / np.sqrt(3)]),
    ]
    nodes += [(nodes[0] + nodes[1]) / 2.0, (nodes[1] + nodes[2]) / 2.0, (nodes[2] + nodes[0]) / 2.0]
    nodes += [(nodes[0] + nodes[3]) / 2.0, (nodes[1] + nodes[3]) / 2.0, (nodes[2] + nodes[3]) / 2.0]
    nodes += [
        (nodes[0] + nodes[1] + nodes[2]) / 3.0,
        (nodes[0] + nodes[1] + nodes[3]) / 3.0,
        (nodes[1] + nodes[2] + nodes[3]) / 3.0,
        (nodes[0] + nodes[2] + nodes[3]) / 3.0,
    ]
    nodes += [(nodes[0] + nodes[1] + nodes[2] + nodes[3]) / 4.0]
    nodes = [mesh.Node(id=i + 1, text=",".join(map(str, node))) for i, node in enumerate(nodes)]
    mesh_obj = mesh.Mesh(
        nodes=(mesh.Nodes(name="tet15", all_nodes=nodes),),
        elements=[
            mesh.Elements(
                name="tet15", type="tet15", all_elements=[mesh.Tet15Element(id=1, text=",".join([str(i + 1) for i in range(15)]))]
            )
        ],
    )
    mesh_obj.node_sets = [mesh.NodeSet(name="top", text="4"), mesh.NodeSet(name="bottom", text="1,2,3,5,6,7,14")]
    return mesh_obj


@pytest.fixture(scope="session")
def pyra5_febmesh():
    nodes = [[-0.5, -0.5, 0.0], [0.5, -0.5, 0.0], [0.5, 0.5, 0.0], [-0.5, 0.5, 0.0], [0.0, 0.0, 1.0 / np.sqrt(2.0)]]
    nodes = [mesh.Node(id=i + 1, text=",".join(map(str, node))) for i, node in enumerate(nodes)]
    mesh_obj = mesh.Mesh(
        nodes=(mesh.Nodes(name="pyra5", all_nodes=nodes),),
        elements=[
            mesh.Elements(name="pyra5", type="pyra5", all_elements=[mesh.Pyra5Element(id=1, text=",".join([str(i + 1) for i in range(5)]))])
        ],
    )
    mesh_obj.node_sets = [mesh.NodeSet(name="top", text="5"), mesh.NodeSet(name="bottom", text="1,2,3,4")]
    return mesh_obj
