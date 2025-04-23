# Copyright 2023-2024 Luminary Cloud, Inc. All Rights Reserved.
from unittest.mock import MagicMock, call
from operator import length_hint

import luminarycloud as lc
from luminarycloud._proto.api.v0.luminarycloud.project import project_pb2 as projectpb
from luminarycloud._proto.api.v0.luminarycloud.mesh import mesh_pb2 as meshpb


def test_project_attr() -> None:
    project = lc.Project(
        projectpb.Project(
            id="project-id",
            name="name",
            description="description",
        )
    )
    assert project.id == "project-id"
    assert project.name == "name"
    assert project.description == "description"


def test_create_project(mock_client: MagicMock) -> None:
    mock_client.CreateProject.return_value = projectpb.CreateProjectResponse(
        project=projectpb.Project(),
    )
    got = lc.create_project("name")
    assert isinstance(got, lc.Project), "Did not get expected type of response"
    mock_client.CreateProject.assert_called_with(projectpb.CreateProjectRequest(name="name"))


def test_get_project(mock_client: MagicMock) -> None:
    mock_client.GetProject.return_value = projectpb.GetProjectResponse(
        project=projectpb.Project(),
    )
    got = lc.get_project("project-id")
    assert isinstance(got, lc.Project), "Did not get expected type of response"
    mock_client.GetProject.assert_called_with(projectpb.GetProjectRequest(id="project-id"))


def test_list_projects(mock_client: MagicMock) -> None:
    mock_client.ListProjects.return_value = projectpb.ListProjectsResponse(
        projects=[projectpb.Project(), projectpb.Project()],
        total_count=2,
        next_page_token="",
    )
    got = lc.list_projects()
    assert len(got) == 2, "Did not get expected number of projects"
    mock_client.ListProjects.assert_called_once_with(
        projectpb.ListProjectsRequest(page_size=50, page_token="")
    )


def test_iterate_projects(mock_client: MagicMock) -> None:
    mock_client.ListProjects.side_effect = [
        projectpb.ListProjectsResponse(
            total_count=3,
            projects=[projectpb.Project(), projectpb.Project()],
            next_page_token="next-token",  # First call returns a next page token
        ),
        projectpb.ListProjectsResponse(
            total_count=3,
            projects=[projectpb.Project()],  # Second call returns the final item
            next_page_token="",  # Empty token indicates no more pages
        ),
    ]
    got = lc.iterate_projects(page_size=2)
    assert length_hint(got) == 3, "Did not get expected length hint on projects iterator"
    assert len(list(got)) == 3, "Did not get expected number of projects"
    mock_client.ListProjects.assert_has_calls(
        [
            call(projectpb.ListProjectsRequest(page_size=2, page_token="")),
            call(projectpb.ListProjectsRequest(page_size=2, page_token="next-token")),
        ]
    )


def test_update_project(mock_client: MagicMock, project: lc.Project) -> None:
    mock_client.UpdateProject.return_value = projectpb.UpdateProjectResponse(
        project=projectpb.Project(
            id="project-id",
            description="description",
        )
    )
    project.update(description="description")
    assert (
        project.description == "description"
    ), "project wrapper did not forward reply from mock client"
    mock_client.UpdateProject.assert_called_with(
        projectpb.UpdateProjectRequest(
            id="project-id",
            description="description",
        )
    )


def test_delete_project(mock_client: MagicMock, project: lc.Project) -> None:
    project.delete()
    mock_client.DeleteProject.assert_called_with(
        projectpb.DeleteProjectRequest(
            id="project-id",
        )
    )


def test_create_mesh_no_aspect(mock_client: MagicMock, project: lc.Project) -> None:
    test_mesh_id = "mesh-id"
    mock_client.CreateMesh.return_value = meshpb.CreateMeshResponse(
        mesh=meshpb.Mesh(
            id=test_mesh_id,
            # mock response doesn't really matter
        )
    )
    test_adaptation_params = lc.meshing.MeshAdaptationParams(
        source_simulation_id="source-sim-id", target_cv_count=1000000, h_ratio=1.0
    )
    test_mesh_name = "test adptated mesh"
    mesh = project.create_mesh(test_adaptation_params, name=test_mesh_name)

    assert mesh.id == test_mesh_id, "project wrapper did not forward reply from mock client"
    mock_client.CreateMesh.assert_called_with(
        meshpb.CreateMeshRequest(
            project_id=project.id,
            name=test_mesh_name,
            mesh_adaptation_params=test_adaptation_params._to_proto(),
        )
    )


def test_create_mesh(mock_client: MagicMock, project: lc.Project) -> None:
    test_mesh_id = "mesh-id"
    mock_client.CreateMesh.return_value = meshpb.CreateMeshResponse(
        mesh=meshpb.Mesh(
            id=test_mesh_id,
            # mock response doesn't really matter
        )
    )
    test_adaptation_params = lc.meshing.MeshAdaptationParams(
        source_simulation_id="source-sim-id",
        target_cv_count=1000000,
        h_ratio=1.0,
        aspect_ratio=5.0,
    )
    test_mesh_name = "test adptated mesh"
    mesh = project.create_mesh(
        test_adaptation_params,
        name=test_mesh_name,
    )

    assert mesh.id == test_mesh_id, "project wrapper did not forward reply from mock client"
    mock_client.CreateMesh.assert_called_with(
        meshpb.CreateMeshRequest(
            project_id=project.id,
            name=test_mesh_name,
            mesh_adaptation_params=test_adaptation_params._to_proto(),
        )
    )
