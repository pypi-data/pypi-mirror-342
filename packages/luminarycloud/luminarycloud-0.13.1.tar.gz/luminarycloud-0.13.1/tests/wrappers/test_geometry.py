# Copyright 2023-2024 Luminary Cloud, Inc. All Rights Reserved.
from unittest.mock import MagicMock

import luminarycloud as lc
from luminarycloud._proto.geometry import geometry_pb2 as gpb
from luminarycloud._proto.base import base_pb2 as basepb
from luminarycloud._proto.api.v0.luminarycloud.geometry import geometry_pb2 as geometrypb


def test_list_entities(mock_client: MagicMock) -> None:
    mock_client.ListGeometryEntities.return_value = geometrypb.ListGeometryEntitiesResponse(
        faces=[
            gpb.Face(
                id="0/bound/surface1",
                native_id=123,
                bbox_min=basepb.Vector3(x=0, y=0, z=0),
                bbox_max=basepb.Vector3(x=1, y=2, z=3),
            ),
            gpb.Face(
                id="0/bound/surface2",
                native_id=456,
                bbox_min=basepb.Vector3(x=-1, y=-2, z=-3),
                bbox_max=basepb.Vector3(x=0, y=0, z=0),
            ),
        ],
        bodies=[
            gpb.Body(
                id=890,
                lcn_id=0,
                bbox_min=basepb.Vector3(x=0, y=0, z=0),
                bbox_max=basepb.Vector3(x=1, y=2, z=3),
            ),
            gpb.Body(
                id=876,
                lcn_id=1,
                bbox_min=basepb.Vector3(x=-1, y=-2, z=-3),
                bbox_max=basepb.Vector3(x=0, y=0, z=0),
            ),
        ],
    )
    geometry = lc.Geometry(geometrypb.Geometry(id="test-geometry"))
    surfaces, volumes = geometry.list_entities()
    assert len(surfaces) == 2
    assert isinstance(surfaces[0], lc.params.geometry.Surface)
    assert surfaces[0].id == "0/bound/surface1"
    assert surfaces[0]._native_id == 123
    assert len(volumes) == 2
    assert isinstance(volumes[0], lc.params.geometry.Volume)
    assert volumes[0].id == "890"
    assert volumes[0]._lcn_id == "0"
    mock_client.ListGeometryEntities.assert_called_with(
        geometrypb.ListGeometryEntitiesRequest(geometry_id=geometry.id)
    )


def test_create_tag(mock_client: MagicMock) -> None:
    geometry = lc.Geometry(geometrypb.Geometry(id="test-geometry"))
    geometry.create_tag(
        "tag-example",
        [
            lc.params.geometry.Surface(
                geometry_id=geometry.id,
                id="0/bound/surface1",
                bbox_min=lc.types.Vector3(x=0, y=0, z=0),
                bbox_max=lc.types.Vector3(x=1, y=2, z=3),
                _native_id=123,
            ),
            lc.params.geometry.Volume(
                geometry_id=geometry.id,
                id="890",
                bbox_min=lc.types.Vector3(x=0, y=0, z=0),
                bbox_max=lc.types.Vector3(x=1, y=2, z=3),
                _lcn_id="0",
            ),
        ],
    )
    mock_client.ModifyGeometry.assert_called_with(
        geometrypb.ModifyGeometryRequest(
            geometry_id=geometry.id,
            modification=gpb.Modification(
                mod_type=gpb.Modification.MODIFICATION_TYPE_CREATE_TAG,
                create_or_update_tag=gpb.CreateOrUpdateTag(
                    name="tag-example",
                    bodies=[890],
                    faces=[123],
                ),
            ),
        )
    )
