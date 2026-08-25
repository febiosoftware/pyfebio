import argparse
import json
from pathlib import Path
from typing import Literal

import meshio
from pydantic import BaseModel, Field

import pyfebio as feb


class LigamentModel(BaseModel, frozen=True):
    proximal: list[tuple[float, float, float]]
    distal: list[tuple[float, float, float]]
    youngs_modulus: float = Field(gt=0.0)
    area: float = Field(gt=0.0)
    lambda0: float = Field(gt=0.0)
    prestretch: float = Field(gt=0.0)


class LigamentConfig(BaseModel, frozen=True):
    ligaments: dict[str, LigamentModel]


class ModelConfig(BaseModel, frozen=True):
    # Directory containing mesh files
    mesh_directory: str | Path = "../../assets/openknee"

    # Mesh resolution flag. Max edge lengths as follows:
    #   COARSE: 3.0mm
    #   MEDIUM: 2.0mm
    #   FINE: 1.0mm
    mesh_resolution: Literal["COARSE", "MEDIUM", "FINE"] = "MEDIUM"

    # Femur and Tibia origins. Defaults from OpenKnee model 003
    femur_origin: tuple[float, float, float] = (-1.036, -6.717, 0.171)
    tibia_origin: tuple[float, float, float] = (-4.4315, -7.2204999999999995, -24.9345)

    # Grood and Suntay axes e1, e2, e3. From OpenKnee model 003, but e1,e2 corrected
    # for a left knee
    e1: tuple[float, float, float] = (-0.9889108468842679, 0.1485103932882822, 0.0)
    e2: tuple[float, float, float] = (-0.1485103932882822, -0.9889108468842679, 0.0)
    e3: tuple[float, float, float] = (0.0, 0.0, 1.0)

    # Cartilage thickness in mm
    cartilage_thickness: float = Field(default=1.5, gt=0.0)
    # Young's modulus of the cartilage material in MPa
    youngs_modulus: float = Field(default=10.0, gt=0.0)
    # Poisson's ratio of the cartilage material
    # if poissons_ratio >= 4.5 an uncoupled Mooney-Rivlin model is used
    # otherwise a compressible Neo-Hookean model is used
    poissons_ratio: float = Field(default=0.4, ge=0.0)

    # Ligament configuration file
    ligament_config: str = "ligaments.json"

    superior_load: float = -500.0
    flexion_angle: float = 1.57 / 2.0

    # Contact gap tolerance in mm enforced by the Augmented Lagrangian method
    contact_gap: float = 0.1

    # Angle tolerance in radians for connector constraints
    connector_angle_tolerance: float = 0.0005
    # Gap tolerance in mm for connector constraints
    connector_gap_tolerance: float = 0.05

    output_vars: list[feb.output.PlotDataVariables] = [
        "displacement",
        "stress",
        "Lagrange strain",
        "shell strain",
        "contact pressure",
        "contact gap",
        "shell relative volume",
        "discrete element force",
        "discrete element stretch",
    ]


model_config = ModelConfig()
with open(model_config.ligament_config) as f:
    ligament_config = ModelConfig(**json.load(f))


def import_and_assemble_mesh(mesh_directory: str | Path, mesh_resolution: Literal["COARSE", "MEDIUM", "FINE"]) -> feb.mesh.Mesh:
    """
    Imports the appropriate mesh files based on provided mesh_resolution and mesh_directory.
    Assembles the meshes into a single pyfebio Mesh object.
    """
    suffix = {"COARSE": "_3p0.msh", "MEDIUM": "_2p0.msh", "FINE": ".msh"}
    element_offset = 0
    node_offset = 0
    assembled_mesh = feb.mesh.Mesh()
    for name in ("tbc-l", "tbc-m", "fmc", "femur"):
        if name != "femur":
            meshfile = Path(mesh_directory).joinpath(f"{name}{suffix[mesh_resolution]}")
        else:
            meshfile = Path(mesh_directory).joinpath(f"{name}.msh")
        meshobj = meshio.gmsh.read(meshfile)

        febmesh = feb.mesh.translate_meshio(
            meshobj, nodeoffset=node_offset, elementoffset=element_offset, shell_sets=["cartilage"], nodes_name=name
        )

        element_offset = febmesh.elements[-1].all_elements[-1].id
        node_offset = febmesh.nodes[-1].all_nodes[-1].id
        for node in febmesh.nodes:
            assembled_mesh.add_node_domain(node)

        for i, element in enumerate(febmesh.elements):
            if i > 0:
                element.name = f"{name}_{i + 2}"
            else:
                element.name = name
            assembled_mesh.add_element_domain(element)

    assembled_mesh.add_part_list(feb.mesh.PartList(name="fmc_list", text="fmc"))
    assembled_mesh.add_part_list(feb.mesh.PartList(name="femur_list", text="femur"))
    assembled_mesh.add_part_list(feb.mesh.PartList(name="tbc", text="tbc-l,tbc-m"))
    return assembled_mesh


def define_ligaments(model: feb.model.Model, ligament_model: LigamentConfig) -> None:
    """
    Defines the ligaments for the model based on the provided LigamentConfig pydantic BaseModel.
    """
    node_offset = model.mesh_.nodes[-1].all_nodes[-1].id + 1
    element_offset = model.mesh_.elements[-1].all_elements[-1].id + 1

    # Iterate over the ligaments dict keys and values
    # Each key serves as the element, domain, and material name
    # The values are LigamentModel instances. Consult the LigamentModel class definition for details.
    for discrete_id, (name, ligament) in enumerate(ligament_model.ligaments.items()):
        # Instantiate Nodes objects for the proximal and distal nodes
        proximal_nodes = feb.mesh.Nodes(name=f"{name}_proximal")
        distal_nodes = feb.mesh.Nodes(name=f"{name}_distal")
        # Instantiate DiscreteSet object for the spring elements representing the ligament
        discrete_set = feb.mesh.DiscreteSet(name=name)
        n_fibers = len(ligament.proximal)
        for prox_node, dist_node in zip(ligament.proximal, ligament.distal):
            proximal_nodes.add_node(feb.mesh.Node(id=node_offset, text=f"{prox_node[0]},{prox_node[1]},{prox_node[2]}"))
            distal_nodes.add_node(feb.mesh.Node(id=node_offset + n_fibers, text=f"{dist_node[0]},{dist_node[1]},{dist_node[2]}"))
            discrete_set.add_element(new_element=feb.mesh.DiscreteElement(text=f"{node_offset},{node_offset + n_fibers}"))
            # offset the element and node counters
            element_offset += 1
            node_offset += 1
        # need to offset nodes by 2 after the loop is completed
        node_offset += 2

        # Add the node and discrete sets to the model mesh_
        model.mesh_.add_node_domain(proximal_nodes)
        model.mesh_.add_node_domain(distal_nodes)
        model.mesh_.add_discrete_set(discrete_set)

        # Define a Blankevoort spring model using configuration parameters and
        # the NonLinearSpring discrete material referencing a math expression
        prestrain = ligament.prestretch - 1.0
        e0 = ligament.lambda0 - 1.0

        toe_region = f"H(x + {prestrain:.5f}) * ({0.5 / e0:.5f} * (x + {prestrain:.5f}) ^ 2) * (1.0 - H(x + {prestrain - e0:.5f}))"
        linear_region = f"H(x + {prestrain - e0:.5f}) * (x + {prestrain - e0 / 2.0:.5f})"
        dmat = feb.discrete.NonlinearSpring(
            id=discrete_id + 1,
            name=name,
            scale=ligament.youngs_modulus * ligament.area,
            measure="strain",
            force=feb.discrete.NonlinearSpringForce(math=f"{toe_region} + {linear_region}"),
        )

        # Add the material and element to the model discrete_ section
        model.discrete_.add_discrete_material(dmat)
        model.discrete_.add_discrete_element(feb.discrete.DiscreteEntry(dmat=discrete_id + 1, discrete_set=name))


def main(model_config: ModelConfig, quiet: bool = False) -> None:
    # Construct the ligament configuration object from JSON file
    with open(model_config.ligament_config, "r") as f:
        ligament_config = LigamentConfig(**json.load(f))

    assembled_mesh = import_and_assemble_mesh(model_config.mesh_directory, model_config.mesh_resolution)

    model = feb.model.Model(
        mesh_=assembled_mesh,
        control_=None,
    )

    # Shear modulus and bulk modulus from E and v
    G: float = model_config.youngs_modulus / (2 * (1 + model_config.poissons_ratio))
    K: float = model_config.youngs_modulus / (3 - 6 * model_config.poissons_ratio)

    for i, element in enumerate(model.mesh_.elements[0:3]):
        # Use an Uncoupled Mooney-Rivlin material if nearly incompressible
        # otherwise use a Neo-Hookean material
        if model_config.poissons_ratio >= 0.45:
            mat = feb.material.MooneyRivlinUC(
                name=element.name,
                id=i + 1,
                c1=feb.material.MaterialParameter(text=G / 2.0),
                c2=feb.material.MaterialParameter(text=0.0),
                k=feb.material.MaterialParameter(text=K),
            )
        else:
            mat = feb.material.NeoHookean(
                name=element.name,
                id=i + 1,
                E=feb.material.MaterialParameter(text=model_config.youngs_modulus),
                v=feb.material.MaterialParameter(text=model_config.poissons_ratio),
            )
        model.material_.add_material(mat)
        model.meshdomains_.add_shell_domain(
            feb.meshdomains.ShellDomain(name=element.name, mat=element.name, shell_thickness=model_config.cartilage_thickness)
        )

    # Make the femur Elements a rigid body
    mat = feb.material.RigidBody(
        name="femur",
        id=4,
        center_of_mass=f"{model_config.femur_origin[0]},{model_config.femur_origin[1]},{model_config.femur_origin[2]}",
        E=feb.material.MaterialParameter(text=model_config.youngs_modulus),
        v=feb.material.MaterialParameter(text=model_config.poissons_ratio),
    )
    model.material_.add_material(mat)
    model.meshdomains_.add_shell_domain(
        feb.meshdomains.ShellDomain(name="femur", mat="femur", shell_thickness=model_config.cartilage_thickness)
    )

    # Ligaments
    # --------------------------------------------------------------
    define_ligaments(model, ligament_config)

    for ligament in ligament_config.ligaments:
        model.boundary_.add_bc(feb.boundary.BCRigid(node_set=f"{ligament}_proximal", rb="femur"))
        model.boundary_.add_bc(feb.boundary.BCZeroDisplacement(node_set=f"{ligament}_distal", x_dof=1, y_dof=1, z_dof=1))
    # --------------------------------------------------------------

    # Create simple rigid bodies for the tibia, tibiaGhose, and femurGhost parts
    # --------------------------------------------------------------
    floating_origin = [(a + b) / 2.0 for a, b in zip(model_config.femur_origin, model_config.tibia_origin)]

    model.add_simple_rigid_body(origin=(floating_origin[0], floating_origin[1], floating_origin[2]), name="femurGhost")
    model.add_simple_rigid_body(origin=(floating_origin[0], floating_origin[1], floating_origin[2]), name="tibiaGhost")
    model.add_simple_rigid_body(
        origin=(model_config.tibia_origin[0], model_config.tibia_origin[1], model_config.tibia_origin[2]), name="tibia"
    )
    # --------------------------------------------------------------

    # Global (all steps) Boundary conditions and Contact interactions
    # --------------------------------------------------------------
    model.boundary_.add_bc(feb.boundary.BCRigid(node_set="@part_list:fmc_list", rb="femur"))
    model.boundary_.add_bc(feb.boundary.BCZeroShellDisplacement(node_set="@part_list:tbc", sx_dof=1, sy_dof=1, sz_dof=1))
    model.rigid_.add_rigid_bc(feb.rigid.RigidFixed(rb="tibia", Rx_dof=1, Ry_dof=1, Rz_dof=1, Ru_dof=1, Rw_dof=1, Rv_dof=1))

    model.mesh_.add_surface_pair(feb.mesh.SurfacePair(name="fmc_tbc", primary="@part_list:tbc", secondary="@part_list:fmc_list"))
    model.contact_.add_contact(
        feb.contact.SlidingElastic(
            surface_pair="fmc_tbc",
            penalty=10.0,
            laugon="AUGLAG",
            gaptol=model_config.contact_gap,
            two_pass=1,
            search_radius=2.0,
            tolerance=0,
            symmetric_stiffness=0,
        )
    )
    # --------------------------------------------------------------

    # Define the first step (prestrain)
    # --------------------------------------------------------------
    model.step_.add_step(
        feb.step.StepEntry(
            id=1,
            control=feb.control.Control(
                solver=feb.control.SolidSolver(qn_method=feb.control.BroydenMethod(), lsiter=10),
                time_steps=10,
                step_size=0.1,
                time_stepper=feb.control.TimeStepper(dtmax=feb.control.TimeStepValue(lc=1), max_retries=5),
                plot_level="PLOT_MUST_POINTS",
            ),
            name="prestrain",
            rigid=feb.rigid.Rigid(),
        )
    )

    # Fix the femur in rotation about x-axis
    model.step_.all_steps[0].rigid.add_rigid_bc(
        feb.rigid.RigidFixed(rb="femur", Rx_dof=0, Ry_dof=0, Rz_dof=0, Ru_dof=1, Rw_dof=0, Rv_dof=0)
    )
    # Apply a compressive load in the z-direction
    model.step_.all_steps[0].rigid.add_rigid_load(
        feb.rigid.RigidForceLoad(rb="femur", dof="Rz", value=feb.rigid.Value(lc=2, text=model_config.superior_load))
    )
    # --------------------------------------------------------------

    # Define the second step (load)
    # --------------------------------------------------------------
    model.step_.add_step(
        feb.step.StepEntry(
            id=2,
            name="load",
            control=feb.control.Control(
                solver=feb.control.SolidSolver(qn_method=feb.control.BroydenMethod(), lsiter=10),
                time_steps=100,
                step_size=0.01,
                time_stepper=feb.control.TimeStepper(dtmax=feb.control.TimeStepValue(lc=1), max_retries=5),
                plot_level="PLOT_MUST_POINTS",
            ),
            rigid=feb.rigid.Rigid(),
        )
    )
    # Define the internal-external rotation, inferior-superior translation cylindrical joint
    # This is Grood-Suntay E3
    model.step_.all_steps[1].rigid.add_rigid_connector(
        feb.rigid.RigidCylindricalJoint(
            name="IE_rot_IS_translation",
            body_a="tibia",
            body_b="tibiaGhost",
            joint_origin=f"{model_config.tibia_origin[0]},{model_config.tibia_origin[1]},{model_config.tibia_origin[2]}",
            joint_axis=f"{model_config.e3[0]},{model_config.e3[1]},{model_config.e3[2]}",
            auto_penalty=1,
            laugon="AUGLAG",
            gaptol=model_config.connector_gap_tolerance,
            angtol=model_config.connector_angle_tolerance,
            tolerance=0,
        )
    )
    # Define the varus-valgus rotation, anterior-posterior translation cylindrical joint
    # This is Grood-Suntay E2
    model.step_.all_steps[1].rigid.add_rigid_connector(
        feb.rigid.RigidCylindricalJoint(
            name="VV_rot_AP_translation",
            body_a="tibiaGhost",
            body_b="femurGhost",
            joint_origin=f"{floating_origin[0]},{floating_origin[1]},{floating_origin[2]}",
            joint_axis=f"{model_config.e2[0]},{model_config.e2[1]},{model_config.e2[2]}",
            auto_penalty=1,
            gaptol=model_config.connector_gap_tolerance,
            angtol=model_config.connector_angle_tolerance,
            laugon="AUGLAG",
            tolerance=0,
        )
    )
    # Define the flexion-extension, medial-lateral translation cylindrical joint
    # This is Grood-Suntay E1
    model.step_.all_steps[1].rigid.add_rigid_connector(
        feb.rigid.RigidCylindricalJoint(
            name="Flexion_rot_ML_translation",
            body_a="femurGhost",
            body_b="femur",
            joint_origin=f"{model_config.femur_origin[0]},{model_config.femur_origin[1]},{model_config.femur_origin[2]}",
            joint_axis=f"{model_config.e1[0]},{model_config.e1[1]},{model_config.e1[2]}",
            auto_penalty=1,
            laugon="AUGLAG",
            gaptol=model_config.connector_gap_tolerance,
            angtol=model_config.connector_angle_tolerance,
            tolerance=0,
            prescribed_rotation=1,
            rotation=feb.rigid.Value(lc=3, text=model_config.flexion_angle),
        )
    )
    # Apply the same compressive load to the femur as in prestrain step
    model.step_.all_steps[1].rigid.add_rigid_load(
        feb.rigid.RigidForceLoad(rb="femur", dof="Rz", value=feb.rigid.Value(lc=2, text=-model_config.superior_load))
    )
    # --------------------------------------------------------------

    # Define the Load Curves
    # --------------------------------------------------------------

    # must points forcing output at the 1.0 (end of prestrain step)
    # and at every 0.1 seconds during the load step
    must_points = ["1.0,1.0"]
    must_points += [f"{1.0 + (i + 1) * 0.1},0.1" for i in range(10)]
    model.loaddata_.add_load_curve(
        feb.loaddata.LoadCurve(
            id=1,
            interpolate="STEP",
            points=feb.loaddata.CurvePoints(points=must_points),
        )
    )

    # Load curve scaling the compressive femoral force
    model.loaddata_.add_load_curve(
        feb.loaddata.LoadCurve(
            id=2,
            interpolate="LINEAR",
            points=feb.loaddata.CurvePoints(points=["0.0,0.0", "1.0,1.0"]),
        )
    )

    # Load curve defining the femoral rotation via rigid connnector Flexion_rot_ML_translation
    model.loaddata_.add_load_curve(
        feb.loaddata.LoadCurve(id=3, interpolate="LINEAR", points=feb.loaddata.CurvePoints(points=["1.0,0.0", "2.0,1.0"]))
    )
    # --------------------------------------------------------------

    # Request plot variables listed in ModelConfig
    model.output_.add_plotfile(feb.output.OutputPlotfile(all_vars=[feb.output.Var(type=v) for v in model_config.output_vars]))

    # Save and Run the Model
    output_name = f"openknee_elastic_{model_config.mesh_resolution.lower()}.feb"

    model.save(output_name)
    success = feb.model.run_model(filepath=output_name, silent=quiet)

    if success == 0:
        print(f"Model: {output_name} run successful.")
    else:
        print(f"Model: {output_name} run failed.")


if __name__ == "__main__":
    # Configure a parser to allow for CLI execution and control
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, help="path to configuration file")
    parser.add_argument("--quiet", action="store_true", help="Disable most most screen messages.")
    parser.add_argument("--mesh_resolution", choices=["COARSE", "MEDIUM", "FINE"], help="Override mesh resolution")
    parser.add_argument("--ligament_config", type=str, help="Override path to ligament configuration file")
    parser.add_argument("--youngs_modulus", type=float, help="Override Young's modulus")
    parser.add_argument("--poissons_ratio", type=float, help="Override Poisson's ratio")
    parser.add_argument("--superior_load", type=float, help="Override force to apply in z-direction")
    parser.add_argument("--flexion_angle", type=float, help="Override flexion angle to apply in second step (in radians)")

    args = parser.parse_args()

    # If no config file is provided, use the default ModelConfig
    # Otherwise, load the config from the provided file using json package
    if args.config is None:
        model_config = ModelConfig()
    else:
        with open(args.config, "r") as f:
            model_config = ModelConfig(**json.load(f))

    # Update the model_config with any CLI arguments
    update_dict = {}
    for arg, value in vars(args).items():
        if value is not None and arg not in ["config", "quiet"]:
            update_dict[arg] = value
    model_config = model_config.model_copy(update=update_dict)

    # Run the main function
    main(model_config=model_config, quiet=args.quiet)
