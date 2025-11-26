r"""
We reference:
    https://github.com/febiosoftware/FEBioStudio/blob/master/XPLTLib/xpltReader3.h
    commit: 7c7f171
as:
    xpltReader3.h:LINE_NUMBER
"""

import logging
from enum import Enum, auto
from typing import Literal

import numpy as np
from pydantic.dataclasses import dataclass

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

DI_NAME_SIZE = 64  # Size of name variables (bytes) from xpltReader3.h:209
MAX_DEPTH = 5

_DTYPES = {
    "float32": np.dtype(np.float32),
    "uint32": np.dtype(np.uint32),
    "int32": np.dtype(np.int32),
    "szname": np.dtype("S1"),
    "node": np.dtype([("id", np.int32), ("x", np.float32), ("y", np.float32), ("z", np.float32)]),
}

_DTYPES_SIZE = {
    "float32": 4,
    "uint32": 4,
    "int32": 4,
    "szname": 1,
    "node": 16,
}


def dtypes_to_little_endian(_DTYPES):
    """
    Uncommon these days, but if your XPLT file was created on a big-endian machine,
    this will do a byte swap to little-endian for all _DTYPES

    Note: szname being a byte string type will be unchanged
    """
    for key, value in _DTYPES.items():
        _DTYPES[key] = value.newbyteorder("<")


@dataclass
class Xtag:
    name: str
    leaf: bool = False
    singleton: bool = False
    format: Literal["float32", "uint32", "int32", "szname", "node"] = "int32"


FEBIO_TAG = int(0x00464542)

TAG_LUT = {
    # Root/
    # Root/Header
    int(0x01000000): Xtag(name="PLT_ROOT"),
    int(0x1010000): Xtag(name="PLT_HEADER"),
    int(0x01010001): Xtag(name="PLT_HDR_VERSION", leaf=True),
    int(0x01010004): Xtag(name="PLT_HDR_COMPRESSION", leaf=True),
    int(0x01010005): Xtag(name="PLT_HDR_AUTHOR", leaf=True),
    int(0x01010006): Xtag(name="PLT_HDR_SOFTWARE", leaf=True),
    int(0x01010007): Xtag(name="PLT_HDR_UNITS", leaf=True, format="szname"),
    # Root/Dictionary
    int(0x01020000): Xtag(name="PLT_DICTIONARY"),
    int(0x01020001): Xtag(name="PLT_DIC_ITEM"),
    int(0x01020002): Xtag(name="PLT_DIC_ITEM_TYPE", leaf=True, singleton=True),
    int(0x01020003): Xtag(name="PLT_DIC_ITEM_FMT", leaf=True, singleton=True),
    int(0x01020004): Xtag(name="PLT_DIC_ITEM_NAME", leaf=True, format="szname"),
    int(0x01020005): Xtag(name="PLT_DIC_ITEM_ARRAYSIZE", leaf=True),
    int(0x01020006): Xtag(name="PLT_DIC_ITEM_ARRAYNAME", leaf=True, format="szname"),
    int(0x01020007): Xtag(name="PLT_DIC_ITEM_UNITS", leaf=True, format="szname"),
    int(0x01021000): Xtag(name="PLT_DIC_GLOBAL"),
    int(0x01023000): Xtag(name="PLT_DIC_NODAL"),
    int(0x01024000): Xtag(name="PLT_DIC_DOMAIN"),
    int(0x01025000): Xtag(name="PLT_DIC_SURFACE"),
    int(0x01026000): Xtag(name="PLT_DIC_EDGE"),
    # Mesh/
    int(0x01040000): Xtag(name="PLT_MESH"),
    # Mesh/Nodes
    int(0x01041000): Xtag(name="PLT_NODE_SECTION"),
    int(0x01041100): Xtag(name="PLT_NODE_HEADER"),
    int(0x01041101): Xtag(name="PLT_NODE_SIZE", leaf=True),
    int(0x01041102): Xtag(name="PLT_NODE_DIM", leaf=True),
    int(0x01041103): Xtag(name="PLT_NODE_NAME", leaf=True, format="szname"),
    int(0x01041200): Xtag(name="PLT_NODE_COORDS", leaf=True, format="node"),
    # Mesh/Domains
    int(0x01042000): Xtag(name="PLT_DOMAIN_SECTION"),
    # Mesh/Domains/Domain
    int(0x01042100): Xtag(name="PLT_DOMAIN"),
    int(0x01042101): Xtag(name="PLT_DOMAIN_HDR"),
    int(0x01042102): Xtag(name="PLT_DOM_ELEM_TYPE", leaf=True),
    int(0x01042103): Xtag(name="PLT_DOM_PART_ID", leaf=True, singleton=True),
    int(0x01032104): Xtag(name="PLT_DOM_ELEMS", leaf=True),
    int(0x01032105): Xtag(name="PLT_DOM_NAME", leaf=True, format="szname"),
    int(0x01042200): Xtag(name="PLT_DOM_ELEM_LIST", leaf=False),
    int(0x01042201): Xtag(name="PLT_ELEMENT", leaf=True),
    # Mesh/Surfaces
    int(0x01043000): Xtag(name="PLT_SURFACE_SECTION"),
    # Mesh/Surfaces/Surface
    int(0x01043100): Xtag(name="PLT_SURFACE"),
    int(0x01043101): Xtag(name="PLT_SURFACE_HDR"),
    int(0x01043102): Xtag(name="PLT_SURFACE_ID", leaf=True, singleton=True),
    int(0x01043103): Xtag(name="PLT_SURFACE_FACES", leaf=True),
    int(0x01043104): Xtag(name="PLT_SURFACE_NAME", leaf=True, format="szname"),
    int(0x01043105): Xtag(name="PLT_SURFACE_MAX_FACET_NODES", leaf=True),
    int(0x01043200): Xtag(name="PLT_FACE_LIST"),
    int(0x01043201): Xtag(name="PLT_FACE", leaf=True),
    int(0x01044000): Xtag(name="PLT_NODESET_SECTION"),
    int(0x01044100): Xtag(name="PLT_NODESET"),
    int(0x01044101): Xtag(name="PLT_NODESET_HDR"),
    int(0x01044102): Xtag(name="PLT_NODESET_ID", leaf=True),
    int(0x01044103): Xtag(name="PLT_NODESET_NAME", leaf=True, format="szname"),
    int(0x01044104): Xtag(name="PLT_NODESET_SIZE", leaf=True),
    int(0x01044200): Xtag(name="PLT_NODESET_LIST", leaf=True),
    int(0x01045000): Xtag(name="PLT_PARTS_SECTION"),
    int(0x01045100): Xtag(name="PLT_PART"),
    int(0x01045101): Xtag(name="PLT_PART_ID", leaf=True),
    int(0x01045102): Xtag(name="PLT_PART_NAME", leaf=True, format="szname"),
    # Mesh/ElementSets
    # element set section was added in 4.1
    int(0x01046000): Xtag(name="PLT_ELEMENTSET_SECTION"),
    # Mesh/ElementSets/ElementSet
    int(0x01046100): Xtag(name="PLT_ELEMENTSET"),
    int(0x01046101): Xtag(name="PLT_ELEMENTSET_HDR"),
    int(0x01046102): Xtag(name="PLT_ELEMENTSET_ID", leaf=True),
    int(0x01046103): Xtag(name="PLT_ELEMENTSET_NAME", leaf=True, format="szname"),
    int(0x01046104): Xtag(name="PLT_ELEMENTSET_SIZE", leaf=True),
    int(0x01046200): Xtag(name="PLT_ELEMENTSET_LIST", leaf=True),
    # Mesh/FacetSets
    # facet set section was added in 4.1
    int(0x01047000): Xtag(name="PLT_FACETSET_SECTION"),
    # Mesh/FacetSets/FacetSet
    int(0x01047100): Xtag(name="PLT_FACETSET"),
    int(0x01047101): Xtag(name="PLT_FACETSET_HDR"),
    int(0x01047102): Xtag(name="PLT_FACETSET_ID", leaf=True),
    int(0x01047103): Xtag(name="PLT_FACETSET_NAME", leaf=True, format="szname"),
    int(0x01047104): Xtag(name="PLT_FACETSET_SIZE", leaf=True),
    int(0x01047105): Xtag(name="PLT_FACETSET_MAXNODES", leaf=True),
    int(0x01047200): Xtag(name="PLT_FACETSET_LIST", leaf=False),
    int(0x01047201): Xtag(name="PLT_FACET", leaf=True),
    # Mesh/Edges
    int(0x01048000): Xtag(name="PLT_EDGE_SECTION"),
    # Mesh/Edges/Edge
    int(0x01048100): Xtag(name="PLT_EDGE"),
    int(0x01048101): Xtag(name="PLT_EDGE_HDR"),
    int(0x01048102): Xtag(name="PLT_EDGE_ID", leaf=True),
    int(0x01048103): Xtag(name="PLT_EDGE_LINES", leaf=True),
    int(0x01048104): Xtag(name="PLT_EDGE_NAME", leaf=True, format="szname"),
    int(0x01048105): Xtag(name="PLT_EDGE_MAX_NODES", leaf=True),
    # Mesh/Edges/EdgeList
    int(0x01048200): Xtag(name="PLT_EDGE_LIST", leaf=True),
    # Mesh/Edges/EdgeList/Line
    int(0x01048201): Xtag(name="PLT_LINE", leaf=True),
    # Mesh/Objects
    int(0x01050000): Xtag(name="PLT_OBJECTS_SECTION"),
    # Mesh/Objects/Object
    int(0x01050001): Xtag(name="PLT_OBJECT_ID", leaf=True),
    int(0x01050002): Xtag(name="PLT_OBJECT_NAME", leaf=True, format="szname"),
    int(0x01050003): Xtag(name="PLT_OBJECT_TAG", leaf=True),
    int(0x01050004): Xtag(name="PLT_OBJECT_POS", leaf=True, format="float32"),
    int(0x01050005): Xtag(name="PLT_OBJECT_ROT", leaf=True, format="float32"),
    int(0x01050006): Xtag(name="PLT_OBJECT_DATA", leaf=True, format="float32"),
    # Mesh/Objects/Object/Point
    int(0x01051000): Xtag(name="PLT_POINT_OBJECT"),
    int(0x01051001): Xtag(name="PLT_POINT_COORD", leaf=True, format="float32"),
    # Mesh/Objects/Object/Line
    int(0x01052000): Xtag(name="PLT_LINE_OBJECT"),
    int(0x01052001): Xtag(name="PLT_LINE_COORDS", leaf=True, format="float32"),
    # State/
    int(0x02000000): Xtag(name="PLT_STATE"),
    # State/Header
    int(0x02010000): Xtag(name="PLT_STATE_HEADER"),
    int(0x02010001): Xtag(name="PLT_STATE_HDR_ID", leaf=True),
    int(0x02010002): Xtag(name="PLT_STATE_HDR_TIME", leaf=True, format="float32"),
    int(0x02010003): Xtag(name="PLT_STATE_STATUS", leaf=True),
    # State/Data
    int(0x02020000): Xtag(name="PLT_STATE_DATA"),
    int(0x02020001): Xtag(name="PLT_STATE_VARIABLE"),
    int(0x02020002): Xtag(name="PLT_STATE_VAR_ID", leaf=True, singleton=True),
    int(0x02020003): Xtag(name="PLT_STATE_VAR_DATA", leaf=True, format="float32"),
    int(0x02020100): Xtag(name="PLT_GLOBAL_DATA"),
    int(0x02020300): Xtag(name="PLT_NODE_DATA"),
    int(0x02020400): Xtag(name="PLT_ELEMENT_DATA"),
    int(0x02020500): Xtag(name="PLT_FACE_DATA"),
    int(0x02020600): Xtag(name="PLT_EDGE_DATA"),
    # State/MeshState
    int(0x02030000): Xtag(name="PLT_MESH_STATE"),
    # State/MeshState/ElementState
    int(0x02030001): Xtag(name="PLT_ELEMENT_STATE", leaf=True),
    # State/ObjectsState
    int(0x02040000): Xtag(name="PLT_OBJECTS_STATE"),
}


class VarType(Enum):
    """
    Var_Type from xpltReader3.h:179
    """

    FLOAT = auto()
    VEC3F = auto()
    MAT3FS = auto()
    MAT3FD = auto()
    TENS4FS = auto()
    MAT3F = auto()
    ARRAY = auto()
    ARRAY_VEC3F = auto()


class VarFormat(Enum):
    """
    Var_Fmt from xpltReader3.h:182
    """

    FMT_NODE = auto()
    FMT_ITEM = auto()
    FMT_MULT = auto()
    FMT_REGION = auto()


class ElemType(Enum):
    """
    Elem_Type from xpltReader3.h:185
    """

    PLT_ELEM_HEX8 = auto()
    PLT_ELEM_PENTA = auto()
    PLT_ELEM_TET4 = auto()
    PLT_ELEM_QUAD = auto()
    PLT_ELEM_TRI = auto()
    PLT_ELEM_TRUSS = auto()
    PLT_ELEM_HEX20 = auto()
    PLT_ELEM_TET10 = auto()
    PLT_ELEM_TET15 = auto()
    PLT_ELEM_HEX27 = auto()
    PLT_ELEM_TRI6 = auto()
    PLT_ELEM_QUAD8 = auto()
    PLT_ELEM_QUAD9 = auto()
    PLT_ELEM_PENTA15 = auto()
    PLT_ELEM_TET20 = auto()
    PLT_ELEM_TRI10 = auto()
    PLT_ELEM_PYRA5 = auto()
    PLT_ELEM_TET5 = auto()
    PLT_ELEM_PYRA13 = auto()
    PLT_ELEM_LINE3 = auto()  # new in 3.4


# @dataclass
# class DictItem:
#     ntype: np.uint32
#     nfmt: np.uint32
#     szname: str
#     szunit: str
#     index: np.uint32
#     array_size: np.uint32
#     array_names: list[str]


# @dataclass
# class Dictionary:
#     glb: list[DictItem]
#     mat: list[DictItem]
#     node: list[DictItem]
#     elem: list[DictItem]
#     face: list[DictItem]
#     edge: list[DictItem]


# @dataclass
# class Material:
#     nid: np.int32
#     szname: str


# @dataclass
# class Node:
#     id: np.int32
#     x: tuple[float, float, float]


# @dataclass
# class Elem:
#     eid: np.int32
#     index: np.int32
#     node: list[np.int32]


# @dataclass
# class Face:
#     nid: np.int32
#     nn: np.int32
#     node: list[np.int32]


# @dataclass
# class Line:
#     id: np.int32
#     nn: np.int32
#     node: list[np.int32]


# @dataclass
# class Domain:
#     etype: np.int32
#     mid: np.int32
#     ne: np.int32
#     nid: np.int32
#     szname: str
#     elist: list[np.int32]
#     elem: list[Elem]


# @dataclass
# class Surface:
#     sid: np.int32
#     nfaces: np.int32
#     max_nodes: np.int32
#     face: list[Face]
#     szname: str


# @dataclass
# class Edge:
#     eid: np.int32
#     nlines: np.int32
#     max_nodes: np.int32
#     line: list[Line]
#     szname: str


# @dataclass
# class NodeSet:
#     nid: np.int32
#     nn: np.int32
#     szname: str
#     node: list[np.int32]


# @dataclass
# class ElemSet:
#     nid: np.int32
#     ne: np.int32
#     szname: str
#     elem: list[np.int32]


# @dataclass
# class XMesh:
#     mat: list[Material]
#     node: list[Node]
#     dom: list[Domain]
#     surf: list[Surface]
#     edge: list[Edge]
#     node_set: list[NodeSet]
#     elem_set: list[ElemSet]
#     facet_set: list[Surface]


def check_file_is_febio(buffer):
    if not np.frombuffer(buffer, dtype=_DTYPES["int32"], count=1)[0] == int(FEBIO_TAG):
        dtypes_to_little_endian(_DTYPES)
        if np.frombuffer(buffer, dtype=_DTYPES["int32"], count=1)[0] == int(FEBIO_TAG):
            log.info("File is FEBio, but in Big Endian format -- will be byte-swapped to Little Endian")
        else:
            raise ValueError("Invalid FEBio file")
    else:
        log.info("File is FEBio, and in Little Endian format")


def parse_blocks(buffer, data_offset=0, max_depth=MAX_DEPTH):
    i = 0
    blocks = []
    while i < (len(buffer) - 8):
        tag = np.frombuffer(buffer, dtype=_DTYPES["int32"], count=1, offset=i)[0]
        count = np.frombuffer(buffer, dtype=_DTYPES["int32"], count=1, offset=i + 4)[0]
        child = buffer[i + 8 : i + 8 + count]
        block = {"tag": f"{tag:#010x}", "name": TAG_LUT[tag].name, "size": count}
        try:
            TAG_LUT[tag]
        except KeyError:
            log.warning(f"Unknown tag {tag:#08x}")
            block["data"] = child
            blocks.append(block)
            i += 8 + count
            continue
        if TAG_LUT[tag].leaf:
            max_depth = MAX_DEPTH
            if TAG_LUT[tag].name == "PLT_STATE_VAR_DATA":
                data = {}
                j = 0
                total_size = 0
                while j < len(child):
                    region_id = np.frombuffer(child[j : j + 4], count=1, dtype=_DTYPES["int32"])[0]
                    region_size = np.frombuffer(child[j + 4 : j + 8], count=1, dtype=_DTYPES["int32"])[0]
                    data[region_id] = np.frombuffer(
                        child[j + 8 : j + 8 + region_size],
                        dtype=_DTYPES[TAG_LUT[tag].format],
                    )
                    total_size += region_size
                    j += region_size + 8
                block["data"] = data
                block["size"] = total_size
            else:
                block["data"] = np.frombuffer(
                    child, dtype=_DTYPES[TAG_LUT[tag].format], offset=0, count=count // _DTYPES_SIZE[TAG_LUT[tag].format]
                )
            if TAG_LUT[tag].format == "szname":
                assert isinstance(block["data"], np.ndarray)
                if block["size"] == DI_NAME_SIZE:
                    block["data"] = block["data"].tobytes()
                    str_end = block["data"].find(b"\x00")
                    block["data"] = block["data"][0:str_end].decode("utf-8")
                elif block["size"] > 0:
                    block["data"] = block["data"].tobytes()
                    str_start = block["data"].rfind(b"\x00")
                    block["data"] = block["data"][str_start + 1 :].decode("utf-8")
                else:
                    block["data"] = ""
        else:
            if max_depth > 1:
                block["data"] = parse_blocks(child, data_offset=data_offset + i + 8, max_depth=max_depth - 1)
        blocks.append(block)
        i += 8 + count
    return blocks


def parse_xplt(filename: str):
    with open(filename, "rb") as fid:
        buffer = fid.read()
        check_file_is_febio(buffer)
        blocks = parse_blocks(buffer[4:])
        log.info(blocks)
