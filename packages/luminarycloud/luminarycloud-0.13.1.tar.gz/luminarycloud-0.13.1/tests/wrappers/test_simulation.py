# Copyright 2023-2024 Luminary Cloud, Inc. All Rights Reserved.
from unittest.mock import MagicMock

from luminarycloud import (
    Project,
    Simulation,
    get_simulation,
)
from luminarycloud.enum import SimulationStatus, GPUType
from luminarycloud._proto.api.v0.luminarycloud.simulation import simulation_pb2 as simulationpb
from luminarycloud._proto.api.v0.luminarycloud.solution import solution_pb2 as solutionpb


def test_simulation_attr() -> None:
    simulation = Simulation(
        simulationpb.Simulation(
            id="simulation-id",
            name="name",
            status=simulationpb.Simulation.SIMULATION_STATUS_COMPLETED,
            mesh_id="mesh-id",
        )
    )
    assert simulation.id == "simulation-id"
    assert simulation.name == "name"
    assert simulation.mesh_id == "mesh-id"
    assert simulation.status == SimulationStatus.COMPLETED
    assert isinstance(simulation.status, SimulationStatus)


def test_get_simulation(mock_client: MagicMock) -> None:
    mock_client.GetSimulation.return_value = simulationpb.GetSimulationResponse(
        simulation=simulationpb.Simulation(),
    )
    got = get_simulation("simulation-id")
    assert isinstance(got, Simulation), "Did not get expected type of response"
    mock_client.GetSimulation.assert_called_with(
        simulationpb.GetSimulationRequest(id="simulation-id")
    )


def test_create_simulation_client_simulation_param(
    mock_client: MagicMock,
    project: Project,
) -> None:
    mock_client.CreateSimulation.return_value = simulationpb.CreateSimulationResponse(
        simulation=simulationpb.Simulation(),
    )
    mesh_id = "mesh-1234"
    sim_name = "simulation-name"
    sim_template_id = "simtemplate-id"
    got = project.create_simulation(
        mesh_id,
        sim_name,
        sim_template_id,
        batch_processing=True,
    )
    assert got is not None, "Did not get expected simulation"

    mock_client.CreateSimulation.assert_called_with(
        simulationpb.CreateSimulationRequest(
            project_id=project.id,
            mesh_id=mesh_id,
            name=sim_name,
            simulation_template_id=sim_template_id,
            simulation_options=simulationpb.SimulationOptions(batch_processing=True),
        )
    )


def test_create_simulation_gpu_prefs(
    mock_client: MagicMock,
    project: Project,
) -> None:
    mock_client.CreateSimulation.return_value = simulationpb.CreateSimulationResponse(
        simulation=simulationpb.Simulation(),
    )
    mesh_id = "mesh-1234"
    sim_name = "simulation-name"
    sim_template_id = "simtemplate-id"
    got = project.create_simulation(
        mesh_id,
        sim_name,
        sim_template_id,
        batch_processing=True,
        gpu_type=GPUType.V100,
        gpu_count=1,
    )
    assert got is not None, "Did not get expected simulation"

    mock_client.CreateSimulation.assert_called_with(
        simulationpb.CreateSimulationRequest(
            project_id=project.id,
            mesh_id=mesh_id,
            name=sim_name,
            simulation_template_id=sim_template_id,
            simulation_options=simulationpb.SimulationOptions(
                batch_processing=True,
                gpu_type=GPUType.V100,
                gpu_count=1,
            ),
        )
    )


def test_list_simulations(mock_client: MagicMock, project: Project) -> None:
    mock_client.ListSimulations.return_value = simulationpb.ListSimulationsResponse(
        simulations=[simulationpb.Simulation(), simulationpb.Simulation()],
    )
    got = project.list_simulations()
    assert len(got) == 2, "Did not get expected number of simulations"
    mock_client.ListSimulations.assert_called_with(
        simulationpb.ListSimulationsRequest(project_id="project-id")
    )


def test_update_simulation(mock_client: MagicMock, simulation: Simulation) -> None:
    mock_client.UpdateSimulation.return_value = simulationpb.UpdateSimulationResponse(
        simulation=simulationpb.Simulation(
            id="simulation-id",
            name="simulation-name",
        )
    )
    simulation.update(name="simulation-name")
    assert (
        simulation.name == "simulation-name"
    ), "simulation wrapper did not forward reply from mock client"
    mock_client.UpdateSimulation.assert_called_with(
        simulationpb.UpdateSimulationRequest(
            id="simulation-id",
            name="simulation-name",
        )
    )


def test_list_solutions(mock_client: MagicMock, simulation: Simulation) -> None:
    mock_client.ListSolutions.return_value = solutionpb.ListSolutionsResponse(
        solutions=[solutionpb.Solution(), solutionpb.Solution()],
    )
    got = simulation.list_solutions()
    assert len(got) == 2, f"Expected 2 solutions, got {len(got)}: {got}"
    mock_client.ListSolutions.assert_called_with(
        solutionpb.ListSolutionsRequest(simulation_id=simulation.id)
    )
