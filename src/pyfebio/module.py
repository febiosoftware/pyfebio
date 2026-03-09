from typing import Literal

from pydantic_xml import BaseXmlModel, attr


class Module(BaseXmlModel, tag="Module", validate_assignment=True):
    """
    FEBio module -- currently, only supporting "solid" and "biphasic".

    Unsupported modules: "solute", "heat", "fluid", "fluid-FSI"

    """

    type: Literal["solid", "biphasic", "multiphasic"] = attr(default="solid")
