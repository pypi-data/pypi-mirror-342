# Copyright 2023-2024 Luminary Cloud, Inc. All Rights Reserved.
from unittest.mock import MagicMock

import luminarycloud as lc
from luminarycloud.enum import MeshStatus
from luminarycloud._proto.api.v0.luminarycloud.mesh import mesh_pb2 as meshpb
from luminarycloud._proto.api.v0.luminarycloud.project import project_pb2 as projectpb
from luminarycloud.params.geometry import (
    AnnularCylinder,
    Cube,
    Cylinder,
    OrientedCube,
    Sphere,
    SphereShell,
)


def test_mesh_attr() -> None:
    mesh = lc.Mesh(
        meshpb.Mesh(
            id="mesh-id",
            name="name",
            status=meshpb.Mesh.MESH_STATUS_COMPLETED,
        )
    )
    assert mesh.id == "mesh-id"
    assert mesh.name == "name"
    assert mesh.status == MeshStatus.COMPLETED
    assert isinstance(mesh.status, MeshStatus)


# test attrs and _to_proto
def test_mesh_adaptation_parameters() -> None:
    test_source_sim_id = "source-sim-id"
    test_cv_count = 1000000
    test_h_ratio = 1.0
    test_aspect_ratio_default = 0.0
    test_aspect_ratio = 5.0

    ma_params = lc.meshing.MeshAdaptationParams(
        source_simulation_id=test_source_sim_id, target_cv_count=test_cv_count, h_ratio=test_h_ratio
    )
    assert ma_params.source_simulation_id == test_source_sim_id
    assert ma_params.target_cv_count == test_cv_count
    assert ma_params.h_ratio == test_h_ratio
    assert ma_params.aspect_ratio == test_aspect_ratio_default

    ma_proto = ma_params._to_proto()
    assert ma_proto.source_simulation_id == test_source_sim_id
    assert ma_proto.target_cv_count == test_cv_count
    assert ma_proto.h_ratio == test_h_ratio
    assert ma_proto.aspect_ratio == test_aspect_ratio_default

    ma_params = lc.meshing.MeshAdaptationParams(
        source_simulation_id=test_source_sim_id,
        target_cv_count=test_cv_count,
        h_ratio=test_h_ratio,
        aspect_ratio=test_aspect_ratio,
    )
    assert ma_params.source_simulation_id == test_source_sim_id
    assert ma_params.target_cv_count == test_cv_count
    assert ma_params.h_ratio == test_h_ratio
    assert ma_params.aspect_ratio == test_aspect_ratio

    ma_proto = ma_params._to_proto()
    assert ma_proto.source_simulation_id == test_source_sim_id
    assert ma_proto.target_cv_count == test_cv_count
    assert ma_proto.h_ratio == test_h_ratio
    assert ma_proto.aspect_ratio == test_aspect_ratio


def test_mesh_generation_params(mock_client: MagicMock) -> None:
    params = lc.meshing.MeshGenerationParams(
        geometry_id="geometry-id",
        sizing_strategy=lc.meshing.sizing_strategy.MinimalCount(),
    )
    assert params.geometry_id == "geometry-id"
    assert params.sizing_strategy == lc.meshing.sizing_strategy.MinimalCount()
    assert params.min_size == 0.0001
    assert params.max_size == 512
    assert params.body_x_axis == lc.types.Vector3(1, 0, 0)
    assert params.body_y_axis == lc.types.Vector3(0, 1, 0)
    assert params.proximity_layers == 1
    assert params.add_refinement is False

    params_proto = params._to_proto()
    assert params_proto.geometry_id == "geometry-id"
    assert (
        params_proto.mesh_complexity_params.type
        == meshpb.MeshGenerationParams.MeshComplexityParams.ComplexityType.MIN
    )
    assert params_proto.meshing_mode.WhichOneof("mode") == "base"

    req = meshpb.CreateMeshRequest(
        project_id="project-id",
        name="name",
    )
    req.mesh_generation_params.CopyFrom(params._to_proto())
    req.mesh_generation_params.volume_params.append(
        meshpb.MeshGenerationParams.VolumeParams(
            min_size=params.min_size,
            max_size=params.max_size,
        )
    )

    assert req.mesh_generation_params.meshing_mode.WhichOneof("mode") == "base"

    mock_client.CreateMesh.return_value = meshpb.CreateMeshResponse(
        mesh=meshpb.Mesh(id="mesh-id"),
    )

    project = lc.Project(projectpb.Project(id="project-id"))
    project.create_or_get_mesh(params, name="name")
    mock_client.CreateMesh.assert_called_with(req)


def test_get_mesh(mock_client: MagicMock) -> None:
    mock_client.GetMesh.return_value = meshpb.GetMeshResponse(
        mesh=meshpb.Mesh(),
    )
    got = lc.get_mesh("mesh-id")
    assert isinstance(got, lc.Mesh), "Did not get expected type of response"
    mock_client.GetMesh.assert_called_with(meshpb.GetMeshRequest(id="mesh-id"))


def test_list_meshes(mock_client: MagicMock, project: lc.Project) -> None:
    mock_client.ListMeshes.return_value = meshpb.ListMeshesResponse(
        meshes=[meshpb.Mesh(), meshpb.Mesh()],
    )
    got = project.list_meshes()
    assert len(got) == 2, "Did not get expected number of meshes"
    mock_client.ListMeshes.assert_called_with(meshpb.ListMeshesRequest(project_id="project-id"))


def test_update_mesh(mock_client: MagicMock) -> None:
    mesh_proto = meshpb.Mesh(
        id="mesh-id",
        name="name",
        status=meshpb.Mesh.MESH_STATUS_COMPLETED,
    )
    mesh = lc.Mesh(mesh_proto)
    mock_client.UpdateMesh.return_value = meshpb.UpdateMeshResponse(
        # we don't really care about what's returned; we're just using the mock
        # for assert_called_with
        mesh=mesh_proto,
    )
    _ = mesh.update(name="new name")
    mock_client.UpdateMesh.assert_called_with(meshpb.UpdateMeshRequest(id=mesh.id, name="new name"))


def test_refinement_region_shape_proto() -> None:
    """Check that we can transform Shape into proto."""
    shapes = [
        Sphere(center=lc.types.Vector3(1, 2, 3), radius=4),
        SphereShell(center=lc.types.Vector3(1, 2, 3), radius=4, radius_inner=2),
        Cube(min=lc.types.Vector3(1, 2, 3), max=lc.types.Vector3(4, 5, 6)),
        OrientedCube(
            min=lc.types.Vector3(1, 2, 3),
            max=lc.types.Vector3(4, 5, 6),
            origin=lc.types.Vector3(7, 8, 9),
            x_axis=lc.types.Vector3(10, 11, 12),
            y_axis=lc.types.Vector3(13, 14, 15),
        ),
        Cylinder(start=lc.types.Vector3(1, 2, 3), end=lc.types.Vector3(4, 5, 6), radius=7),
        AnnularCylinder(
            start=lc.types.Vector3(1, 2, 3),
            end=lc.types.Vector3(4, 5, 6),
            radius=7,
            radius_inner=5,
        ),
    ]
    for shape in shapes:
        refinement_region = lc.meshing.RefinementRegion(
            name="foo",
            h_limit=10,
            shape=shape,
        )
        assert refinement_region.shape == shape
        proto = refinement_region._to_proto()
        assert proto.h_limit == 10
        # We don't let the users set the IDs, so we take the names as the IDs.
        assert proto.name in proto.id

        if isinstance(shape, Sphere):
            assert proto.sphere.radius == shape.radius
            assert proto.sphere.center.x == shape.center.x
            assert proto.sphere.center.y == shape.center.y
            assert proto.sphere.center.z == shape.center.z
        elif isinstance(shape, SphereShell):
            assert proto.sphere_shell.radius == shape.radius
            assert proto.sphere_shell.radius_inner == shape.radius_inner
            assert proto.sphere_shell.center.x == shape.center.x
            assert proto.sphere_shell.center.y == shape.center.y
            assert proto.sphere_shell.center.z == shape.center.z
        elif isinstance(shape, Cube):
            assert proto.cube.min.x == shape.min.x
            assert proto.cube.min.y == shape.min.y
            assert proto.cube.min.z == shape.min.z
            assert proto.cube.max.x == shape.max.x
            assert proto.cube.max.y == shape.max.y
            assert proto.cube.max.z == shape.max.z
        elif isinstance(shape, OrientedCube):
            assert proto.oriented_cube.min.x == shape.min.x
            assert proto.oriented_cube.min.y == shape.min.y
            assert proto.oriented_cube.min.z == shape.min.z
            assert proto.oriented_cube.max.x == shape.max.x
            assert proto.oriented_cube.max.y == shape.max.y
            assert proto.oriented_cube.max.z == shape.max.z
            assert proto.oriented_cube.origin.x == shape.origin.x
            assert proto.oriented_cube.origin.y == shape.origin.y
            assert proto.oriented_cube.origin.z == shape.origin.z
            assert proto.oriented_cube.x_axis.x == shape.x_axis.x
            assert proto.oriented_cube.x_axis.y == shape.x_axis.y
            assert proto.oriented_cube.x_axis.z == shape.x_axis.z
            assert proto.oriented_cube.y_axis.x == shape.y_axis.x
            assert proto.oriented_cube.y_axis.y == shape.y_axis.y
            assert proto.oriented_cube.y_axis.z == shape.y_axis.z
        elif isinstance(shape, Cylinder):
            assert proto.cylinder.start.x == shape.start.x
            assert proto.cylinder.start.y == shape.start.y
            assert proto.cylinder.start.z == shape.start.z
            assert proto.cylinder.end.x == shape.end.x
            assert proto.cylinder.end.y == shape.end.y
            assert proto.cylinder.end.z == shape.end.z
            assert proto.cylinder.radius == shape.radius
        elif isinstance(shape, AnnularCylinder):
            assert proto.annular_cylinder.start.x == shape.start.x
            assert proto.annular_cylinder.start.y == shape.start.y
            assert proto.annular_cylinder.start.z == shape.start.z
            assert proto.annular_cylinder.end.x == shape.end.x
            assert proto.annular_cylinder.end.y == shape.end.y
            assert proto.annular_cylinder.end.z == shape.end.z
            assert proto.annular_cylinder.radius == shape.radius
            assert proto.annular_cylinder.radius_inner == shape.radius_inner


def test_refinement_regions_duplicate_names() -> None:
    """Check that we can't have duplicate refinement region names."""
    refinement_region_a = lc.meshing.RefinementRegion(
        name="foo",
        h_limit=10,
        shape=Sphere(center=lc.types.Vector3(1, 2, 3), radius=4),
    )
    refinement_region_b = lc.meshing.RefinementRegion(
        name="foo",
        h_limit=10,
        shape=Sphere(center=lc.types.Vector3(1, 2, 3), radius=4),
    )

    mesh_params = lc.meshing.MeshGenerationParams(
        geometry_id="geometry-id",
        sizing_strategy=lc.meshing.sizing_strategy.MaxCount(5e6),
        refinement_regions=[refinement_region_a, refinement_region_b],
    )
    try:
        mesh_params._to_proto()
        assert False, "Expected ValueError for duplicate refinement region names"
    except ValueError as e:
        assert "Refinement region names must be unique" in str(e)
