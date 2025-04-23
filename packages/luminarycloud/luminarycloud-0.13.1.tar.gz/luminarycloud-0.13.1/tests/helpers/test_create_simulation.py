# Copyright 2023-2024 Luminary Cloud, Inc. All Rights Reserved.
from unittest.mock import patch, MagicMock

from google.protobuf.timestamp_pb2 import Timestamp

from luminarycloud._proto.api.v0.luminarycloud.simulation.simulation_pb2 import (
    Simulation,
    SimulationOptions,
    CreateSimulationRequest,
    CreateSimulationResponse,
)
from luminarycloud._helpers import create_simulation


@patch("luminarycloud.Client")
def test_create_simulation_simulation_param(
    MockClient: MagicMock,
) -> None:
    mock_client = MockClient()
    mock_simulation = Simulation(
        id="this-is-a-fake-id",
        name="cube",
        create_time=Timestamp(seconds=0, nanos=0),
        status=Simulation.SIMULATION_STATUS_PENDING,
    )
    mock_simulation_template_id = "this-is-a-sim-config"
    mock_response = CreateSimulationResponse(
        simulation=mock_simulation,
    )
    mock_client.CreateSimulation.return_value = mock_response

    got = create_simulation(
        mock_client,
        "fake-project-id",
        "fake-mesh-id",
        mock_simulation.name,
        mock_simulation_template_id,
        batch_processing=True,
    )
    want = mock_response.simulation
    assert got == want, "Did not get expected response"

    # the main thing we're checking with this unit test is that
    # create_simulation correctly parsed the json as a SimulationParam and set
    # simulation_param in the request
    mock_client.CreateSimulation.assert_called_with(
        CreateSimulationRequest(
            project_id="fake-project-id",
            mesh_id="fake-mesh-id",
            name=mock_simulation.name,
            simulation_template_id=mock_simulation_template_id,
            simulation_options=SimulationOptions(batch_processing=True),
        )
    )
