# Copyright 2023-2024 Luminary Cloud, Inc. All Rights Reserved.
import pytest

from typing import Any

import luminarycloud as lc
from luminarycloud.params import simulation as param
from luminarycloud.params import enum
from luminarycloud.enum import TableType
import luminarycloud._proto.client.simulation_pb2 as clientpb
import luminarycloud._proto.output.output_pb2 as outputpb
import luminarycloud._proto.quantity.quantity_pb2 as quantitypb


def _to_and_from_proto(obj: Any) -> Any:
    proto = obj._to_proto()
    new_obj = type(obj)()
    assert proto != new_obj._to_proto()
    new_obj._from_proto(proto)
    return new_obj


def test_init_params() -> None:
    lc.SimulationParam()

    # Boundary Conditions
    farfield = param.physics.fluid.boundary_conditions.Farfield(
        name="farfield",
        direction_specification=enum.FarFieldFlowDirectionSpecification.FARFIELD_DIRECTION,
        direction=lc.types.Vector3(x=1, y=0, z=0),
    )
    assert farfield == _to_and_from_proto(farfield)
    outlet = param.physics.fluid.boundary_conditions.Outlet(name="outlet")
    assert outlet == _to_and_from_proto(outlet)
    wall = param.physics.fluid.boundary_conditions.Wall(name="wall")
    wall.momentum = param.physics.fluid.boundary_conditions.wall.momentum.Slip()
    assert wall == _to_and_from_proto(wall)
    total_pressure_inlet = param.physics.fluid.boundary_conditions.inlet.TotalPressureInlet(
        name="pressure_inlet"
    )
    assert total_pressure_inlet == _to_and_from_proto(total_pressure_inlet)
    velocity_components_inlet = (
        param.physics.fluid.boundary_conditions.inlet.VelocityComponentsInlet(
            name="velocity_components_inlet",
            profile_table=lc.tables.RectilinearTable(
                id="my_table",
                name="my_table",
                table_type=TableType.PROFILE_BC,
            ),
            total_temperature_column_index=1,
        )
    )
    assert velocity_components_inlet == _to_and_from_proto(velocity_components_inlet)
    velocity_inlet = param.physics.fluid.boundary_conditions.inlet.VelocityMagnitudeInlet(
        name="velocity_inlet"
    )
    assert velocity_inlet == _to_and_from_proto(velocity_inlet)

    # Materials
    material = param.MaterialEntity(
        material_identifier=lc.EntityIdentifier(
            name="Fluid",
            id="fluid_0",
        ),
        fluid=param.material.MaterialFluid(
            reference_pressure=101325,
            material_model=param.material.fluid.material_model.IdealGas(
                molecular_weight=40,
            ),
            viscosity_model=param.material.fluid.viscosity_model.PrescribedViscosity(
                viscosity=1e-3,
            ),
        ),
    )
    assert material == _to_and_from_proto(material)

    material.fluid.material_model = (
        param.material.fluid.material_model.IncompressibleFluidWithEnergy(
            specific_heat_cp=2000,
            density=10,
        )
    )
    assert material == _to_and_from_proto(material)

    # Physics
    physics = param.Physics(
        # must set identifier for the assert to pass bc it gets auto-generated in to_proto()
        physics_identifier=lc.EntityIdentifier(name="physics", id="physics_0"),
        fluid=param.physics.Fluid(),
    )
    assert isinstance(
        physics.fluid.turbulence.constants,
        param.physics.fluid.turbulence.spalart_allmaras.constants.DefaultSpalartAllmarasConstants,
    )
    assert physics == _to_and_from_proto(physics)


def test_params() -> None:
    params = lc.SimulationParam()
    params.basic.gravity = param.basic.gravity.GravityOn(
        acceleration=lc.types.Vector3(x=0, y=0, z=1.62)  # moon's gravity
    )

    # Assign a material to a volume
    air = param.MaterialEntity(
        material_identifier=lc.EntityIdentifier(
            name="air",
            id="fluid_0",
        ),
        fluid=param.material.MaterialFluid(
            reference_pressure=101325,
            material_model=param.material.fluid.material_model.IdealGas(),
            viscosity_model=param.material.fluid.viscosity_model.PrescribedViscosity(
                viscosity=1.2,
            ),
        ),
    )
    params.assign_material(air, "volume")
    assert len(params.materials) == 1
    assert params.materials[0] == air
    assert len(params.volume_entity) == 1
    assert params.volume_entity[0].volume_identifier.id == "volume"

    # Declare fluid physics
    physics = param.Physics(
        physics_identifier=lc.EntityIdentifier(
            name="Fluid",
            id="fluid_0",
        ),
        fluid=param.physics.Fluid(),
    )
    physics.fluid.basic.viscous_model = enum.ViscousModel.LAMINAR
    physics.fluid.turbulence.transition_model = enum.TransitionModel.AFT_2019
    params.assign_physics(physics, "volume")
    assert len(params.physics) == 1
    assert params.physics[0] == physics

    # Add a farfield boundary condition
    farfield_bc = param.physics.fluid.boundary_conditions.Farfield(
        name="farfield",
        direction=lc.types.Vector3(x=1, y=0, z=0),
    )
    physics.fluid.boundary_conditions.append(farfield_bc)
    assert len(physics.fluid.boundary_conditions) == 1
    assert physics.fluid.boundary_conditions[0] == farfield_bc

    # Reference values
    params.reference_values.v_ref = 300

    params.configure_adjoint_surface_output(
        lc.enum.QuantityType.DRAG, ["0/bound/airfoil"], moment_center=(0.25, 0, 0)
    )

    params_proto = params._to_proto()
    assert len(params_proto.volume_entity) == 1
    assert params_proto.volume_entity[0].volume_identifier.id == "volume"
    assert params_proto.general.gravity == clientpb.GRAVITY_ON
    assert params_proto.general.acceleration.x.value == 0
    assert params_proto.general.acceleration.y.value == 0
    assert params_proto.general.acceleration.z.value == 1.62
    assert len(params_proto.material_entity) == 1
    assert params_proto.material_entity[0].material_identifier.name == "air"
    assert len(params_proto.material_entity[0].material_identifier.id) > 0
    assert (
        params_proto.material_entity[0].material_fluid.laminar_viscosity_model_newtonian
        == clientpb.LAMINAR_CONSTANT_VISCOSITY
    )
    assert (
        params_proto.material_entity[0].material_fluid.laminar_constant_viscosity_constant.value
        == 1.2
    )
    assert (
        params_proto.material_entity[0].material_fluid.laminar_thermal_conductivity
        == clientpb.LAMINAR_CONSTANT_THERMAL_PRANDTL
    )
    assert len(params_proto.physics) == 1
    assert params_proto.physics[0].fluid.basic_fluid.viscous_model == clientpb.LAMINAR
    assert len(params_proto.physics[0].fluid.boundary_conditions_fluid) == 1
    assert (
        params_proto.physics[0].fluid.boundary_conditions_fluid[0].boundary_condition_name
        == "farfield"
    )
    assert (
        params_proto.physics[0].fluid.boundary_conditions_fluid[0].physical_boundary
        == clientpb.FARFIELD
    )
    assert (
        params_proto.physics[0]
        .fluid.boundary_conditions_fluid[0]
        .far_field_flow_direction_specification
        == clientpb.FARFIELD_DIRECTION
    )
    assert (
        params_proto.physics[0].fluid.boundary_conditions_fluid[0].farfield_flow_direction.x.value
        == 1
    )
    assert (
        params_proto.physics[0].fluid.boundary_conditions_fluid[0].farfield_flow_direction.y.value
        == 0
    )
    assert (
        params_proto.physics[0].fluid.boundary_conditions_fluid[0].farfield_flow_direction.z.value
        == 0
    )
    assert params_proto.reference_values.v_ref.value == 300

    assert params_proto.adjoint.adjoint_output.in_surfaces[0] == "0/bound/airfoil"
    assert (
        params_proto.adjoint.adjoint_output.force_properties.force_dir_type
        == outputpb.FORCE_DIRECTION_BODY_ORIENTATION_AND_FLOW_DIR
    )

    params_from_proto = lc.SimulationParam()
    params_from_proto._from_proto(params_proto)
    assert len(params_from_proto.physics[0].fluid.boundary_conditions) == 1
    assert params_from_proto.physics[0].fluid.boundary_conditions[0] == farfield_bc


def test_codegen() -> None:
    # Create a SimulationParam from scratch as an advanced SDK user would.
    # Then check that executing the code generated by "to_code" is equivalent.
    # This is also a nice real-world example (AeroSUV case).
    front_wheels_tags = ["0/bound/wheels-front"]
    rear_wheels_tags = ["0/bound/wheels-rear"]
    moving_groud_tags = [
        "0/bound/Ground_1",
        "0/bound/Belt_Ground",
        "0/bound/Belt_Wheels",
    ]
    slip_ground_tags = ["0/bound/Ground_2"]
    body_tags = [
        "0/bound/body",
        "0/bound/cooling-air-inlet-closing",
        "0/bound/cooling-air-outlet-closing",
        "0/bound/engine",
        "0/bound/exhaust",
        "0/bound/gear-box",
        "0/bound/grille-bottom",
        "0/bound/grille-top",
        "0/bound/side-mirrors",
        "0/bound/suspension-front",
        "0/bound/suspension-rear",
        "0/bound/underbody-detailed",
        "0/bound/rear-end_fastback",
    ]
    farfield_tags = [
        "0/bound/Inlet",
        "0/bound/Outlet",
        "0/bound/Tunnel Walls",
    ]

    # Materials can be setup via presets.
    material = lc.params.simulation.MaterialEntity(
        material_identifier=lc.EntityIdentifier(id="mat-0", name="air"),
        fluid=lc.params.simulation.material.MaterialFluid(
            preset=lc.params.enum.MaterialFluidPreset.STANDARD_AIR,
        ),
    )

    # Default-construct a fluid physics (defaults everything like the UI).
    physics = lc.params.simulation.Physics(
        physics_identifier=lc.EntityIdentifier(id="phy-0", name="fluid"),
        fluid=lc.params.simulation.physics.Fluid(),
    )
    physics.fluid.basic.viscous_model = lc.params.enum.ViscousModel.DES

    # This is a DES case and we do not have adequate presets yet, so we need to customize the discretization settings.
    physics.fluid.spatial_discretization.preset = (
        lc.params.enum.SpatialDiscretizationFluidPreset.CUSTOM_SPATIAL_DISCRETIZATION_FLUID
    )
    physics.fluid.spatial_discretization.convective_scheme = (
        lc.params.simulation.physics.fluid.spatial_discretization.convective_scheme.Ld2()
    )
    physics.fluid.spatial_discretization.convective_scheme.alpha_hybrid = 0.2
    physics.fluid.spatial_discretization.convective_scheme_order.geometry_fixes = (
        lc.params.enum.GeometryFixes.GEOMETRY_FIXES_OFF
    )
    physics.fluid.spatial_discretization.convective_scheme_order.limiter = (
        lc.params.enum.Limiter.NO_LIMITER
    )

    # Controls preset.
    physics.fluid.solution_controls.preset = (
        lc.params.enum.SolutionControlsFluidPreset.INTERMEDIATE_SOLUTION_CONTROLS_FLUID
    )

    # Initialization.
    physics.fluid.initialization = (
        lc.params.simulation.physics.fluid.initialization.FluidFarfieldValues()
    )
    physics.fluid.initialization.turbulence.spalart_allmaras = (
        lc.params.simulation.physics.fluid.initialization.turbulence.spalart_allmaras.InitFarfieldValuesSa()
    )

    # Add boundary conditions.
    farfield = lc.params.simulation.physics.fluid.boundary_conditions.Farfield()
    farfield.name = "Farfield"
    farfield.mach_number = 0.146
    farfield.temperature = 293.15
    farfield.surfaces = farfield_tags
    physics.fluid.boundary_conditions.append(farfield)

    symmetry = lc.params.simulation.physics.fluid.boundary_conditions.Symmetry()
    symmetry.name = "Symmetry"
    symmetry.surfaces = slip_ground_tags
    physics.fluid.boundary_conditions.append(symmetry)

    wall = lc.params.simulation.physics.fluid.boundary_conditions.Wall()
    wall.name = "Wall"
    wall.momentum = lc.params.simulation.physics.fluid.boundary_conditions.wall.momentum.WallModel()
    wall.surfaces = front_wheels_tags + rear_wheels_tags + body_tags + moving_groud_tags
    physics.fluid.boundary_conditions.append(wall)

    # Create the main param object and assign physics and materials.
    param = lc.SimulationParam()
    param.assign_material(material, "0")
    param.assign_physics(physics, "0")

    # Transient settings.
    param.basic.time = lc.params.enum.FlowBehavior.TRANSIENT
    param.time.time_step = 4.6192e-5
    param.time.time_step_ramp = lc.params.simulation.time.time_step_ramp.TimeStepRampOn(
        initial_time_step=param.time.time_step * 10,
        start_iteration=1000,
        end_iteration=1500,
    )
    param.time.compute_statistics = (
        lc.params.simulation.time.compute_statistics.ComputeStatisticsOn(
            start_iteration=8000,
            update_interval=1,
        )
    )
    param.output.iters_per_output = 0

    # Motion.
    global_frame = lc.params.simulation.MotionData(
        frame_id="global_frame_id",
        frame_name="Global",
        attached_domains=["0"],
    )
    front_wheels = lc.params.simulation.MotionData(
        frame_id="front_wheels",
        frame_name="Front Wheels",
        frame_parent="global_frame_id",
        attached_boundaries=front_wheels_tags,
        motion_type=lc.params.simulation.motion_data.motion_type.ConstantAngularMotion(
            angular_velocity=lc.types.vector3.Vector3(y=-656.17),
        ),
    )
    rear_wheels = lc.params.simulation.MotionData(
        frame_id="rear_wheels",
        frame_name="Rear Wheels",
        frame_parent="global_frame_id",
        attached_boundaries=rear_wheels_tags,
        motion_type=lc.params.simulation.motion_data.motion_type.ConstantAngularMotion(
            angular_velocity=lc.types.vector3.Vector3(y=-656.17),
        ),
        frame_transforms=[
            lc.params.simulation.motion_data.frame_transforms.TranslationalTransform(
                translation=lc.types.vector3.Vector3(x=0.6965),
            ),
        ],
    )
    ground = lc.params.simulation.MotionData(
        frame_id="ground",
        frame_name="Ground",
        frame_parent="global_frame_id",
        attached_boundaries=moving_groud_tags,
        motion_type=lc.params.simulation.motion_data.motion_type.ConstantTranslationMotion(
            translation_velocity=lc.types.vector3.Vector3(x=50.093),
        ),
    )
    param.motion_data.append(global_frame)
    param.motion_data.append(front_wheels)
    param.motion_data.append(rear_wheels)
    param.motion_data.append(ground)

    param.reference_values.v_ref = 255

    # This doesn't do anything, it's just to test the code generation for dictionary fields.
    param.surface_name["front_wheels"] = lc.params.simulation.SurfaceName(
        surface_name="0/bound/wheels-front"
    )
    param.surface_name["rear_wheels"] = lc.params.simulation.SurfaceName(
        surface_name="0/bound/wheels-rear"
    )

    code = param.to_code()
    assert len(code.split("\n")) == 286
    d = {}
    exec(code, d)
    assert d["obj"] == param
