r"""
We reference:
    https://github.com/febiosoftware/FEBioStudio/blob/master/XPLTLib/xpltReader3.h
    commit: 7c7f171
as:
    xpltReader3.h:LINE_NUMBER
"""

import logging
from enum import Enum, auto
from typing import Any, Callable, Literal

import h5py
import numpy as np
import pyarrow as pa
from pydantic import Field
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

ENDIAN: Literal[">", "<"] = "<"

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
    pyname: str
    parse_fn: Callable | None
    format: Literal["float32", "uint32", "int32", "szname", "node"] = "int32"


FEBIO_TAG = int(0x00464542)


def parse_char64(buffer: bytes) -> str:
    data = np.frombuffer(buffer, dtype=ENDIAN + "S1")
    data = data.tobytes()
    str_end = data.find(b"\x00")
    data = data[0:str_end].decode("utf-8")
    return data


def parse_char_array(buffer: bytes) -> str:
    data = np.frombuffer(buffer, dtype=ENDIAN + "S1")
    data = data.tobytes()
    str_start = data.rfind(b"\x00")
    data = data[str_start + 1 :].decode("utf-8")
    return data


def parse_uint32(buffer: bytes) -> np.ndarray:
    return np.frombuffer(buffer, dtype=ENDIAN + "u32")


def parse_float32(buffer: bytes) -> np.ndarray:
    return np.frombuffer(buffer, dtype=ENDIAN + "f32")


def parse_node3(buffer: bytes) -> np.ndarray:
    return np.frombuffer(
        buffer,
        dtype=[
            ("id", ENDIAN + "u32"),
            ("x", ENDIAN + "f32"),
            ("y", ENDIAN + "f32"),
            ("z", ENDIAN + "f32"),
        ],
    )


def parse_node2(buffer: bytes) -> np.ndarray:
    return np.frombuffer(
        buffer,
        dtype=[
            ("id", ENDIAN + "u32"),
            ("x", ENDIAN + "f32"),
            ("y", ENDIAN + "f32"),
        ],
    )


# TAG_LUT = {
#     # Root/
#     # Root/Header
#     int(0x01000000): Xtag(name="PLT_ROOT", level=0, pyname="root"),
#     int(0x1010000): Xtag(name="PLT_HEADER", level=0, pyname="header"),
#     int(0x01010001): Xtag(name="PLT_HDR_VERSION", level=1, pyname="version", leaf=True),
#     int(0x01010004): Xtag(name="PLT_HDR_COMPRESSION", level=1, pyname="compression", leaf=True),
#     int(0x01010005): Xtag(name="PLT_HDR_AUTHOR", level=1, pyname="author", leaf=True),
#     int(0x01010006): Xtag(name="PLT_HDR_SOFTWARE", level=1, pyname="software", leaf=True),
#     int(0x01010007): Xtag(
#         name="PLT_HDR_UNITS", level=1, pyname="units", leaf=True, format="szname"
#     ),
#     # Root/Dictionary
#     int(0x01020000): Xtag(name="PLT_DICTIONARY", level=0, pyname="dictionary"),
#     int(0x01021000): Xtag(name="PLT_DIC_GLOBAL", level=1, pyname="dic_global"),
#     int(0x01023000): Xtag(name="PLT_DIC_NODAL", level=1, pyname="dic_nodal"),
#     int(0x01024000): Xtag(name="PLT_DIC_DOMAIN", level=1, pyname="dic_domain"),
#     int(0x01025000): Xtag(name="PLT_DIC_SURFACE", level=1, pyname="dic_surface"),
#     int(0x01026000): Xtag(name="PLT_DIC_EDGE", level=1, pyname="dic_edge"),
#     int(0x01020001): Xtag(name="PLT_DIC_ITEM", level=2, pyname="item"),
#     int(0x01020002): Xtag(name="PLT_DIC_ITEM_TYPE", level=3, pyname="itype", leaf=True),
#     int(0x01020003): Xtag(name="PLT_DIC_ITEM_FMT", level=3, pyname="iformat", leaf=True),
#     int(0x01020004): Xtag(
#         name="PLT_DIC_ITEM_NAME", level=3, pyname="name", leaf=True, format="szname"
#     ),
#     int(0x01020005): Xtag(name="PLT_DIC_ITEM_ARRAYSIZE", level=3, pyname="array_size", leaf=True),
#     int(0x01020006): Xtag(
#         name="PLT_DIC_ITEM_ARRAYNAME", level=3, pyname="array_name", leaf=True, format="szname"
#     ),
#     int(0x01020007): Xtag(
#         name="PLT_DIC_ITEM_UNITS", level=3, pyname="units", leaf=True, format="szname"
#     ),
#     # Mesh/
#     int(0x01040000): Xtag(name="PLT_MESH", level=0, pyname="mesh"),
#     # Mesh/Nodes
#     int(0x01041000): Xtag(name="PLT_NODE_SECTION", level=1, pyname="nodes"),
#     int(0x01041100): Xtag(name="PLT_NODE_HEADER", level=2, pyname="header"),
#     int(0x01041101): Xtag(name="PLT_NODE_SIZE", level=3, pyname="nnodes", leaf=True),
#     int(0x01041102): Xtag(name="PLT_NODE_DIM", level=3, pyname="dimension", leaf=True),
#     int(0x01041103): Xtag(name="PLT_NODE_NAME", level=3, pyname="name", leaf=True, format="szname"),
#     int(0x01041200): Xtag(
#         name="PLT_NODE_COORDS", level=3, pyname="coords", leaf=True, format="node"
#     ),
#     # Mesh/Domains
#     int(0x01042000): Xtag(name="PLT_DOMAIN_SECTION", level=1, pyname="domains"),
#     # Mesh/Domains/Domain
#     int(0x01042100): Xtag(name="PLT_DOMAIN", level=2, pyname="domain"),
#     int(0x01042101): Xtag(name="PLT_DOMAIN_HDR", level=3, pyname="header"),
#     int(0x01042102): Xtag(name="PLT_DOM_ELEM_TYPE", level=4, pyname="etype", leaf=True),
#     int(0x01042103): Xtag(name="PLT_DOM_PART_ID", level=4, pyname="id", leaf=True),
#     int(0x01032104): Xtag(name="PLT_DOM_ELEMS", level=4, pyname="nelems", leaf=True),
#     int(0x01032105): Xtag(name="PLT_DOM_NAME", level=4, pyname="name", leaf=True, format="szname"),
#     int(0x01042200): Xtag(name="PLT_DOM_ELEM_LIST", level=4, pyname="elements", leaf=False),
#     int(0x01042201): Xtag(name="PLT_ELEMENT", level=5, pyname="element", leaf=True),
#     # Mesh/Surfaces
#     int(0x01043000): Xtag(name="PLT_SURFACE_SECTION", level=1, pyname="surfaces"),
#     # Mesh/Surfaces/Surface
#     int(0x01043100): Xtag(name="PLT_SURFACE", level=2, pyname="surface"),
#     int(0x01043101): Xtag(name="PLT_SURFACE_HDR", level=3, pyname="header"),
#     int(0x01043102): Xtag(name="PLT_SURFACE_ID", level=4, pyname="id", leaf=True),
#     int(0x01043103): Xtag(name="PLT_SURFACE_FACES", level=4, pyname="nfaces", leaf=True),
#     int(0x01043104): Xtag(
#         name="PLT_SURFACE_NAME", level=4, pyname="name", leaf=True, format="szname"
#     ),
#     int(0x01043105): Xtag(
#         name="PLT_SURFACE_MAX_FACET_NODES", level=4, pyname="max_nodes", leaf=True
#     ),
#     int(0x01043200): Xtag(name="PLT_FACE_LIST", level=3, pyname="faces"),
#     int(0x01043201): Xtag(name="PLT_FACE", level=4, pyname="face", leaf=True),
#     int(0x01044000): Xtag(name="PLT_NODESET_SECTION", level=1, pyname="node_sets"),
#     int(0x01044100): Xtag(name="PLT_NODESET", level=2, pyname="node_set"),
#     int(0x01044101): Xtag(name="PLT_NODESET_HDR", level=3, pyname="header"),
#     int(0x01044102): Xtag(name="PLT_NODESET_ID", level=4, pyname="id", leaf=True),
#     int(0x01044103): Xtag(
#         name="PLT_NODESET_NAME", level=4, pyname="name", leaf=True, format="szname"
#     ),
#     int(0x01044104): Xtag(name="PLT_NODESET_SIZE", level=4, pyname="nnodes", leaf=True),
#     int(0x01044200): Xtag(name="PLT_NODESET_LIST", level=4, pyname="nodes", leaf=True),
#     int(0x01045000): Xtag(name="PLT_PARTS_SECTION", level=1, pyname="parts"),
#     int(0x01045100): Xtag(name="PLT_PART", level=2, pyname="part"),
#     int(0x01045101): Xtag(name="PLT_PART_ID", level=3, pyname="id", leaf=True),
#     int(0x01045102): Xtag(name="PLT_PART_NAME", level=3, pyname="name", leaf=True, format="szname"),
#     # Mesh/ElementSets
#     # element set section was added in 4.1
#     int(0x01046000): Xtag(name="PLT_ELEMENTSET_SECTION", level=1, pyname="element_sets"),
#     # Mesh/ElementSets/ElementSet
#     int(0x01046100): Xtag(name="PLT_ELEMENTSET", level=2, pyname="element_set"),
#     int(0x01046101): Xtag(name="PLT_ELEMENTSET_HDR", level=3, pyname="header"),
#     int(0x01046102): Xtag(name="PLT_ELEMENTSET_ID", level=4, pyname="id", leaf=True),
#     int(0x01046103): Xtag(
#         name="PLT_ELEMENTSET_NAME", level=4, pyname="name", leaf=True, format="szname"
#     ),
#     int(0x01046104): Xtag(name="PLT_ELEMENTSET_SIZE", level=4, pyname="nelems", leaf=True),
#     int(0x01046200): Xtag(name="PLT_ELEMENTSET_LIST", level=4, pyname="elements", leaf=True),
#     # Mesh/FacetSets
#     # facet set section was added in 4.1
#     int(0x01047000): Xtag(name="PLT_FACETSET_SECTION", level=1, pyname="facet_sets"),
#     # Mesh/FacetSets/FacetSet
#     int(0x01047100): Xtag(name="PLT_FACETSET", level=2, pyname="facet_set"),
#     int(0x01047101): Xtag(name="PLT_FACETSET_HDR", level=3, pyname="header"),
#     int(0x01047102): Xtag(name="PLT_FACETSET_ID", level=4, pyname="id", leaf=True),
#     int(0x01047103): Xtag(
#         name="PLT_FACETSET_NAME", level=4, pyname="name", leaf=True, format="szname"
#     ),
#     int(0x01047104): Xtag(name="PLT_FACETSET_SIZE", level=4, pyname="nfacets", leaf=True),
#     int(0x01047105): Xtag(name="PLT_FACETSET_MAXNODES", level=4, pyname="max_nodes", leaf=True),
#     int(0x01047200): Xtag(name="PLT_FACETSET_LIST", level=3, pyname="facets"),
#     int(0x01047201): Xtag(name="PLT_FACET", level=4, pyname="facet", leaf=True),
#     # Mesh/Edges
#     int(0x01048000): Xtag(name="PLT_EDGE_SECTION", level=1, pyname="edges"),
#     # Mesh/Edges/Edge
#     int(0x01048100): Xtag(name="PLT_EDGE", level=2, pyname="edge"),
#     int(0x01048101): Xtag(name="PLT_EDGE_HDR", level=3, pyname="header"),
#     int(0x01048102): Xtag(name="PLT_EDGE_ID", level=4, pyname="id", leaf=True),
#     int(0x01048103): Xtag(name="PLT_EDGE_LINES", level=4, pyname="lines", leaf=True),
#     int(0x01048104): Xtag(name="PLT_EDGE_NAME", level=4, pyname="name", leaf=True, format="szname"),
#     int(0x01048105): Xtag(name="PLT_EDGE_MAX_NODES", level=4, pyname="max_nodes", leaf=True),
#     # Mesh/Edges/EdgeList
#     int(0x01048200): Xtag(name="PLT_EDGE_LIST", level=2, pyname="edges", leaf=True),
#     # Mesh/Edges/EdgeList/Line
#     int(0x01048201): Xtag(name="PLT_LINE", level=3, pyname="line", leaf=True),
#     # Mesh/Objects
#     int(0x01050000): Xtag(name="PLT_OBJECTS_SECTION", level=1, pyname="objects"),
#     # Mesh/Objects/Object
#     int(0x01050001): Xtag(name="PLT_OBJECT_ID", level=2, pyname="id", leaf=True),
#     int(0x01050002): Xtag(
#         name="PLT_OBJECT_NAME", level=2, pyname="name", leaf=True, format="szname"
#     ),
#     int(0x01050003): Xtag(name="PLT_OBJECT_TAG", level=2, pyname="tag", leaf=True),
#     int(0x01050004): Xtag(
#         name="PLT_OBJECT_POS", level=2, pyname="pos", leaf=True, format="float32"
#     ),
#     int(0x01050005): Xtag(
#         name="PLT_OBJECT_ROT", level=2, pyname="rot", leaf=True, format="float32"
#     ),
#     int(0x01050006): Xtag(
#         name="PLT_OBJECT_DATA", level=2, pyname="data", leaf=True, format="float32"
#     ),
#     # Mesh/Objects/Object/Point
#     int(0x01051000): Xtag(name="PLT_POINT_OBJECT", level=3, pyname="point"),
#     int(0x01051001): Xtag(
#         name="PLT_POINT_COORD", level=4, pyname="coord", leaf=True, format="float32"
#     ),
#     # Mesh/Objects/Object/Line
#     int(0x01052000): Xtag(name="PLT_LINE_OBJECT", level=3, pyname="line"),
#     int(0x01052001): Xtag(
#         name="PLT_LINE_COORDS", level=4, pyname="coords", leaf=True, format="float32"
#     ),
#     # State/
#     int(0x02000000): Xtag(name="PLT_STATE", level=0, pyname="state"),
#     # State/Header
#     int(0x02010000): Xtag(name="PLT_STATE_HEADER", level=1, pyname="header"),
#     int(0x02010001): Xtag(name="PLT_STATE_HDR_ID", level=2, pyname="id", leaf=True),
#     int(0x02010002): Xtag(
#         name="PLT_STATE_HDR_TIME", level=2, pyname="time", leaf=True, format="float32"
#     ),
#     int(0x02010003): Xtag(name="PLT_STATE_STATUS", level=2, pyname="status", leaf=True),
#     # State/Data
#     int(0x02020000): Xtag(name="PLT_STATE_DATA", level=1, pyname="state_data"),
#     int(0x02020001): Xtag(name="PLT_STATE_VARIABLE", level=3, pyname="variable"),
#     int(0x02020002): Xtag(name="PLT_STATE_VAR_ID", level=4, pyname="id", leaf=True),
#     int(0x02020003): Xtag(
#         name="PLT_STATE_VAR_DATA", level=4, pyname="data", leaf=True, format="float32"
#     ),
#     int(0x02020100): Xtag(name="PLT_GLOBAL_DATA", level=2, pyname="data"),
#     int(0x02020300): Xtag(name="PLT_NODE_DATA", level=2, pyname="data"),
#     int(0x02020400): Xtag(name="PLT_ELEMENT_DATA", level=2, pyname="data"),
#     int(0x02020500): Xtag(name="PLT_FACE_DATA", level=2, pyname="data"),
#     int(0x02020600): Xtag(name="PLT_EDGE_DATA", level=2, pyname="data"),
#     # State/MeshState
#     int(0x02030000): Xtag(name="PLT_MESH_STATE", level=1, pyname="mesh_state"),
#     # State/MeshState/ElementState
#     int(0x02030001): Xtag(name="PLT_ELEMENT_STATE", level=2, pyname="element_state", leaf=True),
#     # State/ObjectsState
#     int(0x02040000): Xtag(name="PLT_OBJECTS_STATE", level=1, pyname="objects_state"),
# }


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


@dataclass
class Surface:
    name: str
    id: int
    nfaces: int
    max_nodes: int
    faces: list[list[int]]


def assemble_surfaces(surface_section: dict):
    surfaces = []
    for surface in surface_section["data"]:
        surface_dict = {}
        for block in surface["data"]:
            match block["name"]:
                case "PLT_SURFACE_HDR":
                    for header_item in block["data"]:
                        surface_dict[header_item["pyname"]] = header_item["data"][0]
                case "PLT_FACE_LIST":
                    surface_dict["faces"] = []
                    for face_list_item in block["data"]:
                        surface_dict["faces"].append(list(face_list_item["data"]))
                case _:
                    continue

        surfaces.append(Surface(**surface_dict))
    return surfaces


@dataclass
class Domain:
    id: int
    name: str
    etype: int
    nelems: int
    elements: list[list[int]]


def assemble_domains(domain_section: dict):
    domains = []
    for domain in domain_section["data"]:
        domain_dict = {}
        for domain_item in domain["data"]:
            match domain_item["name"]:
                case "PLT_DOMAIN_HDR":
                    for header_item in domain_item["data"]:
                        domain_dict[header_item["pyname"]] = header_item["data"][0]
                case "PLT_DOM_ELEM_LIST":
                    domain_dict["elements"] = []
                    for elem_list_item in domain_item["data"]:
                        domain_dict["elements"].append(list(elem_list_item["data"]))
        domains.append(Domain(**domain_dict))
    return domains


@dataclass
class Nodes:
    dimension: int
    nnodes: int
    ids: list[int]
    coords: list[list[float]]


def check_file_is_febio(buffer):
    if not np.frombuffer(buffer, dtype=_DTYPES["int32"], count=1)[0] == int(FEBIO_TAG):
        dtypes_to_little_endian(_DTYPES)
        if np.frombuffer(buffer, dtype=_DTYPES["int32"], count=1)[0] == int(FEBIO_TAG):
            log.info(
                "File is FEBio, but in Big Endian format -- will be byte-swapped to Little Endian"
            )
        else:
            raise ValueError("Invalid FEBio file")
    else:
        log.info("File is FEBio, and in Little Endian format")


def _unwrap_string(data: np.ndarray):
    if data.size == DI_NAME_SIZE:
        _data = data.tobytes()
        str_end = _data.find(b"\x00")
        _data = _data[0:str_end].decode("utf-8")
    elif data.size > 0:
        _data = data.tobytes()
        str_start = _data.rfind(b"\x00")
        _data = _data[str_start + 1 :].decode("utf-8")
    else:
        _data = ""
    return _data


def parse_prefix(buffer: bytes) -> tuple[int, int]:
    tag = np.frombuffer(buffer[0:4], dtype=_DTYPES["int32"])[0]
    offset = np.frombuffer(buffer[4:8], dtype=_DTYPES["int32"])[0]
    return tag, offset


@dataclass
class DicItem:
    name: str
    itype: int
    iformat: int
    array_size: int
    units: str | None = None


def _parse_dic_item(buffer: bytes):
    i = 0
    item_dict = {}
    while i < len(buffer) - 8:
        tag, offset = parse_prefix(buffer[i : i + 8])
        data = np.frombuffer(buffer[i + 8 : i + 8 + offset], dtype=_DTYPES[TAG_LUT[tag].format])
        if data.size == 1:
            data = data[0]
        if TAG_LUT[tag].format == "szname":
            data = _unwrap_string(data)
        item_dict[TAG_LUT[tag].pyname] = data
        i += 8 + offset
    return DicItem(**item_dict)


def parse_dictionary(buffer: bytes) -> dict[str, list[DicItem]]:
    i = 0
    section_keys = (
        "PLT_DIC_GLOBAL",
        "PLT_DIC_NODAL",
        "PLT_DIC_DOMAIN",
        "PLT_DIC_SURFACE",
        "PLT_DIC_EDGE",
    )
    xdictionary = {key: [] for key in section_keys}
    current_key = None
    while i < len(buffer) - 8:
        tag, offset = parse_prefix(buffer[i : i + 8])
        if TAG_LUT[tag].name == "PLT_DIC_ITEM":
            item = _parse_dic_item(buffer[i + 8 : i + 8 + offset])
            i += 8 + offset
            if current_key is None:
                raise ValueError("Unexpected PLT_DIC_ITEM without a preceding key")
            xdictionary[current_key].append(item)
        elif TAG_LUT[tag].name in section_keys:
            current_key = TAG_LUT[tag].name
            i += 8
        else:
            i += 8
    return xdictionary


def parse_root(buffer: bytes, f):
    pass


def parse_header(buffer: bytes, f):
    i = 0
    while i < len(buffer) - 8:
        tag, offset = parse_prefix(buffer[i : i + 8])
        f["/"].attrs[TAG_LUT[tag].name] = np.frombuffer(
            buffer[i + 8 : i + 8 + offset], dtype=_DTYPES[TAG_LUT[tag].format]
        )
        i += 8 + offset


def assemble_nodes(node_section: dict):
    node_dict = {}
    for node_item in node_section["data"]:
        match node_item["name"]:
            case "PLT_NODE_HEADER":
                for header_item in node_item["data"]:
                    node_dict[header_item["pyname"]] = header_item["data"][0]
            case "PLT_NODE_COORDS":
                node_dict["ids"] = [node[0] for node in node_item["data"]]
                node_dict["coords"] = [node.tolist()[1:] for node in node_item["data"]]
    return Nodes(**node_dict)


def _parse_node_header(buffer: bytes):
    i = 0
    header_dict = {}
    while i < len(buffer) - 8:
        tag, offset = parse_prefix(buffer[i : i + 8])
        child = buffer[i + 8 : i + 8 + offset]
        header_dict[TAG_LUT[tag].pyname] = np.frombuffer(child, dtype=_DTYPES[TAG_LUT[tag].format])
        i += 8 + offset
    return header_dict


def _parse_node_section(buffer: bytes) -> dict[str, Any]:
    node_dict = {}
    i = 0
    while i < len(buffer) - 8:
        tag, offset = parse_prefix(buffer[i : i + 8])
        match TAG_LUT[tag].name:
            case "PLT_NODE_HEADER":
                node_dict = _parse_node_header(buffer[i + 8 : i + 8 + offset])
            case "PLT_NODE_COORDS":
                nodes = np.frombuffer(buffer[i + 8 : i + 8 + offset], dtype=_DTYPES["node"])
                node_dict["data"] = nodes
        i += 8 + offset
    return node_dict


def _parse_domain_header(buffer: bytes) -> dict[str, Any]:
    i = 0
    header_dict = {}
    while i < len(buffer) - 8:
        tag, offset = parse_prefix(buffer[i : i + 8])
        child = buffer[i + 8 : i + 8 + offset]
        data = np.frombuffer(child, dtype=_DTYPES[TAG_LUT[tag].format])
        if TAG_LUT[tag].format == "szname":
            data = _unwrap_string(data)
        header_dict[TAG_LUT[tag].pyname] = data
        i += 8 + offset
    return header_dict


def _parse_domain_elements(buffer: bytes) -> np.ndarray:
    elements = []
    i = 0
    while i < len(buffer) - 8:
        tag, offset = parse_prefix(buffer[i : i + 8])
        child = buffer[i + 8 : i + 8 + offset]
        elements.append(np.frombuffer(child, dtype=_DTYPES[TAG_LUT[tag].format]).reshape([1, -1]))
        i += 8 + offset
    elements = np.concatenate(elements, axis=0)
    return elements


def _parse_domain(buffer: bytes) -> dict[str, Any]:
    domain_dict = {}
    i = 0
    while i < len(buffer) - 8:
        tag, offset = parse_prefix(buffer[i : i + 8])
        child = buffer[i + 8 : i + 8 + offset]
        match TAG_LUT[tag].name:
            case "PLT_DOMAIN_HDR":
                domain_dict = _parse_domain_header(child)
            case "PLT_DOM_ELEM_LIST":
                domain_dict["elements"] = _parse_domain_elements(child)
        i += 8 + offset
    return domain_dict


def _parse_domain_section(buffer: bytes) -> list[dict[str, Any]]:
    i = 0
    domains = []
    while i < len(buffer) - 8:
        tag, offset = parse_prefix(buffer[i : i + 8])
        child = buffer[i + 8 : i + 8 + offset]
        if TAG_LUT[tag].name == "PLT_DOMAIN":
            domain_dict = _parse_domain(child)
            domains.append(domain_dict)
        i += 8 + offset
    return domains


def _parse_surface_header(buffer: bytes) -> dict[str, Any]:
    i = 0
    header_dict = {}
    while i < len(buffer) - 8:
        tag, offset = parse_prefix(buffer[i : i + 8])
        child = buffer[i + 8 : i + 8 + offset]
        data = np.frombuffer(child, dtype=_DTYPES[TAG_LUT[tag].format])
        if TAG_LUT[tag].format == "szname":
            data = _unwrap_string(data)
        header_dict[TAG_LUT[tag].pyname] = data
        i += 8 + offset
    return header_dict


def _parse_surface_faces(buffer: bytes) -> list[np.ndarray]:
    i = 0
    faces = []
    while i < len(buffer) - 8:
        tag, offset = parse_prefix(buffer[i : i + 8])
        child = buffer[i + 8 : i + 8 + offset]
        faces.append(np.frombuffer(child, dtype=_DTYPES[TAG_LUT[tag].format]))
        i += 8 + offset
    return faces


def _parse_surface(buffer: bytes) -> dict[str, Any]:
    surface_dict = {}
    i = 0
    while i < len(buffer) - 8:
        tag, offset = parse_prefix(buffer[i : i + 8])
        child = buffer[i + 8 : i + 8 + offset]
        match TAG_LUT[tag].name:
            case "PLT_SURFACE_HDR":
                surface_dict = _parse_surface_header(child)
            case "PLT_FACE_LIST":
                surface_dict["faces"] = _parse_surface_faces(child)
        i += 8 + offset
    return surface_dict


def _parse_surface_section(buffer: bytes):
    i = 0
    surfaces = []
    while i < len(buffer) - 8:
        tag, offset = parse_prefix(buffer[i : i + 8])
        child = buffer[i + 8 : i + 8 + offset]
        if TAG_LUT[tag].name == "PLT_SURFACE":
            surface_dict = _parse_surface(child)
            surfaces.append(surface_dict)
        i += 8 + offset
    return surfaces


def _parse_nodeset(buffer: bytes):
    nodeset_dict = {}
    i = 0
    while i < len(buffer) - 8:
        tag, offset = parse_prefix(buffer[i : i + 8])
        child = buffer[i + 8 : i + 8 + offset]
        match TAG_LUT[tag].name:
            case "PLT_NODESET_HDR":
                nodeset_dict = _parse_surface_header(child)
            case "PLT_NODESET_LIST":
                nodeset_dict["nodes"] = np.frombuffer(child, dtype=_DTYPES[TAG_LUT[tag].format])
        i += 8 + offset
    return nodeset_dict


def parse_nodeset_section(buffer: bytes):
    i = 0
    nodesets = []
    while i < len(buffer) - 8:
        tag, offset = parse_prefix(buffer[i : i + 8])
        child = buffer[i + 8 : i + 8 + offset]
        if TAG_LUT[tag].name == "PLT_NODESET":
            nodeset_dict = _parse_nodeset(child)
            nodesets.append(nodeset_dict)
        i += 8 + offset
    return nodesets


def _parse_elementset(buffer: bytes):
    elementset_dict = {}
    i = 0
    while i < len(buffer) - 8:
        tag, offset = parse_prefix(buffer[i : i + 8])
        child = buffer[i + 8 : i + 8 + offset]
        match TAG_LUT[tag].name:
            case "PLT_ELEMENTSET_HDR":
                elementset_dict = _parse_surface_header(child)
            case "PLT_ELEMENTSET_LIST":
                elementset_dict["elements"] = np.frombuffer(
                    child, dtype=_DTYPES[TAG_LUT[tag].format]
                )
        i += 8 + offset
    return elementset_dict


def parse_elementset_section(buffer: bytes):
    i = 0
    element_sets = []
    while i < len(buffer) - 8:
        tag, offset = parse_prefix(buffer[i : i + 8])
        child = buffer[i + 8 : i + 8 + offset]
        if TAG_LUT[tag].name == "PLT_ELEMENTSET":
            elementset_dict = _parse_elementset(child)
            element_sets.append(elementset_dict)
        i += 8 + offset
    return element_sets


def _parse_part(buffer: bytes):
    i = 0
    part_dict = {}
    while i < len(buffer) - 8:
        tag, offset = parse_prefix(buffer[i : i + 8])
        data = np.frombuffer(buffer[i + 8 : i + 8 + offset], dtype=_DTYPES[TAG_LUT[tag].format])
        if TAG_LUT[tag].format == "szname":
            data = _unwrap_string(data)
        part_dict[TAG_LUT[tag].pyname] = data
        i += 8 + offset
    return part_dict


def parse_parts_section(buffer: bytes):
    i = 0
    parts = []
    while i < len(buffer) - 8:
        tag, offset = parse_prefix(buffer[i : i + 8])
        child = buffer[i + 8 : i + 8 + offset]
        if TAG_LUT[tag].name == "PLT_PART":
            part_dict = _parse_part(child)
            parts.append(part_dict)
        i += 8 + offset
    return parts


def _parse_object(buffer: bytes):
    i = 0
    object_dict = {}
    while i < len(buffer) - 8:
        tag, offset = parse_prefix(buffer[i : i + 8])
        data = np.frombuffer(buffer[i + 8 : i + 8 + offset], dtype=_DTYPES[TAG_LUT[tag].format])
        if TAG_LUT[tag].format == "szname":
            data = _unwrap_string(data)
        object_dict[TAG_LUT[tag].pyname] = data
        i += 8 + offset
    return object_dict


def parse_objects_section(buffer: bytes):
    i = 0
    objects = {"points": [], "lines": []}
    while i < len(buffer) - 8:
        tag, offset = parse_prefix(buffer[i : i + 8])
        child = buffer[i + 8 : i + 8 + offset]
        match TAG_LUT[tag].name:
            case "PLT_POINT_OBJECT":
                objects["points"].append(_parse_object(child))
            case "PLT_LINE_OBJECT":
                objects["lines"].append(_parse_object(child))
        i += 8 + offset
    return objects


def parse_mesh(buffer: bytes, mesh_cnt: int, f):
    i = 0
    while i < len(buffer) - 8:
        tag, offset = parse_prefix(buffer[i : i + 8])
        child = buffer[i + 8 : i + 8 + offset]
        match TAG_LUT[tag].name:
            case "PLT_NODE_SECTION":
                nodes = _parse_node_section(child)
                dset_path = f"/meshes/{mesh_cnt}/nodes"
                f.create_dataset(dset_path, data=nodes["data"], dtype=_DTYPES["node"])
                i += 8 + offset
            case "PLT_DOMAIN_SECTION":
                domains = _parse_domain_section(child)
                for domain in domains:
                    dset_path = f"/meshes/{mesh_cnt}/domains/{domain['name']}"
                    f.create_dataset(dset_path, data=domain["elements"], dtype=_DTYPES["int32"])
                    for key, value in domain.items():
                        if not key == "elements":
                            f[dset_path].attrs[key] = value
                i += 8 + offset
            case "PLT_SURFACE_SECTION":
                surfaces = _parse_surface_section(child)
                for surface in surfaces:
                    dset_path = f"/meshes/{mesh_cnt}/surfaces/{surface['name']}"
                    f.create_dataset(dset_path, data=surface["faces"], dtype=_DTYPES["int32"])
                    for key, value in surface.items():
                        if not key == "surfaces":
                            f[dset_path].attrs[key] = value
                i += 8 + offset
            case "PLT_NODESET_SECTION":
                nodesets = parse_nodeset_section(child)
                for nodeset in nodesets:
                    if nodeset["name"] == "":
                        nodeset["name"] = nodeset["id"][0]
                    dset_path = f"/meshes/{mesh_cnt}/nodesets/{nodeset['name']}"
                    f.create_dataset(dset_path, data=nodeset["nodes"], dtype=_DTYPES["int32"])
                    for key, value in nodeset.items():
                        if not key == "nodes":
                            f[dset_path].attrs[key] = value
                i += 8 + offset
            case "PLT_ELEMENTSET_SECTION":
                elementsets = parse_elementset_section(child)
                for elementset in elementsets:
                    dset_path = f"/meshes/{mesh_cnt}/elementsets/{elementset['name']}"
                    f.create_dataset(dset_path, data=elementset["elements"], dtype=_DTYPES["int32"])
                    for key, value in elementset.items():
                        if not key == "elements":
                            f[dset_path].attrs[key] = value
                i += 8 + offset
            case "PLT_PARTS_SECTION":
                parts = parse_parts_section(child)
                i += 8 + offset
            case "PLT_OBJECTS_SECTION":
                objects = parse_objects_section(child)
                i += 8 + offset
            case _:
                print(TAG_LUT[tag].name)
                i += 8 + offset


def _parse_state_header(buffer: bytes):
    i = 0
    header_dict = {}
    while i < len(buffer) - 8:
        tag, offset = parse_prefix(buffer[i : i + 8])
        child = buffer[i + 8 : i + 8 + offset]
        header_dict[TAG_LUT[tag].pyname] = np.frombuffer(child, dtype=_DTYPES[TAG_LUT[tag].format])
        i += 8 + offset
    return header_dict


def _parse_mesh_state(buffer: bytes):
    i = 0
    mesh_dict = {}
    while i < len(buffer) - 8:
        tag, offset = parse_prefix(buffer[i : i + 8])
        child = buffer[i + 8 : i + 8 + offset]
        mesh_dict[TAG_LUT[tag].pyname] = np.frombuffer(child, dtype=_DTYPES[TAG_LUT[tag].format])
        i += 8 + offset
    return mesh_dict


def _parse_objects_state(buffer: bytes):
    i = 0
    objects_dict = {"points": [], "lines": []}
    while i < len(buffer) - 8:
        tag, offset = parse_prefix(buffer[i : i + 8])
        match TAG_LUT[tag].name:
            case "PLT_POINT_OBJECT":
                objects_dict["points"].append(_parse_object(buffer[i + 8 : i + 8 + offset]))
            case "PLT_LINE_OBJECT":
                objects_dict["lines"].append(_parse_object(buffer[i + 8 : i + 8 + offset]))
            case _:
                print(TAG_LUT[tag].name)
                pass
        i += 8 + offset
    return objects_dict


def _parse_state_variable(buffer: bytes):
    i = 0
    state_dict = {"data": {}}
    while i < len(buffer) - 8:
        tag, offset = parse_prefix(buffer[i : i + 8])
        state_dict[TAG_LUT[tag].pyname] = np.frombuffer(
            buffer[i + 8 : i + 8 + offset], dtype=_DTYPES[TAG_LUT[tag].format]
        )
        i += 8 + offset
        tag, offset = parse_prefix(buffer[i : i + 8])
        child = buffer[i + 8 : i + 8 + offset]
        j = 0
        while j < offset:
            sid, offset2 = parse_prefix(child[j : j + 8])
            state_dict["data"][sid] = np.frombuffer(
                child[j + 8 : j + 8 + offset2], dtype=_DTYPES[TAG_LUT[tag].format]
            )
            j += 8 + offset2
        i += 8 + offset
    return state_dict


def _parse_data(buffer: bytes):
    i = 0
    data = []
    while i < len(buffer) - 8:
        _, offset = parse_prefix(buffer[i : i + 8])
        data.append(_parse_state_variable(buffer[i + 8 : i + 8 + offset]))
        i += 8 + offset
    return data


def _parse_state_data(buffer: bytes):
    state_data_dict = {}
    i = 0
    while i < len(buffer) - 8:
        tag, offset = parse_prefix(buffer[i : i + 8])
        match TAG_LUT[tag].name:
            case "PLT_NODE_DATA":
                state_data_dict["node_data"] = _parse_data(buffer[i + 8 : i + 8 + offset])
            case "PLT_ELEMENT_DATA":
                data = _parse_data(buffer[i + 8 : i + 8 + offset])
                state_data_dict["element_data"] = _parse_data(buffer[i + 8 : i + 8 + offset])
            case "PLT_OBJECT_DATA":
                data = _parse_data(buffer[i + 8 : i + 8 + offset])
                state_data_dict["object_data"] = _parse_data(buffer[i + 8 : i + 8 + offset])
            case _:
                print(TAG_LUT[tag].name)
                pass
        i += 8 + offset
    return state_data_dict


def parse_state(buffer: bytes):
    i = 0
    while i < len(buffer) - 8:
        tag, offset = parse_prefix(buffer[i : i + 8])
        child = buffer[i + 8 : i + 8 + offset]
        match TAG_LUT[tag].name:
            case "PLT_STATE_HEADER":
                _parse_state_header(child)
            case "PLT_MESH_STATE":
                _parse_mesh_state(child)
            case "PLT_OBJECTS_STATE":
                _parse_objects_state(child)
            case "PLT_STATE_DATA":
                _parse_state_data(child)
            case _:
                pass
        i += offset + 8


def parse_blocks(buffer, f, data_offset=0, max_depth=MAX_DEPTH):
    i = 0
    xdictionary = None
    mesh_cnt = 0
    state_cnt = 0
    while i < (len(buffer) - 8):
        tag, offset = parse_prefix(buffer[i : i + 8])
        child = buffer[i + 8 : i + 8 + offset]
        match TAG_LUT[tag].name:
            case "PLT_ROOT":
                j = 0
                while j < offset:
                    tag, offset2 = parse_prefix(child[j : j + 8])
                    if TAG_LUT[tag].name == "PLT_HEADER":
                        parse_header(child[j + 8 : j + 8 + offset2], f)
                    elif TAG_LUT[tag].name == "PLT_DICTIONARY":
                        xdictionary = parse_dictionary(child[j + 8 : j + 8 + offset2])
                    j += offset2 + 8
            case "PLT_MESH":
                parse_mesh(child, mesh_cnt, f)
                mesh_cnt += 1
            case "PLT_STATE":
                parse_state(child)
                state_cnt += 1
        i += 8 + offset
    #     try:
    #         TAG_LUT[tag]
    #     except KeyError:
    #         log.warning(f"Unknown tag {tag:#08x}")
    #         block["data"] = child
    #         blocks.append(block)
    #         i += 8 + count
    #         continue
    #     if TAG_LUT[tag].leaf:
    #         max_depth = MAX_DEPTH
    #         if TAG_LUT[tag].name == "PLT_STATE_VAR_DATA":
    #             data = {}
    #             j = 0
    #             total_size = 0
    #             while j < len(child):
    #                 region_id = np.frombuffer(child[j : j + 4], count=1, dtype=_DTYPES["int32"])[0]
    #                 region_size = np.frombuffer(
    #                     child[j + 4 : j + 8], count=1, dtype=_DTYPES["int32"]
    #                 )[0]
    #                 data[region_id] = np.frombuffer(
    #                     child[j + 8 : j + 8 + region_size],
    #                     dtype=_DTYPES[TAG_LUT[tag].format],
    #                 )
    #                 total_size += region_size
    #                 j += region_size + 8
    #             block["data"] = data
    #             block["size"] = total_size
    #         else:
    #             block["data"] = np.frombuffer(
    #                 child,
    #                 dtype=_DTYPES[TAG_LUT[tag].format],
    #                 offset=0,
    #                 count=count // _DTYPES_SIZE[TAG_LUT[tag].format],
    #             )
    #         if TAG_LUT[tag].format == "szname":
    #             assert isinstance(block["data"], np.ndarray)
    #             if block["size"] == DI_NAME_SIZE:
    #                 block["data"] = block["data"].tobytes()
    #                 str_end = block["data"].find(b"\x00")
    #                 block["data"] = [block["data"][0:str_end].decode("utf-8")]
    #             elif block["size"] > 0:
    #                 block["data"] = block["data"].tobytes()
    #                 str_start = block["data"].rfind(b"\x00")
    #                 block["data"] = [block["data"][str_start + 1 :].decode("utf-8")]
    #             else:
    #                 block["data"] = [""]
    #     else:
    #         if max_depth > 1:
    #             block["data"] = parse_blocks(
    #                 child, f, data_offset=data_offset + i + 8, max_depth=max_depth - 1
    #             )
    #     blocks.append(block)
    #     i += 8 + count
    # return blocks


@dataclass
class Header:
    version: int
    compression: int
    software: int
    author: str | None = None
    units: str | None = None


# ROOT_HDR_LUT = {
#     "PLT_HDR_VERSION": "version",
#     "PLT_HDR_COMPRESSION": "compression",
#     "PLT_HDR_AUTHOR": "author",
#     "PLT_HDR_SOFTWARE": "software",
#     "PLT_HDR_UNITS": "units",
# }


@dataclass
class Mesh:
    nodes: Nodes | None = None
    domains: list[Domain] | None = None
    surfaces: list[Surface] | None = None


@dataclass
class ElementData:
    id: int
    domain_ids: list[int]
    data: list[list[float]]


@dataclass
class NodeData:
    id: int
    data: list[float]


@dataclass
class State:
    time: float
    status: int
    element_data: list[ElementData]
    node_data: list[NodeData]


@dataclass
class XpltData:
    header: Header
    meshes: list[Mesh] = Field(default_factory=list)


def assemble_element_data(element_data: dict):
    element_data_dict = {}
    for block in element_data["data"]:
        match block["name"]:
            case "PLT_STATE_VARIABLE":
                element_data_dict[block["data"][0]["pyname"]] = block["data"][0]["data"][0]
                var_data = block["data"][1]["data"]
                domain_data = []
                domain_ids = []
                for key, value in var_data.items():
                    domain_data.append(pa.array(value, type=pa.float32()))
                    domain_ids.append(pa.array([key] * len(domain_data[-1]), type=pa.int32()))
                domain_data = pa.concat_arrays(domain_data)
                domain_ids = pa.concat_arrays(domain_ids)
                element_data = pa.table([domain_ids, domain_data], names=["DomainID", "Data"])
                element_data_dict["data"] = element_data

    return element_data_dict


def parse_xplt(filename: str):
    with open(filename, "rb") as fid:
        buffer = fid.read()
        check_file_is_febio(buffer)
        f = h5py.File("test.hdf5", "w")
        blocks = parse_blocks(buffer[4:], f)
        f.close()
        # data = {}
        # for block in blocks:
        #     match block["name"]:
        #         case "PLT_ROOT":
        #             for block2 in block["data"]:
        #                 match block2["name"]:
        #                     case "PLT_HEADER":
        #                         header_dict = {}
        #                         for header_item in block2["data"]:
        #                             header_dict[header_item["pyname"]] = header_item["data"][0]
        #                         data["header"] = Header(**header_dict)
        #                     case "PLT_DICTIONARY":
        #                         continue
        #                     case _:
        #                         continue

        #         case "PLT_MESH":
        #             nodes = None
        #             domains = None
        #             surfaces = None
        #             for block2 in block["data"]:
        #                 match block2["name"]:
        #                     case "PLT_NODE_SECTION":
        #                         nodes = assemble_nodes(block2)
        #                     case "PLT_DOMAIN_SECTION":
        #                         domains = assemble_domains(block2)
        #                     case "PLT_SURFACE_SECTION":
        #                         surfaces = assemble_surfaces(block2)
        #                     case _:
        #                         continue

        #             try:
        #                 data["meshes"].append(Mesh(nodes=nodes, domains=domains, surfaces=surfaces))
        #             except KeyError:
        #                 data["meshes"] = [Mesh(nodes=nodes, domains=domains, surfaces=surfaces)]

        #         case "PLT_STATE":
        #             state_dict = {"element_data": []}
        #             for block2 in block["data"]:
        #                 match block2["name"]:
        #                     case "PLT_STATE_HEADER":
        #                         for header_item in block2["data"]:
        #                             state_dict[header_item["pyname"]] = header_item["data"][0]
        #                     case "PLT_STATE_DATA":
        #                         for data_item in block2["data"]:
        #                             match data_item["name"]:
        #                                 case "PLT_ELEMENT_DATA":
        #                                     element_data = assemble_element_data(data_item)
        #                     case _:
        #                         continue

        #             pass
        # data_model = XpltData(**data)
        # log.info(TypeAdapter(XpltData).dump_json(data_model, indent=4).decode("utf-8"))
    TAG_LUT = {
        # Root/
        # Root/Header
        int(0x01000000): Xtag(name="PLT_ROOT", pyname="root", parse_fn=parse_root),
        int(0x1010000): Xtag(name="PLT_HEADER", pyname="header", parse_fn=parse_header),
        int(0x01010001): Xtag(
            name="PLT_HDR_VERSION",
            pyname="version",
            parse_fn=parse_uint32,
        ),
        int(0x01010004): Xtag(
            name="PLT_HDR_COMPRESSION", pyname="compression", parse_fn=parse_uint32
        ),
        int(0x01010005): Xtag(name="PLT_HDR_AUTHOR", pyname="author", parse_fn=parse_char64),
        int(0x01010006): Xtag(name="PLT_HDR_SOFTWARE", pyname="software", parse_fn=parse_uint32),
        int(0x01010007): Xtag(name="PLT_HDR_UNITS", pyname="units", parse_fn=parse_char64),
        # Root/Dictionary
        int(0x01020000): Xtag(
            name="PLT_DICTIONARY", pyname="dictionary", parse_fn=parse_dictionary
        ),
        int(0x01021000): Xtag(
            name="PLT_DIC_GLOBAL", pyname="dic_global", parse_fn=parse_dic_section
        ),
        int(0x01023000): Xtag(name="PLT_DIC_NODAL", pyname="dic_nodal", parse_fn=parse_dic_section),
        int(0x01024000): Xtag(
            name="PLT_DIC_DOMAIN", pyname="dic_domain", parse_fn=parse_dic_section
        ),
        int(0x01025000): Xtag(
            name="PLT_DIC_SURFACE", pyname="dic_surface", parse_fn=parse_dic_section
        ),
        int(0x01026000): Xtag(name="PLT_DIC_EDGE", pyname="dic_edge", parse_fn=parse_dic_section),
        int(0x01020001): Xtag(name="PLT_DIC_ITEM", pyname="item", parse_fn=_parse_dic_item),
        int(0x01020002): Xtag(name="PLT_DIC_ITEM_TYPE", level=3, pyname="itype", leaf=True),
        int(0x01020003): Xtag(name="PLT_DIC_ITEM_FMT", level=3, pyname="iformat", leaf=True),
        int(0x01020004): Xtag(
            name="PLT_DIC_ITEM_NAME", level=3, pyname="name", leaf=True, format="szname"
        ),
        int(0x01020005): Xtag(
            name="PLT_DIC_ITEM_ARRAYSIZE", level=3, pyname="array_size", leaf=True
        ),
        int(0x01020006): Xtag(
            name="PLT_DIC_ITEM_ARRAYNAME", level=3, pyname="array_name", leaf=True, format="szname"
        ),
        int(0x01020007): Xtag(
            name="PLT_DIC_ITEM_UNITS", level=3, pyname="units", leaf=True, format="szname"
        ),
        # Mesh/
        int(0x01040000): Xtag(name="PLT_MESH", level=0, pyname="mesh"),
        # Mesh/Nodes
        int(0x01041000): Xtag(name="PLT_NODE_SECTION", level=1, pyname="nodes"),
        int(0x01041100): Xtag(name="PLT_NODE_HEADER", level=2, pyname="header"),
        int(0x01041101): Xtag(name="PLT_NODE_SIZE", level=3, pyname="nnodes", leaf=True),
        int(0x01041102): Xtag(name="PLT_NODE_DIM", level=3, pyname="dimension", leaf=True),
        int(0x01041103): Xtag(
            name="PLT_NODE_NAME", level=3, pyname="name", leaf=True, format="szname"
        ),
        int(0x01041200): Xtag(
            name="PLT_NODE_COORDS", level=3, pyname="coords", leaf=True, format="node"
        ),
        # Mesh/Domains
        int(0x01042000): Xtag(name="PLT_DOMAIN_SECTION", level=1, pyname="domains"),
        # Mesh/Domains/Domain
        int(0x01042100): Xtag(name="PLT_DOMAIN", level=2, pyname="domain"),
        int(0x01042101): Xtag(name="PLT_DOMAIN_HDR", level=3, pyname="header"),
        int(0x01042102): Xtag(name="PLT_DOM_ELEM_TYPE", level=4, pyname="etype", leaf=True),
        int(0x01042103): Xtag(name="PLT_DOM_PART_ID", level=4, pyname="id", leaf=True),
        int(0x01032104): Xtag(name="PLT_DOM_ELEMS", level=4, pyname="nelems", leaf=True),
        int(0x01032105): Xtag(
            name="PLT_DOM_NAME", level=4, pyname="name", leaf=True, format="szname"
        ),
        int(0x01042200): Xtag(name="PLT_DOM_ELEM_LIST", level=4, pyname="elements", leaf=False),
        int(0x01042201): Xtag(name="PLT_ELEMENT", level=5, pyname="element", leaf=True),
        # Mesh/Surfaces
        int(0x01043000): Xtag(name="PLT_SURFACE_SECTION", level=1, pyname="surfaces"),
        # Mesh/Surfaces/Surface
        int(0x01043100): Xtag(name="PLT_SURFACE", level=2, pyname="surface"),
        int(0x01043101): Xtag(name="PLT_SURFACE_HDR", level=3, pyname="header"),
        int(0x01043102): Xtag(name="PLT_SURFACE_ID", level=4, pyname="id", leaf=True),
        int(0x01043103): Xtag(name="PLT_SURFACE_FACES", level=4, pyname="nfaces", leaf=True),
        int(0x01043104): Xtag(
            name="PLT_SURFACE_NAME", level=4, pyname="name", leaf=True, format="szname"
        ),
        int(0x01043105): Xtag(
            name="PLT_SURFACE_MAX_FACET_NODES", level=4, pyname="max_nodes", leaf=True
        ),
        int(0x01043200): Xtag(name="PLT_FACE_LIST", level=3, pyname="faces"),
        int(0x01043201): Xtag(name="PLT_FACE", level=4, pyname="face", leaf=True),
        int(0x01044000): Xtag(name="PLT_NODESET_SECTION", level=1, pyname="node_sets"),
        int(0x01044100): Xtag(name="PLT_NODESET", level=2, pyname="node_set"),
        int(0x01044101): Xtag(name="PLT_NODESET_HDR", level=3, pyname="header"),
        int(0x01044102): Xtag(name="PLT_NODESET_ID", level=4, pyname="id", leaf=True),
        int(0x01044103): Xtag(
            name="PLT_NODESET_NAME", level=4, pyname="name", leaf=True, format="szname"
        ),
        int(0x01044104): Xtag(name="PLT_NODESET_SIZE", level=4, pyname="nnodes", leaf=True),
        int(0x01044200): Xtag(name="PLT_NODESET_LIST", level=4, pyname="nodes", leaf=True),
        int(0x01045000): Xtag(name="PLT_PARTS_SECTION", level=1, pyname="parts"),
        int(0x01045100): Xtag(name="PLT_PART", level=2, pyname="part"),
        int(0x01045101): Xtag(name="PLT_PART_ID", level=3, pyname="id", leaf=True),
        int(0x01045102): Xtag(
            name="PLT_PART_NAME", level=3, pyname="name", leaf=True, format="szname"
        ),
        # Mesh/ElementSets
        # element set section was added in 4.1
        int(0x01046000): Xtag(name="PLT_ELEMENTSET_SECTION", level=1, pyname="element_sets"),
        # Mesh/ElementSets/ElementSet
        int(0x01046100): Xtag(name="PLT_ELEMENTSET", level=2, pyname="element_set"),
        int(0x01046101): Xtag(name="PLT_ELEMENTSET_HDR", level=3, pyname="header"),
        int(0x01046102): Xtag(name="PLT_ELEMENTSET_ID", level=4, pyname="id", leaf=True),
        int(0x01046103): Xtag(
            name="PLT_ELEMENTSET_NAME", level=4, pyname="name", leaf=True, format="szname"
        ),
        int(0x01046104): Xtag(name="PLT_ELEMENTSET_SIZE", level=4, pyname="nelems", leaf=True),
        int(0x01046200): Xtag(name="PLT_ELEMENTSET_LIST", level=4, pyname="elements", leaf=True),
        # Mesh/FacetSets
        # facet set section was added in 4.1
        int(0x01047000): Xtag(name="PLT_FACETSET_SECTION", level=1, pyname="facet_sets"),
        # Mesh/FacetSets/FacetSet
        int(0x01047100): Xtag(name="PLT_FACETSET", level=2, pyname="facet_set"),
        int(0x01047101): Xtag(name="PLT_FACETSET_HDR", level=3, pyname="header"),
        int(0x01047102): Xtag(name="PLT_FACETSET_ID", level=4, pyname="id", leaf=True),
        int(0x01047103): Xtag(
            name="PLT_FACETSET_NAME", level=4, pyname="name", leaf=True, format="szname"
        ),
        int(0x01047104): Xtag(name="PLT_FACETSET_SIZE", level=4, pyname="nfacets", leaf=True),
        int(0x01047105): Xtag(name="PLT_FACETSET_MAXNODES", level=4, pyname="max_nodes", leaf=True),
        int(0x01047200): Xtag(name="PLT_FACETSET_LIST", level=3, pyname="facets"),
        int(0x01047201): Xtag(name="PLT_FACET", level=4, pyname="facet", leaf=True),
        # Mesh/Edges
        int(0x01048000): Xtag(name="PLT_EDGE_SECTION", level=1, pyname="edges"),
        # Mesh/Edges/Edge
        int(0x01048100): Xtag(name="PLT_EDGE", level=2, pyname="edge"),
        int(0x01048101): Xtag(name="PLT_EDGE_HDR", level=3, pyname="header"),
        int(0x01048102): Xtag(name="PLT_EDGE_ID", level=4, pyname="id", leaf=True),
        int(0x01048103): Xtag(name="PLT_EDGE_LINES", level=4, pyname="lines", leaf=True),
        int(0x01048104): Xtag(
            name="PLT_EDGE_NAME", level=4, pyname="name", leaf=True, format="szname"
        ),
        int(0x01048105): Xtag(name="PLT_EDGE_MAX_NODES", level=4, pyname="max_nodes", leaf=True),
        # Mesh/Edges/EdgeList
        int(0x01048200): Xtag(name="PLT_EDGE_LIST", level=2, pyname="edges", leaf=True),
        # Mesh/Edges/EdgeList/Line
        int(0x01048201): Xtag(name="PLT_LINE", level=3, pyname="line", leaf=True),
        # Mesh/Objects
        int(0x01050000): Xtag(name="PLT_OBJECTS_SECTION", level=1, pyname="objects"),
        # Mesh/Objects/Object
        int(0x01050001): Xtag(name="PLT_OBJECT_ID", level=2, pyname="id", leaf=True),
        int(0x01050002): Xtag(
            name="PLT_OBJECT_NAME", level=2, pyname="name", leaf=True, format="szname"
        ),
        int(0x01050003): Xtag(name="PLT_OBJECT_TAG", level=2, pyname="tag", leaf=True),
        int(0x01050004): Xtag(
            name="PLT_OBJECT_POS", level=2, pyname="pos", leaf=True, format="float32"
        ),
        int(0x01050005): Xtag(
            name="PLT_OBJECT_ROT", level=2, pyname="rot", leaf=True, format="float32"
        ),
        int(0x01050006): Xtag(
            name="PLT_OBJECT_DATA", level=2, pyname="data", leaf=True, format="float32"
        ),
        # Mesh/Objects/Object/Point
        int(0x01051000): Xtag(name="PLT_POINT_OBJECT", level=3, pyname="point"),
        int(0x01051001): Xtag(
            name="PLT_POINT_COORD", level=4, pyname="coord", leaf=True, format="float32"
        ),
        # Mesh/Objects/Object/Line
        int(0x01052000): Xtag(name="PLT_LINE_OBJECT", level=3, pyname="line"),
        int(0x01052001): Xtag(
            name="PLT_LINE_COORDS", level=4, pyname="coords", leaf=True, format="float32"
        ),
        # State/
        int(0x02000000): Xtag(name="PLT_STATE", level=0, pyname="state"),
        # State/Header
        int(0x02010000): Xtag(name="PLT_STATE_HEADER", level=1, pyname="header"),
        int(0x02010001): Xtag(name="PLT_STATE_HDR_ID", level=2, pyname="id", leaf=True),
        int(0x02010002): Xtag(
            name="PLT_STATE_HDR_TIME", level=2, pyname="time", leaf=True, format="float32"
        ),
        int(0x02010003): Xtag(name="PLT_STATE_STATUS", level=2, pyname="status", leaf=True),
        # State/Data
        int(0x02020000): Xtag(name="PLT_STATE_DATA", level=1, pyname="state_data"),
        int(0x02020001): Xtag(name="PLT_STATE_VARIABLE", level=3, pyname="variable"),
        int(0x02020002): Xtag(name="PLT_STATE_VAR_ID", level=4, pyname="id", leaf=True),
        int(0x02020003): Xtag(
            name="PLT_STATE_VAR_DATA", level=4, pyname="data", leaf=True, format="float32"
        ),
        int(0x02020100): Xtag(name="PLT_GLOBAL_DATA", level=2, pyname="data"),
        int(0x02020300): Xtag(name="PLT_NODE_DATA", level=2, pyname="data"),
        int(0x02020400): Xtag(name="PLT_ELEMENT_DATA", level=2, pyname="data"),
        int(0x02020500): Xtag(name="PLT_FACE_DATA", level=2, pyname="data"),
        int(0x02020600): Xtag(name="PLT_EDGE_DATA", level=2, pyname="data"),
        # State/MeshState
        int(0x02030000): Xtag(name="PLT_MESH_STATE", level=1, pyname="mesh_state"),
        # State/MeshState/ElementState
        int(0x02030001): Xtag(name="PLT_ELEMENT_STATE", level=2, pyname="element_state", leaf=True),
        # State/ObjectsState
        int(0x02040000): Xtag(name="PLT_OBJECTS_STATE", level=1, pyname="objects_state"),
    }
