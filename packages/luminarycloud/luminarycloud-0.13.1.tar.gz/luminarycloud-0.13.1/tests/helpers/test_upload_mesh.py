# Copyright 2023-2024 Luminary Cloud, Inc. All Rights Reserved.
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from luminarycloud.enum import MeshType
from luminarycloud._proto.api.v0.luminarycloud.mesh import mesh_pb2 as meshpb
from luminarycloud._helpers import upload_mesh
from luminarycloud._helpers._upload_mesh import _is_valid_upload_url
from luminarycloud._proto.upload import upload_pb2 as uploadpb


@pytest.fixture()
def mesh_file_path(test_data_dir: Path) -> Path:
    return test_data_dir / "cube.cgns"


def test_is_valid_upload_url() -> None:
    testcases = [
        ("https://example.com/foo.cgns", True),
        ("http://example.com/foo.cgns", True),
        ("C:\\Users\\foo\\Documents\\Luminary API Testing\\FooBar.cgns", False),
        ("C:\\Users\\foo\\Documents\\Luminary_API_Testing\\FooBar.cgns", False),
        ("C:/Users/foo/Documents/Luminary_API_Testing/FooBar.cgns", False),
        ("foo/bar/test.cgns", False),
        ("./foo/bar/test.cgns", False),
        ("/foo/bar/test.cgns", False),
        ("file://foo/bar/test.cgns", False),
    ]
    for path, want in testcases:
        assert _is_valid_upload_url(path) == want


@patch("luminarycloud._helpers._upload_mesh.gcs_resumable_upload")
@patch("luminarycloud.Client")
def test_upload_mesh_from_file(
    MockClient: MagicMock,
    mock_gcs_resumable_upload: MagicMock,
    mesh_file_path: Path,
) -> None:
    mock_client = MockClient()
    mock_response_create_upload = uploadpb.CreateUploadReply(
        upload=uploadpb.Upload(
            id="fake-upload-id-fakefake",
        )
    )
    mock_response_start_upload = uploadpb.StartUploadReply(
        upload=uploadpb.Upload(
            id="fake-upload-id-fakefake",
            gcs_resumable=uploadpb.GCSResumableMethod(
                signed_url="https://example.com/foo.cgns",
                http_headers={"foo": "bar"},
            ),
        )
    )
    mock_finish_upload_reply = uploadpb.FinishUploadReply(
        url="gs://foo/bar/test.cgns", mesh_id="fake-mesh-id"
    )
    mock_get_mesh_response = meshpb.GetMeshResponse(
        mesh=meshpb.Mesh(
            id="fake-mesh-id",
        )
    )

    mock_client.CreateUpload.return_value = mock_response_create_upload
    mock_client.StartUpload.return_value = mock_response_start_upload
    mock_client.FinishUpload.return_value = mock_finish_upload_reply
    mock_client.GetMesh.return_value = mock_get_mesh_response

    # Mock the gcs_resumable_upload function because we don't want to start dealing with GCS or
    # mocking http.
    mock_gcs_resumable_upload.return_value = None

    got = upload_mesh(
        mock_client,
        "fake-project-id",
        mesh_file_path,
        do_not_read_zones_openfoam=True,
    )
    want = mock_get_mesh_response.mesh

    assert got == want, "Did not get expected response"
    assert (
        len(mock_client.CreateUpload.mock_calls) == 1
    ), f"Expected 1 calls to UploadMesh, got {len(mock_client.CreateUpload.mock_calls)}"
    assert (
        len(mock_client.StartUpload.mock_calls) == 1
    ), f"Expected 1 calls to StartUpload, got {len(mock_client.StartUpload.mock_calls)}"
    assert (
        len(mock_client.FinishUpload.mock_calls) == 1
    ), f"Expected 1 calls to FinishUpload, got {len(mock_client.FinishUpload.mock_calls)}"
    assert (
        len(mock_client.GetMesh.mock_calls) == 1
    ), f"Expected 1 calls to GetMesh, got {len(mock_client.GetMesh.mock_calls)}"

    first_req = mock_client.CreateUpload.mock_calls[0].args[0]
    assert first_req.project_id == "fake-project-id", "First request contains incorrect project ID"
    assert (
        first_req.resource_params.mesh_params.mesh_type == MeshType.CGNS
    ), "UploadMesh called with incorrect mesh type"
    assert (
        first_req.resource_params.mesh_params.do_not_read_zones_openfoam == True
    ), "UploadMesh called with unexpected value for `do_not_read_zones_openfoam`"
