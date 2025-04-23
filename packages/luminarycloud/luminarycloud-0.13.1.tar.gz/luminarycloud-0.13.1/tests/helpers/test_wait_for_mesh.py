# Copyright 2023-2024 Luminary Cloud, Inc. All Rights Reserved.
from copy import deepcopy
from time import sleep
from typing import Iterable, Callable
from unittest.mock import patch, MagicMock

from google.protobuf.timestamp_pb2 import Timestamp
import pytest

from luminarycloud._proto.api.v0.luminarycloud.mesh.mesh_pb2 import (
    Mesh,
    GetMeshRequest,
    GetMeshResponse,
)
from luminarycloud._helpers._wait_for_mesh import wait_for_mesh


def mock_GetMesh(
    mesh: Mesh,
    statuses: Iterable[Mesh.MeshStatus.ValueType],
    delay: int = 0,
) -> Callable[
    [GetMeshRequest],
    GetMeshResponse,
]:
    _statuses = statuses.__iter__()

    def mock(
        req: GetMeshRequest,
    ) -> GetMeshResponse:
        sleep(delay)
        _mesh = deepcopy(mesh)
        _mesh.status = next(_statuses)
        return GetMeshResponse(
            mesh=_mesh,
        )

    return mock


@patch("luminarycloud.Client")
def test_wait_for_mesh(MockClient: MagicMock) -> None:
    mock_client = MockClient()
    mock_client.GetMesh.side_effect = mock_GetMesh(
        Mesh(
            id="this-is-a-fake-id",
            name="cube",
            create_time=Timestamp(seconds=0, nanos=0),
        ),
        statuses=[
            Mesh.MESH_STATUS_CREATING,
            Mesh.MESH_STATUS_CREATING,
            Mesh.MESH_STATUS_COMPLETED,
        ],
    )

    got = wait_for_mesh(mock_client, Mesh(), interval_seconds=0)
    want = Mesh.MESH_STATUS_COMPLETED
    assert got == want, "Did not get expected response"

    assert (
        len(mock_client.GetMesh.mock_calls) == 3
    ), f"Expected 3 calls to GetMesh, got {len(mock_client.GetMesh.mock_calls)}"


@patch("luminarycloud.Client")
def test_wait_for_mesh_timeout(MockClient: MagicMock) -> None:
    mock_client = MockClient()
    mock_client.GetMesh.side_effect = mock_GetMesh(
        Mesh(),
        statuses=[
            Mesh.MESH_STATUS_CREATING,
            Mesh.MESH_STATUS_COMPLETED,
        ],
        delay=1,
    )

    with pytest.raises(TimeoutError):
        wait_for_mesh(mock_client, Mesh(), interval_seconds=0, timeout_seconds=0.1)

    assert (
        len(mock_client.GetMesh.mock_calls) == 1
    ), f"Expected 1 calls to GetMesh, got {len(mock_client.GetMesh.mock_calls)}"
