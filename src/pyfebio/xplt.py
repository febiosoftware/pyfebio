r"""
We reference:
    https://github.com/febiosoftware/FEBioStudio/blob/master/XPLTLib/xpltReader3.h
    commit: 7c7f171
as:
    xpltReader3.h:LINE_NUMBER
"""

import logging
from enum import Enum, auto
from typing import Any, Literal

import h5py
import numpy as np
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

_ENDIAN: Literal[">", "<"] = "<"

_DTYPES_SIZE = {
    "float32": 4,
    "uint32": 4,
    "int32": 4,
    "szname": 1,
    "node": 16,
}


def dtypes_to_little__ENDIAN(_DTYPES):
    """
    Uncommon these days, but if your XPLT file was created on a big-_ENDIAN machine,
    this will do a byte swap to little-_ENDIAN for all _DTYPES

    Note: szname being a byte string type will be unchanged
    """
    for key, value in _DTYPES.items():
        _DTYPES[key] = value.newbyteorder("<")


@dataclass
class Xtag:
    name: str
    pyname: str
    format: Literal["float32", "uint32", "int32", "szname", "node"] = "int32"


FEBIO_TAG = int(0x00464542)


def parse_char_array(buffer: bytes) -> str:
    data = np.frombuffer(buffer, dtype="S1")
    data = data.tobytes()
    if len(buffer) == DI_NAME_SIZE:
        str_end = data.find(b"\x00")
        data = data[0:str_end].decode("utf-8")
    else:
        str_start = data.rfind(b"\x00")
        data = data[str_start + 1 :].decode("utf-8")
    return data


def parse_uint32(buffer: bytes) -> np.ndarray:
    data = np.frombuffer(buffer, dtype=_ENDIAN + "u32")
    if data.size == 1:
        return data.item()
    return data


def parse_float32(buffer: bytes) -> np.ndarray:
    data = np.frombuffer(buffer, dtype=_ENDIAN + "f32")
    if data.size == 1:
        return data.item()
    return data


def parse_node3(buffer: bytes) -> np.ndarray:
    return np.frombuffer(
        buffer,
        dtype=[
            ("id", _ENDIAN + "u32"),
            ("x", _ENDIAN + "f32"),
            ("y", _ENDIAN + "f32"),
            ("z", _ENDIAN + "f32"),
        ],
    )


def parse_node2(buffer: bytes) -> np.ndarray:
    return np.frombuffer(
        buffer,
        dtype=[
            ("id", _ENDIAN + "u32"),
            ("x", _ENDIAN + "f32"),
            ("y", _ENDIAN + "f32"),
        ],
    )


TAG_LUT = {
    # Root/
    # Root/Header
    int(0x01000000): Xtag(name="PLT_ROOT", pyname="root"),
    int(0x1010000): Xtag(name="PLT_HEADER", pyname="header"),
    int(0x01010001): Xtag(
        name="PLT_HDR_VERSION",
        pyname="version",
    ),
    int(0x01010004): Xtag(
        name="PLT_HDR_COMPRESSION",
        pyname="compression",
    ),
    int(0x01010005): Xtag(
        name="PLT_HDR_AUTHOR",
        pyname="author",
    ),
    int(0x01010006): Xtag(
        name="PLT_HDR_SOFTWARE",
        pyname="software",
    ),
    int(0x01010007): Xtag(name="PLT_HDR_UNITS", pyname="units", format="szname"),
    # Root/Dictionary
    int(0x01020000): Xtag(name="PLT_DICTIONARY", pyname="dictionary"),
    int(0x01021000): Xtag(name="PLT_DIC_GLOBAL", pyname="dic_global"),
    int(0x01023000): Xtag(name="PLT_DIC_NODAL", pyname="dic_nodal"),
    int(0x01024000): Xtag(name="PLT_DIC_DOMAIN", pyname="dic_domain"),
    int(0x01025000): Xtag(name="PLT_DIC_SURFACE", pyname="dic_surface"),
    int(0x01026000): Xtag(name="PLT_DIC_EDGE", pyname="dic_edge"),
    int(0x01020001): Xtag(name="PLT_DIC_ITEM", pyname="item"),
    int(0x01020002): Xtag(
        name="PLT_DIC_ITEM_TYPE",
        pyname="itype",
    ),
    int(0x01020003): Xtag(
        name="PLT_DIC_ITEM_FMT",
        pyname="iformat",
    ),
    int(0x01020004): Xtag(name="PLT_DIC_ITEM_NAME", pyname="name", format="szname"),
    int(0x01020005): Xtag(
        name="PLT_DIC_ITEM_ARRAYSIZE",
        pyname="array_size",
    ),
    int(0x01020006): Xtag(name="PLT_DIC_ITEM_ARRAYNAME", pyname="array_name", format="szname"),
    int(0x01020007): Xtag(name="PLT_DIC_ITEM_UNITS", pyname="units", format="szname"),
    # Mesh/
    int(0x01040000): Xtag(name="PLT_MESH", pyname="mesh"),
    # Mesh/Nodes
    int(0x01041000): Xtag(name="PLT_NODE_SECTION", pyname="nodes"),
    int(0x01041100): Xtag(name="PLT_NODE_HEADER", pyname="header"),
    int(0x01041101): Xtag(
        name="PLT_NODE_SIZE",
        pyname="nnodes",
    ),
    int(0x01041102): Xtag(
        name="PLT_NODE_DIM",
        pyname="dimension",
    ),
    int(0x01041103): Xtag(name="PLT_NODE_NAME", pyname="name", format="szname"),
    int(0x01041200): Xtag(name="PLT_NODE_COORDS", pyname="coords", format="node"),
    # Mesh/Domains
    int(0x01042000): Xtag(name="PLT_DOMAIN_SECTION", pyname="domains"),
    # Mesh/Domains/Domain
    int(0x01042100): Xtag(name="PLT_DOMAIN", pyname="domain"),
    int(0x01042101): Xtag(name="PLT_DOMAIN_HDR", pyname="header"),
    int(0x01042102): Xtag(
        name="PLT_DOM_ELEM_TYPE",
        pyname="etype",
    ),
    int(0x01042103): Xtag(
        name="PLT_DOM_PART_ID",
        pyname="id",
    ),
    int(0x01032104): Xtag(
        name="PLT_DOM_ELEMS",
        pyname="nelems",
    ),
    int(0x01032105): Xtag(name="PLT_DOM_NAME", pyname="name", format="szname"),
    int(0x01042200): Xtag(name="PLT_DOM_ELEM_LIST", pyname="elements"),
    int(0x01042201): Xtag(
        name="PLT_ELEMENT",
        pyname="element",
    ),
    # Mesh/Surfaces
    int(0x01043000): Xtag(name="PLT_SURFACE_SECTION", pyname="surfaces"),
    # Mesh/Surfaces/Surface
    int(0x01043100): Xtag(name="PLT_SURFACE", pyname="surface"),
    int(0x01043101): Xtag(name="PLT_SURFACE_HDR", pyname="header"),
    int(0x01043102): Xtag(
        name="PLT_SURFACE_ID",
        pyname="id",
    ),
    int(0x01043103): Xtag(
        name="PLT_SURFACE_FACES",
        pyname="nfaces",
    ),
    int(0x01043104): Xtag(name="PLT_SURFACE_NAME", pyname="name", format="szname"),
    int(0x01043105): Xtag(
        name="PLT_SURFACE_MAX_FACET_NODES",
        pyname="max_nodes",
    ),
    int(0x01043200): Xtag(name="PLT_FACE_LIST", pyname="faces"),
    int(0x01043201): Xtag(
        name="PLT_FACE",
        pyname="face",
    ),
    int(0x01044000): Xtag(name="PLT_NODESET_SECTION", pyname="node_sets"),
    int(0x01044100): Xtag(name="PLT_NODESET", pyname="node_set"),
    int(0x01044101): Xtag(name="PLT_NODESET_HDR", pyname="header"),
    int(0x01044102): Xtag(
        name="PLT_NODESET_ID",
        pyname="id",
    ),
    int(0x01044103): Xtag(name="PLT_NODESET_NAME", pyname="name", format="szname"),
    int(0x01044104): Xtag(
        name="PLT_NODESET_SIZE",
        pyname="nnodes",
    ),
    int(0x01044200): Xtag(
        name="PLT_NODESET_LIST",
        pyname="nodes",
    ),
    int(0x01045000): Xtag(name="PLT_PARTS_SECTION", pyname="parts"),
    int(0x01045100): Xtag(name="PLT_PART", pyname="part"),
    int(0x01045101): Xtag(
        name="PLT_PART_ID",
        pyname="id",
    ),
    int(0x01045102): Xtag(name="PLT_PART_NAME", pyname="name", format="szname"),
    # Mesh/ElementSets
    # element set section was added in 4.1
    int(0x01046000): Xtag(name="PLT_ELEMENTSET_SECTION", pyname="element_sets"),
    # Mesh/ElementSets/ElementSet
    int(0x01046100): Xtag(name="PLT_ELEMENTSET", pyname="element_set"),
    int(0x01046101): Xtag(name="PLT_ELEMENTSET_HDR", pyname="header"),
    int(0x01046102): Xtag(
        name="PLT_ELEMENTSET_ID",
        pyname="id",
    ),
    int(0x01046103): Xtag(name="PLT_ELEMENTSET_NAME", pyname="name", format="szname"),
    int(0x01046104): Xtag(
        name="PLT_ELEMENTSET_SIZE",
        pyname="nelems",
    ),
    int(0x01046200): Xtag(
        name="PLT_ELEMENTSET_LIST",
        pyname="elements",
    ),
    # Mesh/FacetSets
    # facet set section was added in 4.1
    int(0x01047000): Xtag(name="PLT_FACETSET_SECTION", pyname="facet_sets"),
    # Mesh/FacetSets/FacetSet
    int(0x01047100): Xtag(name="PLT_FACETSET", pyname="facet_set"),
    int(0x01047101): Xtag(name="PLT_FACETSET_HDR", pyname="header"),
    int(0x01047102): Xtag(
        name="PLT_FACETSET_ID",
        pyname="id",
    ),
    int(0x01047103): Xtag(name="PLT_FACETSET_NAME", pyname="name", format="szname"),
    int(0x01047104): Xtag(
        name="PLT_FACETSET_SIZE",
        pyname="nfacets",
    ),
    int(0x01047105): Xtag(
        name="PLT_FACETSET_MAXNODES",
        pyname="max_nodes",
    ),
    int(0x01047200): Xtag(name="PLT_FACETSET_LIST", pyname="facets"),
    int(0x01047201): Xtag(
        name="PLT_FACET",
        pyname="facet",
    ),
    # Mesh/Edges
    int(0x01048000): Xtag(name="PLT_EDGE_SECTION", pyname="edges"),
    # Mesh/Edges/Edge
    int(0x01048100): Xtag(name="PLT_EDGE", pyname="edge"),
    int(0x01048101): Xtag(name="PLT_EDGE_HDR", pyname="header"),
    int(0x01048102): Xtag(
        name="PLT_EDGE_ID",
        pyname="id",
    ),
    int(0x01048103): Xtag(
        name="PLT_EDGE_LINES",
        pyname="lines",
    ),
    int(0x01048104): Xtag(name="PLT_EDGE_NAME", pyname="name", format="szname"),
    int(0x01048105): Xtag(
        name="PLT_EDGE_MAX_NODES",
        pyname="max_nodes",
    ),
    # Mesh/Edges/EdgeList
    int(0x01048200): Xtag(
        name="PLT_EDGE_LIST",
        pyname="edges",
    ),
    # Mesh/Edges/EdgeList/Line
    int(0x01048201): Xtag(
        name="PLT_LINE",
        pyname="line",
    ),
    # Mesh/Objects
    int(0x01050000): Xtag(name="PLT_OBJECTS_SECTION", pyname="objects"),
    # Mesh/Objects/Object
    int(0x01050001): Xtag(
        name="PLT_OBJECT_ID",
        pyname="id",
    ),
    int(0x01050002): Xtag(name="PLT_OBJECT_NAME", pyname="name", format="szname"),
    int(0x01050003): Xtag(
        name="PLT_OBJECT_TAG",
        pyname="tag",
    ),
    int(0x01050004): Xtag(name="PLT_OBJECT_POS", pyname="pos", format="float32"),
    int(0x01050005): Xtag(name="PLT_OBJECT_ROT", pyname="rot", format="float32"),
    int(0x01050006): Xtag(name="PLT_OBJECT_DATA", pyname="data", format="float32"),
    # Mesh/Objects/Object/Point
    int(0x01051000): Xtag(name="PLT_POINT_OBJECT", pyname="point"),
    int(0x01051001): Xtag(name="PLT_POINT_COORD", pyname="coord", format="float32"),
    # Mesh/Objects/Object/Line
    int(0x01052000): Xtag(name="PLT_LINE_OBJECT", pyname="line"),
    int(0x01052001): Xtag(name="PLT_LINE_COORDS", pyname="coords", format="float32"),
    # State/
    int(0x02000000): Xtag(name="PLT_STATE", pyname="state"),
    # State/Header
    int(0x02010000): Xtag(name="PLT_STATE_HEADER", pyname="header"),
    int(0x02010001): Xtag(
        name="PLT_STATE_HDR_ID",
        pyname="id",
    ),
    int(0x02010002): Xtag(name="PLT_STATE_HDR_TIME", pyname="time", format="float32"),
    int(0x02010003): Xtag(
        name="PLT_STATE_STATUS",
        pyname="status",
    ),
    # State/Data
    int(0x02020000): Xtag(name="PLT_STATE_DATA", pyname="state_data"),
    int(0x02020001): Xtag(name="PLT_STATE_VARIABLE", pyname="variable"),
    int(0x02020002): Xtag(
        name="PLT_STATE_VAR_ID",
        pyname="id",
    ),
    int(0x02020003): Xtag(name="PLT_STATE_VAR_DATA", pyname="data", format="float32"),
    int(0x02020100): Xtag(name="PLT_GLOBAL_DATA", pyname="data"),
    int(0x02020300): Xtag(name="PLT_NODE_DATA", pyname="data"),
    int(0x02020400): Xtag(name="PLT_ELEMENT_DATA", pyname="data"),
    int(0x02020500): Xtag(name="PLT_FACE_DATA", pyname="data"),
    int(0x02020600): Xtag(name="PLT_EDGE_DATA", pyname="data"),
    # State/MeshState
    int(0x02030000): Xtag(name="PLT_MESH_STATE", pyname="mesh_state"),
    # State/MeshState/ElementState
    int(0x02030001): Xtag(
        name="PLT_ELEMENT_STATE",
        pyname="element_state",
    ),
    # State/ObjectsState
    int(0x02040000): Xtag(name="PLT_OBJECTS_STATE", pyname="objects_state"),
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
        dtypes_to_little__ENDIAN(_DTYPES)
        if np.frombuffer(buffer, dtype=_DTYPES["int32"], count=1)[0] == int(FEBIO_TAG):
            log.info("File is FEBio, but in Big ENDIAN format -- will be byte-swapped to Little _ENDIAN")
        else:
            raise ValueError("Invalid FEBio file")
    else:
        log.info("File is FEBio, and in Little ENDIAN format")


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


def parse_root_header(buffer: bytes, f):
    i = 0
    while i < len(buffer) - 8:
        tag, offset = parse_prefix(buffer[i : i + 8])
        f["/"].attrs[TAG_LUT[tag].name] = np.frombuffer(buffer[i + 8 : i + 8 + offset], dtype=_DTYPES[TAG_LUT[tag].format])
        i += 8 + offset


def _parse_header(buffer: bytes) -> dict[str, Any]:
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


def _parse_node_section(buffer: bytes) -> dict[str, Any]:
    node_dict = {}
    i = 0
    while i < len(buffer) - 8:
        tag, offset = parse_prefix(buffer[i : i + 8])
        match TAG_LUT[tag].name:
            case "PLT_NODE_HEADER":
                node_dict = _parse_header(buffer[i + 8 : i + 8 + offset])
            case "PLT_NODE_COORDS":
                nodes = np.frombuffer(buffer[i + 8 : i + 8 + offset], dtype=_DTYPES["node"])
                node_dict["data"] = nodes
        i += 8 + offset
    return node_dict


def _parse_dom_elem_list(buffer: bytes) -> np.ndarray:
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
                domain_dict = _parse_header(child)
            case "PLT_DOM_ELEM_LIST":
                domain_dict["elements"] = _parse_dom_elem_list(child)
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
                elementset_dict["elements"] = np.frombuffer(child, dtype=_DTYPES[TAG_LUT[tag].format])
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
    mesh_dict = {"surfaces": {}, "domains": {}, "node_sets": {}}
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
                    mesh_dict["domains"][domain["id"][0]] = domain["name"]
                    dset_path = f"/meshes/{mesh_cnt}/domains/{domain['name']}"
                    f.create_dataset(dset_path, data=domain["elements"], dtype=_DTYPES["int32"])
                    for key, value in domain.items():
                        if not key == "elements":
                            f[dset_path].attrs[key] = value
                i += 8 + offset
            case "PLT_SURFACE_SECTION":
                surfaces = _parse_surface_section(child)
                for surface in surfaces:
                    mesh_dict["surfaces"][surface["id"][0]] = surface["name"]
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
                    mesh_dict["node_sets"][nodeset["id"][0]] = nodeset["name"]
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
    return mesh_dict


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
        state_dict[TAG_LUT[tag].pyname] = np.frombuffer(buffer[i + 8 : i + 8 + offset], dtype=_DTYPES[TAG_LUT[tag].format])
        i += 8 + offset
        tag, offset = parse_prefix(buffer[i : i + 8])
        child = buffer[i + 8 : i + 8 + offset]
        j = 0
        while j < offset:
            sid, offset2 = parse_prefix(child[j : j + 8])
            state_dict["data"][sid] = np.frombuffer(child[j + 8 : j + 8 + offset2], dtype=_DTYPES[TAG_LUT[tag].format])
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
                state_data_dict["element_data"] = _parse_data(buffer[i + 8 : i + 8 + offset])
            case "PLT_OBJECT_DATA":
                state_data_dict["object_data"] = _parse_data(buffer[i + 8 : i + 8 + offset])
            case "PLT_FACE_DATA":
                state_data_dict["surface_data"] = _parse_data(buffer[i + 8 : i + 8 + offset])
            case _:
                pass
        i += 8 + offset
    return state_data_dict


def parse_state(buffer: bytes, state_cnt: int, xdictionary: dict, mesh_dict: dict, f):
    var_lut = {"node_data": "PLT_DIC_NODAL", "surface_data": "PLT_DIC_SURFACE", "element_data": "PLT_DIC_DOMAIN"}
    set_lut: dict[str, str] = {"node_data": "node_sets", "surface_data": "surfaces", "element_data": "domains"}
    i = 0
    while i < len(buffer) - 8:
        tag, offset = parse_prefix(buffer[i : i + 8])
        child = buffer[i + 8 : i + 8 + offset]
        match TAG_LUT[tag].name:
            case "PLT_STATE_HEADER":
                _parse_header(child)
            case "PLT_MESH_STATE":
                _parse_mesh_state(child)
            case "PLT_OBJECTS_STATE":
                _parse_objects_state(child)
            case "PLT_STATE_DATA":
                data_dict = _parse_state_data(child)
                for key, data_items in data_dict.items():
                    for item in data_items:
                        for set_id, data in item["data"].items():
                            var_name = xdictionary[var_lut[key]][item["id"][0] - 1].name
                            if key == "node_data":
                                set_name = mesh_dict[set_lut[key]][set_id + 1]
                            else:
                                set_name = mesh_dict[set_lut[key]][set_id]
                            dset_path = f"states/{state_cnt}/{key}/{var_name}/{set_name}"
                            f.create_dataset(dset_path, data=data)
            case _:
                pass
        i += offset + 8


def parse_blocks(buffer: bytes, f: h5py.File):
    i = 0
    xdictionary = None
    mesh_dicts: list[dict] = []
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
                        parse_root_header(child[j + 8 : j + 8 + offset2], f)
                    elif TAG_LUT[tag].name == "PLT_DICTIONARY":
                        xdictionary = parse_dictionary(child[j + 8 : j + 8 + offset2])
                    j += offset2 + 8
            case "PLT_MESH":
                mesh_dicts.append(parse_mesh(child, mesh_cnt, f))
                mesh_cnt += 1
            case "PLT_STATE":
                assert xdictionary is not None, "Dictionary not found"
                parse_state(child, state_cnt, xdictionary, mesh_dicts[mesh_cnt - 1], f)
                state_cnt += 1
        i += 8 + offset


@dataclass
class Header:
    version: int
    compression: int
    software: int
    author: str | None = None
    units: str | None = None


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


def parse_xplt(filename: str):
    with open(filename, "rb") as fid:
        buffer = fid.read()
        check_file_is_febio(buffer)
        f = h5py.File("test.hdf5", "w")
        blocks = parse_blocks(buffer[4:], f)
        f.close()

    # TAG_LUT = {
    #     # Root/
    #     # Root/Header
    #     int(0x01000000): Xtag(name="ROOT", pyname="root", parse_fn=parse_root),
    #     int(0x1010000): Xtag(name="HEADER", pyname="header", parse_fn=parse_root_header),
    #     int(0x01010001): Xtag(
    #         name="HDR_VERSION",
    #         pyname="version",
    #         parse_fn=parse_uint32,
    #     ),
    #     int(0x01010004): Xtag(name="HDR_COMPRESSION", pyname="compression", parse_fn=parse_uint32),
    #     int(0x01010005): Xtag(name="HDR_AUTHOR", pyname="author", parse_fn=parse_char_array),
    #     int(0x01010006): Xtag(name="HDR_SOFTWARE", pyname="software", parse_fn=parse_uint32),
    #     int(0x01010007): Xtag(name="HDR_UNITS", pyname="units", parse_fn=parse_char_array),
    #     # Root/Dictionary
    #     int(0x01020000): Xtag(name="DICTIONARY", pyname="dictionary", parse_fn=parse_dictionary),
    #     int(0x01021000): Xtag(name="DIC_GLOBAL", pyname="dic_global", parse_fn=parse_dic_section),
    #     int(0x01023000): Xtag(name="DIC_NODAL", pyname="dic_nodal", parse_fn=parse_dic_section),
    #     int(0x01024000): Xtag(name="DIC_DOMAIN", pyname="dic_domain", parse_fn=parse_dic_section),
    #     int(0x01025000): Xtag(name="DIC_SURFACE", pyname="dic_surface", parse_fn=parse_dic_section),
    #     int(0x01026000): Xtag(name="DIC_EDGE", pyname="dic_edge", parse_fn=parse_dic_section),
    #     int(0x01020001): Xtag(name="DIC_ITEM", pyname="item", parse_fn=_parse_dic_item),
    #     int(0x01020002): Xtag(name="DIC_ITEM_TYPE", pyname="itype", parse_fn=parse_uint32),
    #     int(0x01020003): Xtag(name="DIC_ITEM_FMT", pyname="iformat", parse_fn=parse_uint32),
    #     int(0x01020004): Xtag(name="DIC_ITEM_NAME", pyname="name", parse_fn=parse_char_array),
    #     int(0x01020005): Xtag(name="DIC_ITEM_ARRAYSIZE", pyname="array_size", parse_fn=parse_uint32),
    #     int(0x01020006): Xtag(name="DIC_ITEM_ARRAYNAME", pyname="array_name", parse_fn=parse_char_array),
    #     int(0x01020007): Xtag(name="DIC_ITEM_UNITS", pyname="units", parse_fn=parse_char_array),
    #     # Mesh/
    #     int(0x01040000): Xtag(name="MESH", pyname="mesh", parse_fn=parse_mesh),
    #     # Mesh/Nodes
    #     int(0x01041000): Xtag(name="NODE_SECTION", pyname="nodes", parse_fn=parse_node_section),
    #     int(0x01041100): Xtag(name="NODE_HEADER", pyname="header", parse_fn=parse_header),
    #     int(0x01041101): Xtag(name="NODE_SIZE", pyname="nnodes", parse_fn=parse_uint32),
    #     int(0x01041102): Xtag(name="NODE_DIM", pyname="dimension", parse_fn=parse_uint32),
    #     int(0x01041103): Xtag(name="NODE_NAME", pyname="name", parse_fn=parse_char_array),
    #     int(0x01041200): Xtag(name="NODE_COORDS", pyname="coords", parse_fn=parse_node_coords),
    #     # Mesh/Domains
    #     int(0x01042000): Xtag(name="DOMAIN_SECTION", pyname="domains", parse_fn=parse_domain_section),
    #     # Mesh/Domains/Domain
    #     int(0x01042100): Xtag(name="DOMAIN", pyname="domain", parse_fn=parse_domain),
    #     int(0x01042101): Xtag(name="DOMAIN_HDR", pyname="header", parse_fn=parse_header),
    #     int(0x01042102): Xtag(name="DOM_ELEM_TYPE", pyname="etype", parse_fn=parse_uint32),
    #     int(0x01042103): Xtag(name="DOM_PART_ID", pyname="id", parse_fn=parse_uint32),
    #     int(0x01032104): Xtag(name="DOM_ELEMS", pyname="nelems", parse_fn=parse_uint32),
    #     int(0x01032105): Xtag(name="DOM_NAME", pyname="name", parse_fn=parse_char_array),
    #     int(0x01042200): Xtag(name="DOM_ELEM_LIST", pyname="elements", parse_fn=_parse_dom_elem_list),
    #     int(0x01042201): Xtag(name="ELEMENT", pyname="element", parse_fn=parse_uint32),
    #     # Mesh/Surfaces
    #     int(0x01043000): Xtag(name="SURFACE_SECTION", pyname="surfaces", parse_fn=parse_surface_section),
    #     # Mesh/Surfaces/Surface
    #     int(0x01043100): Xtag(name="SURFACE", pyname="surface", parse_fn=parse_surface),
    #     int(0x01043101): Xtag(name="SURFACE_HDR", pyname="header", parse_fn=parse_header),
    #     int(0x01043102): Xtag(name="SURFACE_ID", pyname="id", parse_fn=parse_uint32),
    #     int(0x01043103): Xtag(name="SURFACE_FACES", pyname="nfaces", parse_fn=parse_uint32),
    #     int(0x01043104): Xtag(name="SURFACE_NAME", pyname="name", parse_fn=parse_char_array),
    #     int(0x01043105): Xtag(name="SURFACE_MAX_FACET_NODES", pyname="max_nodes", parse_fn=parse_uint32),
    #     int(0x01043200): Xtag(name="FACE_LIST", pyname="faces", parse_fn=parse_face_list),
    #     int(0x01043201): Xtag(name="FACE", pyname="face", parse_fn=parse_uint32),
    #     int(0x01044000): Xtag(name="NODESET_SECTION", pyname="node_sets", parse_fn=parse_node_set_section),
    #     int(0x01044100): Xtag(name="NODESET", pyname="node_set", parse_fn=parse_node_set),
    #     int(0x01044101): Xtag(name="NODESET_HDR", pyname="header", parse_fn=parse_header),
    #     int(0x01044102): Xtag(name="NODESET_ID", pyname="id", parse_fn=parse_uint32),
    #     int(0x01044103): Xtag(name="NODESET_NAME", pyname="name", parse_fn=parse_char_array),
    #     int(0x01044104): Xtag(name="NODESET_SIZE", pyname="nnodes", parse_fn=parse_uint32),
    #     int(0x01044200): Xtag(name="NODESET_LIST", pyname="nodes", parse_fn=_parse_nodeset_list),
    #     int(0x01045000): Xtag(name="PARTS_SECTION", pyname="parts", parse_fn=_parse_parts_section),
    #     int(0x01045100): Xtag(name="PART", pyname="part", parse_fn=_parse_part),
    #     int(0x01045101): Xtag(name="PART_ID", pyname="id", parse_fn=parse_uint32),
    #     int(0x01045102): Xtag(name="PART_NAME", pyname="name", parse_fn=parse_char_array),
    #     # Mesh/ElementSets
    #     # element set section was added in 4.1
    #     int(0x01046000): Xtag(name="ELEMENTSET_SECTION", pyname="element_sets", parse_fn=_parse_elementset_section),
    #     # Mesh/ElementSets/ElementSet
    #     int(0x01046100): Xtag(name="ELEMENTSET", pyname="element_set", parse_fn=_parse_elementset),
    #     int(0x01046101): Xtag(name="ELEMENTSET_HDR", pyname="header", parse_fn=_parse_header),
    #     int(0x01046102): Xtag(name="ELEMENTSET_ID", pyname="id", parse_fn=parse_uint32),
    #     int(0x01046103): Xtag(name="ELEMENTSET_NAME", pyname="name", parse_fn=parse_char_array),
    #     int(0x01046104): Xtag(name="ELEMENTSET_SIZE", pyname="nelems", parse_fn=parse_uint32),
    #     int(0x01046200): Xtag(name="ELEMENTSET_LIST", pyname="elements", parse_fn=parse_uint32),
    #     # Mesh/FacetSets
    #     # facet set section was added in 4.1
    #     int(0x01047000): Xtag(name="FACETSET_SECTION", pyname="facet_sets", parse_fn=_parse_facetset_section),
    #     # Mesh/FacetSets/FacetSet
    #     int(0x01047100): Xtag(name="FACETSET", pyname="facet_set", parse_fn=_parse_facetset),
    #     int(0x01047101): Xtag(name="FACETSET_HDR", pyname="header", parse_fn=_parse_header),
    #     int(0x01047102): Xtag(name="FACETSET_ID", pyname="id", parse_fn=parse_uint32),
    #     int(0x01047103): Xtag(name="FACETSET_NAME", pyname="name", parse_fn=parse_char_array),
    #     int(0x01047104): Xtag(name="FACETSET_SIZE", pyname="nfacets", parse_fn=parse_uint32),
    #     int(0x01047105): Xtag(name="FACETSET_MAXNODES", pyname="max_nodes", parse_fn=parse_uint32),
    #     int(0x01047200): Xtag(name="FACETSET_LIST", pyname="facets", parse_fn=_parse_facetset_list),
    #     int(0x01047201): Xtag(name="FACET", pyname="facet", parse_fn=parse_uint32),
    #     # Mesh/Edges
    #     int(0x01048000): Xtag(name="EDGE_SECTION", pyname="edges", parse_fn=_parse_edge_section),
    #     # Mesh/Edges/Edge
    #     int(0x01048100): Xtag(name="EDGE", pyname="edge", parse_fn=_parse_edge),
    #     int(0x01048101): Xtag(name="EDGE_HDR", pyname="header", parse_fn=_parse_header),
    #     int(0x01048102): Xtag(name="EDGE_ID", pyname="id", parse_fn=parse_uint32),
    #     int(0x01048103): Xtag(name="EDGE_LINES", pyname="lines", parse_fn=parse_uint32),
    #     int(0x01048104): Xtag(name="EDGE_NAME", pyname="name", parse_fn=parse_char_array),
    #     int(0x01048105): Xtag(name="EDGE_MAX_NODES", pyname="max_nodes", parse_fn=parse_uint32),
    #     # Mesh/Edges/EdgeList
    #     int(0x01048200): Xtag(name="EDGE_LIST", pyname="edges", parse_fn=_parse_edge_list),
    #     # Mesh/Edges/EdgeList/Line
    #     int(0x01048201): Xtag(name="LINE", pyname="line", parse_fn=parse_uint32),
    #     # Mesh/Objects
    #     int(0x01050000): Xtag(name="OBJECTS_SECTION", pyname="objects", parse_fn=_parse_objects_section),
    #     # Mesh/Objects/Object
    #     int(0x01050001): Xtag(name="OBJECT_ID", pyname="id", parse_fn=parse_uint32),
    #     int(0x01050002): Xtag(name="OBJECT_NAME", pyname="name", parse_fn=parse_char_array),
    #     int(0x01050003): Xtag(name="OBJECT_TAG", pyname="tag", parse_fn=parse_uint32),
    #     int(0x01050004): Xtag(name="OBJECT_POS", pyname="pos", parse_fn=parse_float32),
    #     int(0x01050005): Xtag(name="OBJECT_ROT", pyname="rot", parse_fn=parse_float32),
    #     int(0x01050006): Xtag(name="OBJECT_DATA", pyname="data", parse_fn=parse_float32),
    #     # Mesh/Objects/Object/Point
    #     int(0x01051000): Xtag(name="POINT_OBJECT", pyname="point", parse_fn=_parse_point_object),
    #     int(0x01051001): Xtag(name="POINT_COORD", pyname="coord", parse_fn=parse_float32),
    #     # Mesh/Objects/Object/Line
    #     int(0x01052000): Xtag(name="LINE_OBJECT", pyname="line", parse_fn=_parse_line_object),
    #     int(0x01052001): Xtag(name="LINE_COORDS", pyname="coords", parse_fn=parse_float32),
    #     # State/
    #     int(0x02000000): Xtag(name="STATE", pyname="state", parse_fn=_parse_state),
    #     # State/Header
    #     int(0x02010000): Xtag(name="STATE_HEADER", pyname="header", parse_fn=_parse_header),
    #     int(0x02010001): Xtag(name="STATE_HDR_ID", pyname="id", parse_fn=parse_uint32),
    #     int(0x02010002): Xtag(name="STATE_HDR_TIME", pyname="time", parse_fn=parse_float32),
    #     int(0x02010003): Xtag(name="STATE_STATUS", pyname="status", parse_fn=parse_uint32),
    #     # State/Data
    #     int(0x02020000): Xtag(name="STATE_DATA", pyname="state_data", parse_fn=_parse_state_data),
    #     int(0x02020001): Xtag(name="STATE_VARIABLE", pyname="variable", parse_fn=_parse_state_variable),
    #     int(0x02020002): Xtag(name="STATE_VAR_ID", pyname="id", parse_fn=parse_uint32),
    #     int(0x02020003): Xtag(name="STATE_VAR_DATA", pyname="data", parse_fn=_parse_state_var_data),
    #     int(0x02020100): Xtag(name="GLOBAL_DATA", pyname="data", parse_fn=_parse_state_section),
    #     int(0x02020300): Xtag(name="NODE_DATA", pyname="data", parse_fn=_parse_state_section),
    #     int(0x02020400): Xtag(name="ELEMENT_DATA", pyname="data", parse_fn=_parse_state_section),
    #     int(0x02020500): Xtag(name="FACE_DATA", pyname="data", parse_fn=_parse_state_section),
    #     int(0x02020600): Xtag(name="EDGE_DATA", pyname="data", parse_fn=_parse_state_section),
    #     # State/MeshState
    #     int(0x02030000): Xtag(name="MESH_STATE", pyname="mesh_state", parse_fn=_parse_mesh_state),
    #     # State/MeshState/ElementState
    #     int(0x02030001): Xtag(name="ELEMENT_STATE", pyname="element_state", parse_fn=parse_uint32),
    #     # State/ObjectsState
    #     int(0x02040000): Xtag(name="OBJECTS_STATE", pyname="objects_state", parse_fn=parse_uint32),
    # }
