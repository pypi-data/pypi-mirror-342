# Copyright 2023-2024 Luminary Cloud, Inc. All Rights Reserved.
import pytest
from unittest.mock import MagicMock, patch

from luminarycloud import (
    Client,
    Project,
    Simulation,
    SimulationTemplate,
    Solution,
    set_default_client,
)
from luminarycloud._proto.api.v0.luminarycloud.project import project_pb2 as projectpb
from luminarycloud._proto.api.v0.luminarycloud.simulation import simulation_pb2 as simulationpb
from luminarycloud._proto.api.v0.luminarycloud.solution import solution_pb2 as solutionpb
from luminarycloud._proto.api.v0.luminarycloud.simulation_template import (
    simulation_template_pb2 as simtemplatepb,
)


@pytest.fixture
def project() -> Project:
    return Project(projectpb.Project(id="project-id"))


@pytest.fixture
def simulation() -> Simulation:
    return Simulation(simulationpb.Simulation(id="simulation-id"))


@pytest.fixture
def solution() -> Solution:
    return Solution(solutionpb.Solution(id="solution-id"))


@pytest.fixture
def simulation_template() -> SimulationTemplate:
    return SimulationTemplate(simtemplatepb.SimulationTemplate(id="simtemplate-id"))


@pytest.fixture
@patch("luminarycloud.Client")
def mock_client(MockClient: MagicMock) -> Client:
    mock_client = MockClient()
    set_default_client(mock_client)
    return mock_client
