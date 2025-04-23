# Copyright 2023-2024 Luminary Cloud, Inc. All Rights Reserved.
import pytest
from luminarycloud import (
    Solution,
)
from luminarycloud._proto.api.v0.luminarycloud.solution import solution_pb2 as solutionpb


def test_solution_attr() -> None:
    solution = Solution(
        solutionpb.Solution(
            id="solution-id",
            simulation_id="simulation-id",
            iteration=5,
            physical_time=3.14,
        )
    )
    assert solution.id == "solution-id", f'expected id = "solution-id", got {solution.id}'
    assert (
        solution.simulation_id == "simulation-id"
    ), f'expected simulation_id = "simulation-id", got {solution.simulation_id}'
    assert solution.iteration == 5, "expected solution.iteration = 5, got {solution.iteration}"
    assert solution.physical_time == pytest.approx(
        3.14
    ), f"expected solution.physical_time to be approx 3.14, got {solution.physical_time}"
