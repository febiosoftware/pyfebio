from typing import Annotated

from pydantic import StringConstraints

StringFloatVec = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        pattern=r"^([+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?,)+([+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?)$",
    ),
]


StringFloatVec2 = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        pattern=r"^" + ",".join([r"[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?"] * 2) + r"$",
    ),
]

StringFloatVec3 = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        pattern=r"^" + ",".join([r"[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?"] * 3) + r"$",
    ),
]


StringFloatVec9 = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        pattern=r"^" + ",".join([r"[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?"] * 9) + r"$",
    ),
]

StringUIntVec = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        pattern=r"^(?:\d+)(?:,(?:\d+))*$",
    ),
]

StringUIntVec2 = Annotated[
    str,
    StringConstraints(strip_whitespace=True, pattern=r"^" + ",".join([r"\d+"] * 2) + r"$"),
]

StringUIntVec3 = Annotated[
    str,
    StringConstraints(strip_whitespace=True, pattern=r"^" + ",".join([r"\d+"] * 3) + r"$"),
]

StringUIntVec4 = Annotated[
    str,
    StringConstraints(strip_whitespace=True, pattern=r"^" + ",".join([r"\d+"] * 4) + r"$"),
]

StringUIntVec5 = Annotated[
    str,
    StringConstraints(strip_whitespace=True, pattern=r"^" + ",".join([r"\d+"] * 5) + r"$"),
]

StringUIntVec6 = Annotated[
    str,
    StringConstraints(strip_whitespace=True, pattern=r"^" + ",".join([r"\d+"] * 6) + r"$"),
]

StringUIntVec8 = Annotated[
    str,
    StringConstraints(strip_whitespace=True, pattern=r"^" + ",".join([r"\d+"] * 8) + r"$"),
]

StringUIntVec9 = Annotated[
    str,
    StringConstraints(strip_whitespace=True, pattern=r"^" + ",".join([r"\d+"] * 9) + r"$"),
]

StringUIntVec10 = Annotated[
    str,
    StringConstraints(strip_whitespace=True, pattern=r"^" + ",".join([r"\d+"] * 10) + r"$"),
]

StringUIntVec15 = Annotated[
    str,
    StringConstraints(strip_whitespace=True, pattern=r"^" + ",".join([r"\d+"] * 15) + r"$"),
]

StringUIntVec20 = Annotated[
    str,
    StringConstraints(strip_whitespace=True, pattern=r"^" + ",".join([r"\d+"] * 20) + r"$"),
]

StringUIntVec27 = Annotated[
    str,
    StringConstraints(strip_whitespace=True, pattern=r"^" + ",".join([r"\d+"] * 27) + r"$"),
]
