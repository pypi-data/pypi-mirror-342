# Copyright 2023-2024 Luminary Cloud, Inc. All Rights Reserved.
import luminarycloud as lc
from luminarycloud._proto.api.v0.luminarycloud.common import common_pb2 as commonpb


def test_vector3() -> None:
    vec3 = lc.types.Vector3(1, 2, 3)
    vec3_proto = vec3._to_proto()
    assert isinstance(vec3_proto, commonpb.Vector3)
    assert vec3_proto.x == vec3.x
    assert vec3_proto.y == vec3.y
    assert vec3_proto.z == vec3.z
