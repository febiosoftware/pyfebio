import itertools
from io import StringIO
from typing import Literal

import meshio
import numpy as np
from pydantic import Field, model_validator
from pydantic_xml import BaseXmlModel, attr, element

from ._types import (
    StringFloatVec3,
    StringUIntVec,
    StringUIntVec2,
    StringUIntVec3,
    StringUIntVec4,
    StringUIntVec5,
    StringUIntVec6,
    StringUIntVec8,
    StringUIntVec9,
    StringUIntVec10,
    StringUIntVec15,
    StringUIntVec20,
    StringUIntVec27,
)

SolidFEBioElementType = Literal["tet4", "tet10", "tet15", "hex8", "hex20", "hex27", "penta6", "penta15", "pyra5"]
ShellFEBioElementType = Literal["tri3", "tri6", "quad4", "quad8", "quad9", "q4ans", "q4eas"]
BeamFEBioElementType = Literal["line2", "line3"]


class Node(BaseXmlModel, tag="node", validate_assignment=True):
    text: StringFloatVec3 = Field(default="0.0,0.0,0.0")
    id: int = attr()


class Nodes(BaseXmlModel, validate_assignment=True):
    name: str = attr(default="")
    all_nodes: list[Node] = element(tag="node", default=[])

    def add_node(self, new_node: Node):
        assert isinstance(new_node, Node), "new_node must be an instance of Node"
        self.all_nodes.append(new_node)


class Tet4Element(BaseXmlModel, tag="elem", validate_assignment=True):
    text: StringUIntVec4 = Field(default="1,2,3,4")
    id: int = attr()


class Tet10Element(BaseXmlModel, tag="elem", validate_assignment=True):
    text: StringUIntVec10 = Field(default="1,2,3,4,5,6,7,8,9,10")
    id: int = attr()


class Tet15Element(BaseXmlModel, tag="elem", validate_assignment=True):
    text: StringUIntVec15 = Field(default="1,2,3,4,5,6,7,8,9,10,11,12,13,14,15")
    id: int = attr()


class Hex8Element(BaseXmlModel, tag="elem", validate_assignment=True):
    text: StringUIntVec8 = Field(default="1,2,3,4,5,6,7,8")
    id: int = attr()


class Hex20Element(BaseXmlModel, tag="elem", validate_assignment=True):
    text: StringUIntVec20 = Field(default="1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20")
    id: int = attr()


class Hex27Element(BaseXmlModel, tag="elem", validate_assignment=True):
    text: StringUIntVec27 = Field(default="1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27")
    id: int = attr()


class Penta6Element(BaseXmlModel, tag="elem", validate_assignment=True):
    text: StringUIntVec6 = Field(default="1,2,3,4,5,6")
    id: int = attr()


class Penta15Element(BaseXmlModel, tag="elem", validate_assignment=True):
    text: StringUIntVec15 = Field(default="1,2,3,4,5,6,7,8,9,10,11,12,13,14,15")
    id: int = attr()


class Pyra5Element(BaseXmlModel, tag="elem", validate_assignment=True):
    text: StringUIntVec5 = Field(default="1,2,3,4,5")
    id: int = attr()


class Tri3Element(BaseXmlModel, tag="elem", validate_assignment=True):
    text: StringUIntVec3 = Field(default="1,2,3")
    id: int = attr()


class Tri6Element(BaseXmlModel, tag="elem", validate_assignment=True):
    text: StringUIntVec6 = Field(default="1,2,3,4,5,6")
    id: int = attr()


class Quad4Element(BaseXmlModel, tag="elem", validate_assignment=True):
    text: StringUIntVec4 = Field(default="1,2,3,4")
    id: int = attr()


class Quad8Element(BaseXmlModel, tag="elem", validate_assignment=True):
    text: StringUIntVec8 = Field(default="1,2,3,4,5,6,7,8")
    id: int = attr()


class Quad9Element(BaseXmlModel, tag="elem", validate_assignment=True):
    text: StringUIntVec9 = Field(default="1,2,3,4,5,6,7,8,9")
    id: int = attr()


class Line2Element(BaseXmlModel, tag="elem", validate_assignment=True):
    text: StringUIntVec2 = Field(default="1,2")
    id: int = attr()


class Line3Element(BaseXmlModel, tag="elem", validate_assignment=True):
    text: StringUIntVec3 = Field(default="1,2,3")
    id: int = attr()


ElementType = (
    Tet4Element
    | Tet10Element
    | Tet15Element
    | Hex8Element
    | Hex20Element
    | Hex27Element
    | Penta6Element
    | Penta15Element
    | Pyra5Element
    | Tri3Element
    | Tri6Element
    | Quad4Element
    | Quad8Element
    | Quad9Element
    | Line2Element
    | Line3Element
)

ELEMENT_CLASS_MAP: dict[str, type[ElementType]] = {
    "tet4": Tet4Element,
    "tet10": Tet10Element,
    "tet15": Tet15Element,
    "hex8": Hex8Element,
    "hex20": Hex20Element,
    "hex27": Hex27Element,
    "tri3": Tri3Element,
    "tri6": Tri6Element,
    "penta6": Penta6Element,
    "penta15": Penta15Element,
    "pyra5": Pyra5Element,
    "quad4": Quad4Element,
    "q4ans": Quad4Element,
    "q4eas": Quad4Element,
    "quad8": Quad8Element,
    "quad9": Quad9Element,
    "line2": Line2Element,
    "line3": Line3Element,
}


class Elements(BaseXmlModel, tag="elements", validate_assignment=True):
    name: str = attr(default="Part")
    type: SolidFEBioElementType | ShellFEBioElementType | BeamFEBioElementType = attr(default="hex8")
    all_elements: list[ElementType] = element(default=[], tag="elem")

    def add_element(self, new_element: ElementType):
        self.all_elements.append(new_element)

    @model_validator(mode="after")
    def validate_elements(self):
        if not all(isinstance(elm, ELEMENT_CLASS_MAP[self.type]) for elm in self.all_elements):
            raise ValueError(f"All elements must be of type: {self.type}")
        return self


class ElementSet(BaseXmlModel, tag="ElementSet", validate_assignment=True):
    name: str = attr(default="")
    text: StringUIntVec

    def add_element(self, new_element_id: int):
        ",".join([self.text, str(new_element_id)])


class NodeSet(BaseXmlModel, tag="NodeSet", validate_assignment=True):
    name: str = attr(default="")
    text: StringUIntVec

    def add_node(self, new_node_id: int):
        ",".join([self.text, str(new_node_id)])


class Surface(BaseXmlModel, tag="Surface", validate_assignment=True):
    name: str = attr(default="")
    all_tri3: list[Tri3Element] = element(default=[], tag="tri3")
    all_tri6: list[Tri6Element] = element(default=[], tag="tri6")
    all_quad4: list[Quad4Element] = element(default=[], tag="quad4")
    all_quad8: list[Quad8Element] = element(default=[], tag="quad8")
    all_quad9: list[Quad9Element] = element(default=[], tag="quad9")

    def add_tri3(self, new_tri: Tri3Element):
        self.all_tri3.append(new_tri)

    def add_tri6(self, new_tri: Tri6Element):
        self.all_tri6.append(new_tri)

    def add_quad4(self, new_quad: Quad4Element):
        self.all_quad4.append(new_quad)

    def add_quad8(self, new_quad: Quad8Element):
        self.all_quad8.append(new_quad)

    def add_quad9(self, new_quad: Quad9Element):
        self.all_quad9.append(new_quad)


class Edge(BaseXmlModel, tag="Edge", validate_assignment=True):
    name: str = attr(default="")
    all_line2: list[Line2Element] = element(default=[], tag="line2")
    all_line3: list[Line3Element] = element(default=[], tag="line3")

    def add_line2(self, new_line2: Line2Element):
        self.all_line2.append(new_line2)

    def add_line3(self, new_line3: Line3Element):
        self.all_line3.append(new_line3)


class SurfacePair(BaseXmlModel, tag="SurfacePair", validate_assignment=True):
    name: str = attr(default="")
    primary: str = element()
    secondary: str = element()


class DiscreteElement(BaseXmlModel, tag="delem", validate_assignment=True):
    text: StringUIntVec2


class DiscreteSet(BaseXmlModel, tag="DiscreteSet", validate_assignment=True):
    name: str = attr(default="")
    elements: list[DiscreteElement] = element(default=[])

    def add_element(self, new_element: DiscreteElement):
        self.elements.append(new_element)


class Mesh(BaseXmlModel, validate_assignment=True):
    nodes: list[Nodes] = element(default=[], tag="Nodes")
    elements: list[Elements] = element(default=[], tag="Elements")
    surfaces: list[Surface] = element(default=[], tag="Surface")
    edges: list[Edge] = element(default=[], tag="Edge")
    element_sets: list[ElementSet] = element(default=[], tag="ElementSet")
    node_sets: list[NodeSet] = element(default=[], tag="NodeSet")
    discrete_sets: list[DiscreteSet] = element(default=[], tag="DiscreteSet")
    surface_pairs: list[SurfacePair] = element(default=[], tag="SurfacePair")

    def add_node_domain(self, new_node_domain: Nodes):
        if not new_node_domain.name:
            new_node_domain.name = f"Part{len(self.nodes) + 1}"
        assert isinstance(new_node_domain, Nodes), "new_node_domain must be an instance of Nodes"
        self.nodes.append(new_node_domain)

    def add_element_domain(self, new_element_domain: Elements):
        if new_element_domain.name == "Part":
            new_element_domain.name = f"Part{len(self.elements) + 1}"
        assert isinstance(new_element_domain, Elements), "new_element_domain must be an instance of Elements"
        self.elements.append(new_element_domain)

    def add_surface(self, new_surface: Surface):
        if not new_surface.name:
            new_surface.name = f"Surface{len(self.surfaces) + 1}"
        assert isinstance(new_surface, Surface), "new_surface must be an instance of Surface"
        self.surfaces.append(new_surface)

    def add_edge(self, new_edge: Edge):
        if not new_edge.name:
            new_edge.name = f"Edge{len(self.edges) + 1}"
        assert isinstance(new_edge, Edge), "new_edge must be an instance of Edge"
        self.edges.append(new_edge)

    def add_element_set(self, new_element_set: ElementSet):
        if not new_element_set.name:
            new_element_set.name = f"ElementSet{len(self.element_sets) + 1}"
        assert isinstance(new_element_set, ElementSet), "new_element_set must be an instance of ElementSet"
        self.element_sets.append(new_element_set)

    def add_node_set(self, new_node_set: NodeSet):
        if not new_node_set.name:
            new_node_set.name = f"NodeSet{len(self.node_sets) + 1}"
        assert isinstance(new_node_set, NodeSet), "new_node_set must be an instance of NodeSet"
        self.node_sets.append(new_node_set)

    def add_discrete_set(self, new_discrete_set: DiscreteSet):
        if not new_discrete_set.name:
            new_discrete_set.name = f"DiscreteSet{len(self.discrete_sets) + 1}"
        assert isinstance(new_discrete_set, DiscreteSet), "new_discrete_set must be an instance of DiscreteSet"
        self.discrete_sets.append(new_discrete_set)

    def add_surface_pair(self, new_surface_pair: SurfacePair):
        if not new_surface_pair.name:
            new_surface_pair.name = f"SurfacePair{len(self.surface_pairs) + 1}"
        assert isinstance(new_surface_pair, SurfacePair), "new_surface_pair must be an instance of SurfacePair"
        self.surface_pairs.append(new_surface_pair)


ELEMENT_MAP: dict[str, SolidFEBioElementType | ShellFEBioElementType | BeamFEBioElementType] = {
    "tetra": "tet4",
    "tetra10": "tet10",
    "hexahedron": "hex8",
    "hexahedron20": "hex20",
    "hexahedron27": "hex27",
    "triangle": "tri3",
    "triangle6": "tri6",
    "quad": "quad4",
    "quad8": "quad8",
    "quad9": "quad9",
    "line": "line2",
    "line3": "line3",
}


def _numpy_to_string_array(arr: np.ndarray, fmt: str) -> list[str]:
    """
    Using np.savetxt with a StringIO buffer is ~4X faster than using [",".join(map(str, row)) for row in arr]
    """

    buffer = StringIO()
    np.savetxt(buffer, arr, delimiter=",", fmt=fmt)
    buffer.seek(0)
    return buffer.read().splitlines()


def numpy_to_nodes(nodes: np.ndarray, name: str = "Part", offset: int = 0) -> Nodes:
    if nodes.ndim == 1:
        nodes = nodes.reshape(1, 3)
    str_array = _numpy_to_string_array(nodes, fmt="%e")
    return Nodes(name=name, all_nodes=[Node(id=i + offset + 1, text=line) for i, line in enumerate(str_array)])


def numpy_to_elements(
    elements: np.ndarray,
    element_type: SolidFEBioElementType | ShellFEBioElementType | BeamFEBioElementType,
    name: str = "Part",
    offset: int = 0,
) -> Elements:
    if elements.ndim == 1:
        elements = elements.reshape(1, elements.size)
    str_array = _numpy_to_string_array(elements, fmt="%d")
    elem_class = ELEMENT_CLASS_MAP[element_type]
    return Elements(
        name=name, type=element_type, all_elements=[elem_class(id=i + offset + 1, text=line) for i, line in enumerate(str_array)]
    )


def numpy_to_surface_list(
    facets: np.ndarray,
    element_type: ShellFEBioElementType,
    offset: int = 0,
) -> list[ShellFEBioElementType]:
    str_array = _numpy_to_string_array(facets, fmt="%d")
    elem_class = ELEMENT_CLASS_MAP[element_type]
    return [elem_class(id=i + offset + 1, text=line) for i, line in enumerate(str_array)]  # type:ignore


EXCLUDE_SET_STR = ("gmsh:bounding_entities",)


def translate_meshio(
    meshobj: meshio.Mesh,
    nodeoffset: int = 0,
    elementoffset: int = 0,
    surfaceoffset: int = 0,
    shell_sets: list[str] | None = None,
    elements_name: str | None = None,
    nodes_name: str | None = None,
    node_sets_from_surfaces: bool = False,
) -> Mesh:
    if shell_sets is None:
        shell_sets = []
    solid_nodes = []
    for key, value in meshobj.cells_dict.items():
        if meshio._mesh.topological_dimension[key] == 3:
            solid_nodes.extend(np.unique(value.ravel()).tolist())
    solid_nodes = set(solid_nodes)

    make_element = {}
    for key, values in meshobj.cells_dict.items():
        make_element[key] = []
        if meshio._mesh.topological_dimension[key] == 2:
            if not solid_nodes:
                make_element[key].extend([False] * len(values))
            else:
                for element in values:
                    make_element[key].append(bool(set(element.ravel()).difference(solid_nodes)))
        else:
            make_element[key].extend([True] * len(values))

    febio_mesh = Mesh()
    if nodes_name is None:
        nodes_name = "Part"
    nodes_object = numpy_to_nodes(nodes=meshobj.points, name=nodes_name, offset=nodeoffset)
    febio_mesh.add_node_domain(nodes_object)
    num_elements = 0
    if not meshobj.cell_sets_dict:
        cell_sets = set(itertools.chain(*meshobj.cell_tags.values()))  # type:ignore
        cell_sets = {set_name: [] for set_name in cell_sets}
        for cell_tags in meshobj.cell_data["cell_tags"]:
            unique_tags = np.unique(cell_tags)
            tmp_cell_sets = {set_name: [] for set_name in cell_sets}
            for tag, set_names in meshobj.cell_tags.items():  # type: ignore
                if tag in unique_tags:
                    for set_name in set_names:
                        tmp_cell_sets[set_name].append(np.argwhere(cell_tags == tag).ravel())
                else:
                    for set_name in set_names:
                        tmp_cell_sets[set_name].append(np.array([]))
            for key, value in cell_sets.items():
                cell_sets[key].append(np.concatenate(tmp_cell_sets[key]))

        meshobj.cell_sets = cell_sets

    # hex27 are ordered incorrectly
    hex27_reorder = [2, 6, 7, 3, 1, 5, 4, 0, 18, 14, 19, 10, 17, 12, 16, 8, 9, 13, 15, 11]
    hex27_reorder.extend([21, 25, 20, 24, 23, 22, 26])
    if not solid_nodes:
        for cell_block in meshobj.cells:
            if elements_name is None:
                part_name = cell_block.type
            else:
                part_name = elements_name
            etype = ELEMENT_MAP[cell_block.type]
            elements_object = numpy_to_elements(
                elements=cell_block.data + 1 + nodeoffset, element_type=etype, name=part_name, offset=num_elements + elementoffset
            )
            num_elements += cell_block.data.shape[0]
            febio_mesh.add_element_domain(elements_object)
    for name, members in meshobj.cell_sets_dict.items():
        if any([exclude in name.lower() for exclude in EXCLUDE_SET_STR]):
            continue
        shell_set = name in shell_sets
        for member, offsets in members.items():
            if len(members.keys()) > 1:
                set_name = f"{name}_{ELEMENT_MAP[member]}"
            else:
                set_name = name
            etype = ELEMENT_MAP[member]
            if shell_set or np.array(make_element[member])[offsets].all():
                if etype == "hex27":
                    elements = meshobj.cells_dict[member][offsets] + 1 + nodeoffset
                    elements = elements[:, hex27_reorder]
                else:
                    elements = meshobj.cells_dict[member][offsets] + 1 + nodeoffset
                elements_object = numpy_to_elements(
                    elements=elements,
                    element_type=etype,
                    name=set_name,
                    offset=num_elements + elementoffset,
                )
                num_elements += meshobj.cells_dict[member][offsets].shape[0]
                febio_mesh.add_element_domain(elements_object)
            else:
                surface_object = Surface(name=set_name)
                fn_map = {
                    "tri3": surface_object.all_tri3,
                    "tri6": surface_object.all_tri6,
                    "quad4": surface_object.all_quad4,
                    "quad8": surface_object.all_quad8,
                    "quad9": surface_object.all_quad9,
                }
                etype = ELEMENT_MAP[member]
                facets = meshobj.cells_dict[member][offsets] + 1 + nodeoffset
                surface_list = numpy_to_surface_list(facets=facets, element_type=etype, offset=surfaceoffset)  # type:ignore
                fn_map[etype].extend(surface_list)
                if node_sets_from_surfaces:
                    node_set = ",".join(map(str, sorted(np.unique(facets.ravel()))))
                    febio_mesh.add_node_set(NodeSet(name=set_name, text=node_set))
                febio_mesh.add_surface(surface_object)
    return febio_mesh
