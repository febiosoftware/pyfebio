import math
import subprocess
from pathlib import Path

from pydantic_xml import BaseXmlModel, attr, element

from . import (
    boundary,
    constraints,
    contact,
    control,
    discrete,
    globals,
    include,
    initial,
    loaddata,
    loads,
    material,
    mesh,
    meshadaptor,
    meshdata,
    meshdomains,
    module,
    output,
    rigid,
    step,
)

SectionTypes = (
    module.Module
    | globals.Globals
    | control.Control
    | material.Material
    | material.RigidBody
    | meshdomains.MeshDomains
    | mesh.Mesh
    | meshdata.MeshData
    | discrete.Discrete
    | loaddata.LoadData
    | loads.Loads
    | rigid.Rigid
    | initial.Initial
    | boundary.Boundary
    | contact.Contact
    | constraints.Constraints
    | step.Step
    | output.Output
    | include.Include
)


class FEBioRoot(BaseXmlModel, tag="febio_spec", validate_assignment=True):
    version: str = attr(default="4.0")
    sections: list[SectionTypes] = element(default=[])

    def add_section(self, section: SectionTypes):
        assert isinstance(section, SectionTypes), "section must be a SectionTypes"
        self.sections.append(section)

    def save(self, filename: str | Path):
        xml = self.to_xml(
            pretty_print=True,
            encoding="ISO-8859-1",
            xml_declaration=True,
            skip_empty=True,
        )
        assert isinstance(xml, bytes)
        with open(filename, "wb") as fid:
            _ = fid.write(xml)


class Model(BaseXmlModel, tag="febio_spec", validate_assignment=True, extra="forbid"):
    version: str = attr(default="4.0")
    module_: module.Module | None = element(default=module.Module(), tag="Module")
    globals_: globals.Globals = element(default=globals.Globals(), tag="Globals")
    control_: control.Control | None = element(default=control.Control(), tag="Control")
    material_: material.Material = element(default=material.Material(), tag="Material")
    mesh_: mesh.Mesh = element(default=mesh.Mesh(), tag="Mesh")
    meshdomains_: meshdomains.MeshDomains = element(default=meshdomains.MeshDomains(), tag="MeshDomains")
    meshdata_: meshdata.MeshData = element(default=meshdata.MeshData(), tag="MeshData")
    meshadaptor_: meshadaptor.MeshAdaptor = element(default=meshadaptor.MeshAdaptor())
    discrete_: discrete.Discrete = element(default=discrete.Discrete(), tag="Discrete")
    loaddata_: loaddata.LoadData = element(default=loaddata.LoadData(), tag="LoadData")
    loads_: loads.Loads = element(default=loads.Loads(), tag="Loads")
    rigid_: rigid.Rigid = element(default=rigid.Rigid(), tag="Rigid")
    initial_: initial.Initial = element(default=initial.Initial(), tag="Initial")
    boundary_: boundary.Boundary = element(default=boundary.Boundary(), tag="Boundary")
    contact_: contact.Contact = element(default=contact.Contact(), tag="Contact")
    constraints_: constraints.Constraints = element(default=constraints.Constraints(), tag="Constraints")
    step_: step.Step = element(default=step.Step(), tag="Step")
    output_: output.Output = element(default=output.Output(), tag="Output")

    def save(self, filename: str | Path):
        xml = self.to_xml(
            pretty_print=True,
            encoding="ISO-8859-1",
            xml_declaration=True,
            skip_empty=True,
        )
        assert isinstance(xml, bytes)
        with open(filename, "wb") as fid:
            _ = fid.write(xml)

    def add_simple_rigid_body(self, origin: tuple[float, float, float], name: str):
        element_id = self.mesh_.elements[-1].all_elements[-1].id + 1
        node_id_start = self.mesh_.nodes[-1].all_nodes[-1].id + 1
        connectivity = [node_id for node_id in range(node_id_start, node_id_start + 4)]
        sqrt3over2 = math.sqrt(3.0) / 2.0
        ideal_tet = [
            [-1.0, -sqrt3over2, -sqrt3over2],
            [1.0, -sqrt3over2, -sqrt3over2],
            [0.0, sqrt3over2, -sqrt3over2],
            [0.0, 0.0, sqrt3over2],
        ]
        new_tet = [[tet[i] + origin[i] for i in range(3)] for tet in ideal_tet]
        nodes = [mesh.Node(id=node_id_start + i, text=",".join(map(str, new_tet[i]))) for i in range(4)]
        node_domain = mesh.Nodes(name=name, all_nodes=nodes)
        element = mesh.Tet4Element(id=element_id, text=",".join(map(str, connectivity)))
        element_domain = mesh.Elements(name=name, all_elements=[element], type="tet4")
        self.mesh_.add_node_domain(node_domain)
        self.mesh_.add_element_domain(element_domain)

        material_id = len(self.material_.all_materials) + 1

        mat = material.RigidBody(name=name, id=material_id, center_of_mass=",".join(map(str, origin)))
        self.material_.add_material(mat)
        self.meshdomains_.add_solid_domain(meshdomains.SolidDomain(name=name, mat=name))


class BiphasicModel(Model):
    module_: module.Module | None = element(default=module.Module(type="biphasic"))
    control_: control.Control | None = element(
        default=control.Control(
            analysis="TRANSIENT",
            solver=control.BiphasicSolver(),
            time_steps=100,
            step_size=0.1,
            time_stepper=control.TimeStepper(dtmax=control.TimeStepValue(text=0.1)),
        )
    )


class MultiphasicModel(Model):
    module_: module.Module | None = element(default=module.Module(type="multiphasic"))
    control_: control.Control | None = element(
        default=control.Control(
            analysis="TRANSIENT",
            solver=control.MultiphasicSolver(),
            time_steps=100,
            step_size=0.1,
            time_stepper=control.TimeStepper(dtmax=control.TimeStepValue(text=0.1)),
        )
    )


def run_model(filepath: str | Path, silent: bool = False) -> int:
    if silent:
        return subprocess.run(f"febio4 -i {filepath} -silent", shell=True, check=False).returncode
    else:
        return subprocess.run(f"febio4 -i {filepath}", shell=True, check=False).returncode
