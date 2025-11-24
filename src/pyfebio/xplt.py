r"""
We reference:
    https://github.com/febiosoftware/FEBioStudio/blob/master/XPLTLib/xpltReader3.h
    commit: 7c7f171
as:
    xpltReader3.h:LINE_NUMBER
"""

from enum import Enum, auto

import numpy as np
from pydantic.dataclasses import dataclass

FEBIO_TAG = 0x00464542  # From xpltReader3.h:176
DI_NAME_SIZE = 64  # Size of name variables (bytes) from xpltReader3.h:209

_DTYPES = {"float32": np.dtype(np.float32), "uint32": np.dtype(np.uint32), "int32": np.dtype(np.int32), "szname": np.dtype("S64")}


def dtypes_to_little_endian(_DTYPES):
    """
    Uncommon these days, but if your XPLT file was created on a big-endian machine,
    this will do a byte swap to little-endian for all _DTYPES

    Note: szname being a byte string type will be unchanged
    """
    for key, value in _DTYPES.items():
        _DTYPES[key] = value.newbyteorder("<")


TAG_LUT = {
    int(0x01000000): "PLT_ROOT",
    int(0x1010000): "PLT_HEADER ",
    int(0x01010001): "PLT_HDR_VERSION",
    int(0x01010004): "PLT_HDR_COMPRESSION",
    int(0x01010005): "PLT_HDR_AUTHOR",
    int(0x01010006): "PLT_HDR_SOFTWARE",
    int(0x01010007): "PLT_HDR_UNITS",
    int(0x01020000): "PLT_DICTIONARY",
    int(0x01020001): "PLT_DIC_ITEM",
    int(0x01020002): "PLT_DIC_ITEM_TYPE",
    int(0x01020003): "PLT_DIC_ITEM_FMT",
    int(0x01020004): "PLT_DIC_ITEM_NAME",
    int(0x01020005): "PLT_DIC_ITEM_ARRAYSIZE",
    int(0x01020006): "PLT_DIC_ITEM_ARRAYNAME",
    int(0x01020007): "PLT_DIC_ITEM_UNITS",
    int(0x01021000): "PLT_DIC_GLOBAL",
    int(0x01023000): "PLT_DIC_NODAL",
    int(0x01024000): "PLT_DIC_DOMAIN",
    int(0x01025000): "PLT_DIC_SURFACE",
    int(0x01026000): "PLT_DIC_EDGE",
    int(0x01040000): "PLT_MESH",
    int(0x01041000): "PLT_NODE_SECTION",
    int(0x01041100): "PLT_NODE_HEADER",
    int(0x01041101): "PLT_NODE_SIZE",
    int(0x01041102): "PLT_NODE_DIM",
    int(0x01041103): "PLT_NODE_NAME",
    int(0x01041200): "PLT_NODE_COORDS",
    int(0x01042000): "PLT_DOMAIN_SECTION",
    int(0x01042100): "PLT_DOMAIN",
    int(0x01042101): "PLT_DOMAIN_HDR",
    int(0x01042102): "PLT_DOM_ELEM_TYPE",
    int(0x01042103): "PLT_DOM_PART_ID",
    int(0x01032104): "PLT_DOM_ELEMS",
    int(0x01032105): "PLT_DOM_NAME",
    int(0x01042200): "PLT_DOM_ELEM_LIST",
    int(0x01042201): "PLT_ELEMENT",
    int(0x01043000): "PLT_SURFACE_SECTION",
    int(0x01043100): "PLT_SURFACE",
    int(0x01043101): "PLT_SURFACE_HDR",
    int(0x01043102): "PLT_SURFACE_ID",
    int(0x01043103): "PLT_SURFACE_FACES",
    int(0x01043104): "PLT_SURFACE_NAME",
    int(0x01043105): "PLT_SURFACE_MAX_FACET_NODES",
    int(0x01043200): "PLT_FACE_LIST",
    int(0x01043201): "PLT_FACE",
    int(0x01044000): "PLT_NODESET_SECTION",
    int(0x01044100): "PLT_NODESET",
    int(0x01044101): "PLT_NODESET_HDR",
    int(0x01044102): "PLT_NODESET_ID",
    int(0x01044103): "PLT_NODESET_NAME",
    int(0x01044104): "PLT_NODESET_SIZE",
    int(0x01044200): "PLT_NODESET_LIST",
    int(0x01045000): "PLT_PARTS_SECTION",
    int(0x01045100): "PLT_PART",
    int(0x01045101): "PLT_PART_ID",
    int(0x01045102): "PLT_PART_NAME",
    # element set section was added in 4.1
    int(0x01046000): "PLT_ELEMENTSET_SECTION",
    int(0x01046100): "PLT_ELEMENTSET",
    int(0x01046101): "PLT_ELEMENTSET_HDR",
    int(0x01046102): "PLT_ELEMENTSET_ID",
    int(0x01046103): "PLT_ELEMENTSET_NAME",
    int(0x01046104): "PLT_ELEMENTSET_SIZE",
    int(0x01046200): "PLT_ELEMENTSET_LIST",
    # facet set section was added in 4.1
    int(0x01047000): "PLT_FACETSET_SECTION",
    int(0x01047100): "PLT_FACETSET",
    int(0x01047101): "PLT_FACETSET_HDR",
    int(0x01047102): "PLT_FACETSET_ID",
    int(0x01047103): "PLT_FACETSET_NAME",
    int(0x01047104): "PLT_FACETSET_SIZE",
    int(0x01047105): "PLT_FACETSET_MAXNODES",
    int(0x01047200): "PLT_FACETSET_LIST",
    int(0x01047201): "PLT_FACET",
    int(0x01048000): "PLT_EDGE_SECTION",
    int(0x01048100): "PLT_EDGE",
    int(0x01048101): "PLT_EDGE_HDR",
    int(0x01048102): "PLT_EDGE_ID",
    int(0x01048103): "PLT_EDGE_LINES",
    int(0x01048104): "PLT_EDGE_NAME",
    int(0x01048105): "PLT_EDGE_MAX_NODES",
    int(0x01048200): "PLT_EDGE_LIST",
    int(0x01048201): "PLT_LINE",
    int(0x01050000): "PLT_OBJECTS_SECTION",
    int(0x01050001): "PLT_OBJECT_ID",
    int(0x01050002): "PLT_OBJECT_NAME",
    int(0x01050003): "PLT_OBJECT_TAG",
    int(0x01050004): "PLT_OBJECT_POS",
    int(0x01050005): "PLT_OBJECT_ROT",
    int(0x01050006): "PLT_OBJECT_DATA",
    int(0x01051000): "PLT_POINT_OBJECT",
    int(0x01051001): "PLT_POINT_COORD",
    int(0x01052000): "PLT_LINE_OBJECT",
    int(0x01052001): "PLT_LINE_COORDS",
    int(0x02000000): "PLT_STATE",
    int(0x02010000): "PLT_STATE_HEADER",
    int(0x02010001): "PLT_STATE_HDR_ID",
    int(0x02010002): "PLT_STATE_HDR_TIME",
    int(0x02010003): "PLT_STATE_STATUS",
    int(0x02020000): "PLT_STATE_DATA",
    int(0x02020001): "PLT_STATE_VARIABLE",
    int(0x02020002): "PLT_STATE_VAR_ID",
    int(0x02020003): "PLT_STATE_VAR_DATA",
    int(0x02020100): "PLT_GLOBAL_DATA",
    int(0x02020300): "PLT_NODE_DATA",
    int(0x02020400): "PLT_ELEMENT_DATA",
    int(0x02020500): "PLT_FACE_DATA",
    int(0x02020600): "PLT_EDGE_DATA",
    int(0x02030000): "PLT_MESH_STATE",
    int(0x02030001): "PLT_ELEMENT_STATE",
    int(0x02040000): "PLT_OBJECTS_STATE",
}


@dataclass
class BranchBlock:
    btype: str
    count: int
    size: int


class FileTags(Enum):
    """
    File section tags xpltReader3.h:46
    """

    PLT_ROOT = 0x01000000
    PLT_HEADER = 0x1010000
    PLT_HDR_VERSION = 0x01010001
    PLT_HDR_COMPRESSION = 0x01010004
    PLT_HDR_AUTHOR = 0x01010005  # new in 2.0
    PLT_HDR_SOFTWARE = 0x01010006  # new in 2.0
    PLT_HDR_UNITS = 0x01010007  # new in 4.0
    PLT_DICTIONARY = 0x01020000
    PLT_DIC_ITEM = 0x01020001
    PLT_DIC_ITEM_TYPE = 0x01020002
    PLT_DIC_ITEM_FMT = 0x01020003
    PLT_DIC_ITEM_NAME = 0x01020004
    PLT_DIC_ITEM_ARRAYSIZE = 0x01020005  # added in version 0x05
    PLT_DIC_ITEM_ARRAYNAME = 0x01020006  # added in version 0x05
    PLT_DIC_ITEM_UNITS = 0x01020007  # added in version 4.0
    PLT_DIC_GLOBAL = 0x01021000
    PLT_DIC_NODAL = 0x01023000
    PLT_DIC_DOMAIN = 0x01024000
    PLT_DIC_SURFACE = 0x01025000
    PLT_DIC_EDGE = 0x01026000
    PLT_MESH = 0x01040000  # this was PLT_GEOMETRY
    PLT_NODE_SECTION = 0x01041000
    PLT_NODE_HEADER = 0x01041100  # new in 2.0
    PLT_NODE_SIZE = 0x01041101  # new in 2.0
    PLT_NODE_DIM = 0x01041102  # new in 2.0
    PLT_NODE_NAME = 0x01041103  # new in 2.0
    PLT_NODE_COORDS = 0x01041200  # new in 2.0
    PLT_DOMAIN_SECTION = 0x01042000
    PLT_DOMAIN = 0x01042100
    PLT_DOMAIN_HDR = 0x01042101
    PLT_DOM_ELEM_TYPE = 0x01042102
    PLT_DOM_PART_ID = 0x01042103  # this was PLT_DOM_MAT_ID
    PLT_DOM_ELEMS = 0x01032104
    PLT_DOM_NAME = 0x01032105
    PLT_DOM_ELEM_LIST = 0x01042200
    PLT_ELEMENT = 0x01042201
    PLT_SURFACE_SECTION = 0x01043000
    PLT_SURFACE = 0x01043100
    PLT_SURFACE_HDR = 0x01043101
    PLT_SURFACE_ID = 0x01043102
    PLT_SURFACE_FACES = 0x01043103
    PLT_SURFACE_NAME = 0x01043104
    PLT_SURFACE_MAX_FACET_NODES = 0x01043105  # new in 2.0 (max number of nodes per facet)
    PLT_FACE_LIST = 0x01043200
    PLT_FACE = 0x01043201
    PLT_NODESET_SECTION = 0x01044000
    PLT_NODESET = 0x01044100
    PLT_NODESET_HDR = 0x01044101
    PLT_NODESET_ID = 0x01044102
    PLT_NODESET_NAME = 0x01044103
    PLT_NODESET_SIZE = 0x01044104
    PLT_NODESET_LIST = 0x01044200
    PLT_PARTS_SECTION = 0x01045000  # new in 2.0
    PLT_PART = 0x01045100
    PLT_PART_ID = 0x01045101
    PLT_PART_NAME = 0x01045102

    # element set section was added in 4.1
    PLT_ELEMENTSET_SECTION = 0x01046000
    PLT_ELEMENTSET = 0x01046100
    PLT_ELEMENTSET_HDR = 0x01046101
    PLT_ELEMENTSET_ID = 0x01046102
    PLT_ELEMENTSET_NAME = 0x01046103
    PLT_ELEMENTSET_SIZE = 0x01046104
    PLT_ELEMENTSET_LIST = 0x01046200

    # facet set section was added in 4.1
    PLT_FACETSET_SECTION = 0x01047000
    PLT_FACETSET = 0x01047100
    PLT_FACETSET_HDR = 0x01047101
    PLT_FACETSET_ID = 0x01047102
    PLT_FACETSET_NAME = 0x01047103
    PLT_FACETSET_SIZE = 0x01047104
    PLT_FACETSET_MAXNODES = 0x01047105
    PLT_FACETSET_LIST = 0x01047200
    PLT_FACET = 0x01047201

    PLT_EDGE_SECTION = 0x01048000  # new in 3.5
    PLT_EDGE = 0x01048100
    PLT_EDGE_HDR = 0x01048101
    PLT_EDGE_ID = 0x01048102
    PLT_EDGE_LINES = 0x01048103
    PLT_EDGE_NAME = 0x01048104
    PLT_EDGE_MAX_NODES = 0x01048105
    PLT_EDGE_LIST = 0x01048200
    PLT_LINE = 0x01048201

    PLT_OBJECTS_SECTION = 0x01050000
    PLT_OBJECT_ID = 0x01050001
    PLT_OBJECT_NAME = 0x01050002
    PLT_OBJECT_TAG = 0x01050003
    PLT_OBJECT_POS = 0x01050004
    PLT_OBJECT_ROT = 0x01050005
    PLT_OBJECT_DATA = 0x01050006
    PLT_POINT_OBJECT = 0x01051000
    PLT_POINT_COORD = 0x01051001
    PLT_LINE_OBJECT = 0x01052000
    PLT_LINE_COORDS = 0x01052001

    PLT_STATE = 0x02000000
    PLT_STATE_HEADER = 0x02010000
    PLT_STATE_HDR_ID = 0x02010001
    PLT_STATE_HDR_TIME = 0x02010002
    PLT_STATE_STATUS = 0x02010003  # new in 3.1
    PLT_STATE_DATA = 0x02020000
    PLT_STATE_VARIABLE = 0x02020001
    PLT_STATE_VAR_ID = 0x02020002
    PLT_STATE_VAR_DATA = 0x02020003
    PLT_GLOBAL_DATA = 0x02020100
    PLT_NODE_DATA = 0x02020300
    PLT_ELEMENT_DATA = 0x02020400
    PLT_FACE_DATA = 0x02020500
    PLT_EDGE_DATA = 0x02020600  # new in 3.5
    PLT_MESH_STATE = 0x02030000
    PLT_ELEMENT_STATE = 0x02030001
    PLT_OBJECTS_STATE = 0x02040000


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


def _read_root_section(buffer):
    if not np.frombuffer(buffer, dtype=_DTYPES["int32"], count=1)[0] == int(FEBIO_TAG):
        dtypes_to_little_endian(_DTYPES)
        if np.frombuffer(buffer, dtype=_DTYPES["int32"], count=1)[0] == int(FEBIO_TAG):
            pass
        else:
            raise ValueError("Invalid FEBio file")
    data_offset = 4
    while data_offset < len(buffer) - 4:
        tag = np.frombuffer(buffer, dtype=_DTYPES["int32"], count=1, offset=data_offset)[0]
        data_offset += 4
        # count = int(np.frombuffer(buffer, dtype=_DTYPES["int32"], count=1, offset=data_offset))
        # data_offset += 4
        try:
            print(TAG_LUT[tag], hex(tag), tag, data_offset)
        except KeyError:
            continue

        # match tag:
        #     case int(FileTags.PLT_DICTIONARY.value):
        #         print("found")
        #         print(hex(tag), data_offset)
        #         break
        #     case _:
        #         print(hex(tag), data_offset)


def _read_state_section():
    pass


def _read_dictionary():
    pass


def _read_mesh():
    pass


def _read_dict_item():
    pass


def _create_materials():
    pass


def _build_mesh():
    pass


def _read_global_dict_items():
    pass


def _read_material_dict_items():
    pass


def _read_node_dict_items():
    pass


def _read_elem_dict_items():
    pass


def _read_face_dict_items():
    pass


def _read_edge_dict_items():
    pass


def parse_xplt(filename: str):
    with open(filename, "rb") as fid:
        buffer = fid.read()
        _read_root_section(buffer)
        _read_state_section()
        _read_dictionary()
        _read_mesh()
        _read_dict_item()
        _create_materials()
        _build_mesh()
        _read_global_dict_items()
        _read_material_dict_items()
        _read_node_dict_items()
        _read_elem_dict_items()
        _read_face_dict_items()
        _read_edge_dict_items()
