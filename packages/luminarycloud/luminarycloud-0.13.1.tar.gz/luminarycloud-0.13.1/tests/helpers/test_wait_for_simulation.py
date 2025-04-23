# Copyright 2023-2024 Luminary Cloud, Inc. All Rights Reserved.
from copy import deepcopy
from typing import Iterable, Callable
from unittest.mock import patch, MagicMock

from google.protobuf.timestamp_pb2 import Timestamp

from luminarycloud._proto.api.v0.luminarycloud.simulation.simulation_pb2 import (
    GetSimulationGlobalResidualsResponse,
    Simulation,
    GetSimulationRequest,
    GetSimulationResponse,
)
from luminarycloud._helpers import wait_for_simulation
from luminarycloud._proto.api.v0.luminarycloud.common.common_pb2 import File


def mock_GetSimulation(
    simulation: Simulation,
    statuses: Iterable[Simulation.SimulationStatus.ValueType],
) -> Callable[
    [GetSimulationRequest],
    GetSimulationResponse,
]:
    _statuses = statuses.__iter__()

    def mock(
        req: GetSimulationRequest,
    ) -> GetSimulationResponse:
        _simulation = deepcopy(simulation)
        _simulation.status = next(_statuses)
        return GetSimulationResponse(
            simulation=_simulation,
        )

    return mock


@patch("luminarycloud.Client")
def test_wait_for_simulation(MockClient: MagicMock) -> None:
    mock_client = MockClient()
    mock_client.GetSimulation.side_effect = mock_GetSimulation(
        Simulation(
            id="this-is-a-fake-id",
            name="cube",
            create_time=Timestamp(seconds=0, nanos=0),
        ),
        statuses=[
            Simulation.SIMULATION_STATUS_PENDING,
            Simulation.SIMULATION_STATUS_ACTIVE,
            Simulation.SIMULATION_STATUS_COMPLETED,
        ],
    )

    got = wait_for_simulation(mock_client, Simulation(), interval_seconds=0)
    want = Simulation.SIMULATION_STATUS_COMPLETED
    assert got == want, "Did not get expected response"

    assert (
        mock_client.GetSimulation.call_count == 3
    ), f"Expected 3 calls to GetSimulation, got {mock_client.GetSimulation.call_count}"


@patch("luminarycloud.Client")
def test_wait_for_simulation_print_residuals(MockClient: MagicMock) -> None:
    mock_client = MockClient()
    mock_client.GetSimulation.side_effect = mock_GetSimulation(
        Simulation(
            id="this-is-a-fake-id",
            name="cube",
            create_time=Timestamp(seconds=0, nanos=0),
        ),
        statuses=[
            Simulation.SIMULATION_STATUS_PENDING,
            Simulation.SIMULATION_STATUS_ACTIVE,
            Simulation.SIMULATION_STATUS_ACTIVE,
            Simulation.SIMULATION_STATUS_ACTIVE,
            Simulation.SIMULATION_STATUS_ACTIVE,
            Simulation.SIMULATION_STATUS_COMPLETED,
        ],
    )
    mock_client.GetSimulationGlobalResiduals.return_value = GetSimulationGlobalResidualsResponse(
        csv_file=File(full_contents="foo,bar\n123,456\n".encode())
    )
    got = wait_for_simulation(mock_client, Simulation(), print_residuals=True, interval_seconds=0)
    want = Simulation.SIMULATION_STATUS_COMPLETED
    want_call_count = 6
    assert got == want, "Did not get expected response"
    assert (
        mock_client.GetSimulation.call_count == want_call_count
    ), f"Expected {want_call_count} calls to GetSimulation, got {mock_client.GetSimulation.call_count}"

    # GetSimulationGlobalResiduals should be called whenever simulation status is not pending
    want_call_count = 5
    assert (
        mock_client.GetSimulationGlobalResiduals.call_count == want_call_count
    ), f"Expected {want_call_count} calls to GetSimulationGlobalResiduals, got {mock_client.GetSimulationGlobalResiduals.call_count}"


@patch("luminarycloud.Client")
def test_wait_for_simulation_suspended(MockClient: MagicMock) -> None:
    mock_client = MockClient()
    mock_client.GetSimulation.side_effect = mock_GetSimulation(
        Simulation(
            id="this-is-a-fake-id",
            name="cube",
            create_time=Timestamp(seconds=0, nanos=0),
        ),
        statuses=[
            Simulation.SIMULATION_STATUS_PENDING,
            Simulation.SIMULATION_STATUS_ACTIVE,
            Simulation.SIMULATION_STATUS_SUSPENDED,
        ],
    )

    got = wait_for_simulation(mock_client, Simulation(), interval_seconds=0)
    want = Simulation.SIMULATION_STATUS_SUSPENDED
    assert got == want, "Did not get expected response"

    want_call_count = 3
    assert (
        mock_client.GetSimulation.call_count == want_call_count
    ), f"Expected {want_call_count} calls to GetSimulation, got {mock_client.GetSimulation.call_count}"
