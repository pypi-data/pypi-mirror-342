# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
import pytest
from google.protobuf.json_format import Parse

from luminarycloud._helpers.cond import params_to_dict
from luminarycloud._helpers.defaults import _reset_defaults
import luminarycloud._proto.client.simulation_pb2 as clientpb


@pytest.fixture()
def client_simulation_param(client_simulation_param_json_bytes: bytes) -> clientpb.SimulationParam:
    return Parse(client_simulation_param_json_bytes, clientpb.SimulationParam())


def test_params_to_dict(client_simulation_param: clientpb.SimulationParam) -> None:
    params_dict = params_to_dict(client_simulation_param)
    # spot-check a few params
    assert (
        params_dict["general"]["flow_behavior"] == "STEADY"
    ), "general.flow_behavior is not STEADY"
    assert (
        params_dict["general"]["gravity"] == "GRAVITY_OFF"
    ), "general.gravity is not set to default value GRAVITY_OFF"
    assert (
        "acceleration" not in params_dict["general"]
    ), "general.acceleration is present even though it is not active"
    assert (
        params_dict["physics"][0]["fluid"]["boundary_conditions_fluid"][0]["physical_boundary"]
        == "SYMMETRY"
    )

    for bc in params_dict["physics"][0]["fluid"]["boundary_conditions_fluid"]:
        assert bc.get("fixed_temperature") is None


def test_cht_params_to_dict() -> None:

    # Test that uniform_t is hidden if there is no heat physics and fluid is incompressible
    params = clientpb.SimulationParam()

    # Set density_relationship to CONSTANT_DENSITY since the default value enables uniform_t
    fluid_material = clientpb.MaterialEntity()
    fluid_material.material_identifier.id = "my material"
    fluid_material.material_fluid.density_relationship = clientpb.CONSTANT_DENSITY
    params.material_entity.append(fluid_material)

    # Set uniform_t to some non-default value
    fluid_physics = clientpb.Physics()
    fluid_physics.physics_identifier.id = "my physics"
    fluid_physics.fluid.initialization_fluid.uniform_t.value = 300
    params.physics.append(fluid_physics)

    volume_material = clientpb.VolumeMaterialRelationship()
    volume_material.volume_identifier.id = "1"
    volume_material.material_identifier.id = fluid_material.material_identifier.id
    params.entity_relationships.volume_material_relationship.append(volume_material)

    volume_physics = clientpb.VolumePhysicsRelationship()
    volume_physics.volume_identifier.id = "1"
    volume_physics.physics_identifier.id = fluid_physics.physics_identifier.id
    params.entity_relationships.volume_physics_relationship.append(volume_physics)

    params_dict = params_to_dict(params)

    assert (
        params_dict["material_entity"][0]["material_fluid"]["density_relationship"]
        == "CONSTANT_DENSITY"
    ), "general.gravity is not set to default value GRAVITY_OFF"
    assert "heat" not in params_dict["physics"][0], "general.physics[0] should not have heat"
    assert "fluid" in params_dict["physics"][0], "general.physics[0] should have fluid"
    assert (
        "uniform_t" not in params_dict["physics"][0]["fluid"]["initialization_fluid"]
    ), "general.physics[0].initialization_fluid should not have uniform_t"

    # Test that uniform_t is enabled if heat physics is added
    heat_physics = clientpb.Physics()
    _reset_defaults(heat_physics.heat)
    heat_physics.physics_identifier.id = "my heat physics"
    params.physics.append(heat_physics)

    volume_physics = clientpb.VolumePhysicsRelationship()
    volume_physics.volume_identifier.id = "1"
    volume_physics.physics_identifier.id = heat_physics.physics_identifier.id
    params.entity_relationships.volume_physics_relationship.append(volume_physics)

    params_dict = params_to_dict(params)

    assert (
        "uniform_t" in params_dict["physics"][0]["fluid"]["initialization_fluid"]
    ), "general.physics[0].initialization_fluid should have uniform_t"
