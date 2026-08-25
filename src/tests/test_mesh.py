import pytest
from meshio import Mesh
from pydantic import ValidationError

import pyfebio as feb

NODE_STRINGS = (
    "-1.0,-1.0,-1.0",
    "1.0,-1.0,-1.0",
    "1.0,1.0,-1.0",
    "-1.0,1.0,-1.0",
    "-1.0,-1.0,1.0",
    "1.0,-1.0,1.0",
    "1.0,1.0,1.0",
    "-1.0,1.0,1.0",
    "0.0,0.0,2.0",
)

TET4_ELEMENT_STRINGS = ("1,2,3,5",)
PENTA6_ELEMENT_STRINGS = ("1,2,3,4,5,8",)
HEX8_ELEMENT_STRINGS = ("1,2,3,4,5,6,7,8",)

TRI3_ELEMENT_STRINGS = ("1,2,3",)
QUAD4_ELEMENT_STRINGS = ("1,2,3,4",)


def test_node_definition():
    _ = feb.mesh.Node(id=1, text=NODE_STRINGS[0])
    with pytest.raises(ValidationError):
        _ = feb.mesh.Node(id=1, text=("1.,2.,3.,4."))


def test_bad_node_append():
    mesh_obj = feb.mesh.Mesh(nodes=[feb.mesh.Nodes(all_nodes=[feb.mesh.Node(id=1, text=NODE_STRINGS[0])])])
    with pytest.raises(ValidationError):
        mesh_obj.add_node_domain(feb.mesh.Nodes(all_nodes=[feb.mesh.Node(id=1, text="1.0")]))


def test_nodes_definition():
    nodes = feb.mesh.Nodes(name="Nodes1")
    for i, n in enumerate(NODE_STRINGS):
        nodes.add_node(feb.mesh.Node(id=i, text=n))


def test_tet4_element_definition():
    _ = feb.mesh.Tet4Element(id=1, text=TET4_ELEMENT_STRINGS[0])
    with pytest.raises(ValidationError):
        _ = feb.mesh.Tet4Element(id=1, text=HEX8_ELEMENT_STRINGS[0])


def test_penta6_element_definition():
    _ = feb.mesh.Penta6Element(id=1, text=PENTA6_ELEMENT_STRINGS[0])
    with pytest.raises(ValidationError):
        _ = feb.mesh.Penta6Element(id=1, text=HEX8_ELEMENT_STRINGS[0])


def test_hex8_element_definition():
    _ = feb.mesh.Hex8Element(id=1, text=HEX8_ELEMENT_STRINGS[0])
    with pytest.raises(ValidationError):
        _ = feb.mesh.Hex8Element(id=1, text=TET4_ELEMENT_STRINGS[0])


def test_tri3_element_definition():
    _ = feb.mesh.Tri3Element(id=1, text=TRI3_ELEMENT_STRINGS[0])
    with pytest.raises(ValidationError):
        _ = feb.mesh.Tri3Element(id=1, text=HEX8_ELEMENT_STRINGS[0])


def test_quad4_element_definition():
    _ = feb.mesh.Quad4Element(id=1, text=QUAD4_ELEMENT_STRINGS[0])
    with pytest.raises(ValidationError):
        _ = feb.mesh.Quad4Element(id=1, text=HEX8_ELEMENT_STRINGS[0])


def test_translate_tet4_mesh(tet4_meshio: Mesh):
    mesh = feb.mesh.translate_meshio(tet4_meshio)
    assert mesh.nodes
    assert mesh.elements


def test_translate_tet10_mesh(tet10_meshio: Mesh):
    mesh = feb.mesh.translate_meshio(tet10_meshio)
    assert mesh.nodes
    assert mesh.elements


def test_translate_hex8_mesh(hex8_meshio: Mesh):
    mesh = feb.mesh.translate_meshio(hex8_meshio)
    assert mesh.nodes
    assert mesh.elements


def test_translate_hex20_mesh(hex20_meshio: Mesh):
    mesh = feb.mesh.translate_meshio(hex20_meshio)
    assert mesh.nodes
    assert mesh.elements


def test_translate_hex27_mesh(hex27_meshio: Mesh):
    mesh = feb.mesh.translate_meshio(hex27_meshio)
    assert mesh.nodes
    assert mesh.elements
