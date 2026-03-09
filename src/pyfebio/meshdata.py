from typing import Literal

from pydantic_xml import BaseXmlModel, attr, element

from ._types import (
    StringFloatVec3,
)


class NodeDataNode(BaseXmlModel, tag="node", validate_assignment=True):
    lid: int = attr(ge=1)
    text: float | StringFloatVec3


class NodeData(BaseXmlModel, validate_assignment=True):
    name: str = attr()
    node_set: str = attr()
    data_type: Literal["scalar", "vec3"] = attr()
    all_nodes: list[NodeDataNode] = element(default=[], tag="node")

    def add_node(self, new_node: NodeDataNode):
        self.all_nodes.append(new_node)


class ElementDataElement(BaseXmlModel, tag="elem", validate_assignment=True):
    lid: int = attr(ge=1)
    text: float | StringFloatVec3


class ElementData(BaseXmlModel, validate_assignment=True):
    name: str = attr()
    elem_set: str = attr()
    data_type: Literal["scalar", "vec3"] = attr()
    all_elements: list[ElementDataElement] = element(default=[], tag="elem")

    def add_element(self, new_element: ElementDataElement):
        self.all_elements.append(new_element)


class SurfaceData(BaseXmlModel, validate_assignment=True):
    pass


class MeshData(BaseXmlModel, validate_assignment=True):
    element_data: list[ElementData] = element(default=[], tag="ElementData")
    node_data: list[NodeData] = element(default=[], tag="NodeData")

    def add_element_data(self, new_element_data: ElementData):
        assert isinstance(new_element_data, ElementData), "new_element_data must be an ElementData"
        self.element_data.append(new_element_data)

    def add_node_data(self, new_node_data: NodeData):
        assert isinstance(new_node_data, NodeData), "new_node_data must be a NodeData"
        self.node_data.append(new_node_data)
