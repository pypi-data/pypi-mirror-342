# Copyright 2025 Luminary Cloud, Inc. All Rights Reserved.

import pytest

from luminarycloud.types import Vector3, FirstOrderAdFloat


def test_vector3():
    vector3 = Vector3(1.0, 2.0, 3.0)
    ad_proto = vector3._to_ad_proto()
    assert ad_proto.x.value == 1.0
    assert ad_proto.y.value == 2.0
    assert ad_proto.z.value == 3.0

    vector3 = Vector3(
        FirstOrderAdFloat(1.0, (2.0,), (3.0,)),
        FirstOrderAdFloat(2.0, (3.0,), (4.0,)),
        FirstOrderAdFloat(3.0, (4.0,), (5.0,)),
    )
    ad_proto = vector3._to_ad_proto()
    assert ad_proto.x.first_order.value == 1.0
    assert ad_proto.x.first_order.tangent[0] == 2.0
    assert ad_proto.x.first_order.adjoint[0] == 3.0
    assert ad_proto.y.first_order.value == 2.0
    assert ad_proto.y.first_order.tangent[0] == 3.0
    assert ad_proto.y.first_order.adjoint[0] == 4.0
    assert ad_proto.z.first_order.value == 3.0
    assert ad_proto.z.first_order.tangent[0] == 4.0
    assert ad_proto.z.first_order.adjoint[0] == 5.0
