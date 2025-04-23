# Copyright 2025 Luminary Cloud, Inc. All Rights Reserved.

import pytest

from luminarycloud.types.adfloat import (
    FirstOrderAdFloat,
    SecondOrderAdFloat,
    _from_ad_proto,
    _to_ad_proto,
)
from luminarycloud._proto.base.base_pb2 import AdFloatType


def test_adfloat() -> None:
    adfloat = SecondOrderAdFloat(
        FirstOrderAdFloat(1.0, (2.0,), (3.0,)),
        (FirstOrderAdFloat(2.0, (3.0,), (4.0,)),),
        (FirstOrderAdFloat(5.0, (6.0,), (7.0,)),),
    )
    assert adfloat == 1.0
    assert adfloat + 1.0 == 2
    assert 2.0 + adfloat == 3
    assert 2 == adfloat + 1
    assert 3 == 2 + adfloat
    assert 1.0 == adfloat
    assert isinstance(adfloat, float)
    assert isinstance(adfloat, SecondOrderAdFloat)
    assert not isinstance(adfloat, FirstOrderAdFloat)
    assert isinstance(adfloat.value, float)
    assert isinstance(adfloat.value, FirstOrderAdFloat)
    assert not isinstance(adfloat.value, SecondOrderAdFloat)
    assert adfloat.value.tangent[0] == 2.0
    assert adfloat.value.adjoint[0] == 3.0
    assert adfloat.tangent[0] == 2.0
    assert adfloat.tangent[0].tangent[0] == 3.0
    assert adfloat.adjoint[0] == 5.0
    assert adfloat.adjoint[0].adjoint[0] == 7.0
    assert not isinstance(float(adfloat), SecondOrderAdFloat)

    try:
        adfloat.value.tangent[0] = 2.0
        assert False, "AdFloats should be immutable"
    except TypeError:
        pass

    try:
        adfloat = SecondOrderAdFloat(1.0, [], [])
        assert False, "SecondOrderAdFloat should raise a TypeError if called with a regular float"
    except TypeError:
        pass


def test_adfloat_to_and_from_proto() -> None:
    # Check that a regular float converts to a value AdFloatType proto
    adfloat = 1.0
    adproto = _to_ad_proto(adfloat)
    assert isinstance(adproto, AdFloatType)
    assert adproto.HasField("value")
    assert adproto.value == adfloat
    assert _from_ad_proto(adproto) == adfloat

    # Check that a value AdFloatType proto converts to a regular float
    adfloat = _from_ad_proto(adproto)
    assert adfloat == 1.0
    assert isinstance(adfloat, float)
    assert not isinstance(adfloat, (FirstOrderAdFloat, SecondOrderAdFloat))

    # Check that a FirstOrderAdFloat converts to a FirstOrderAdType proto
    adfloat = FirstOrderAdFloat(1.0, (2.0,), (3.0,))
    adproto = _to_ad_proto(adfloat)
    assert isinstance(adproto, AdFloatType)
    assert adproto.HasField("first_order")
    assert adproto.first_order.value == 1.0
    assert adproto.first_order.tangent[0] == 2.0
    assert adproto.first_order.adjoint[0] == 3.0

    # Check that a FirstOrderAdType proto converts to a FirstOrderAdFloat
    adfloat = _from_ad_proto(adproto)
    assert adfloat == 1.0
    assert isinstance(adfloat, FirstOrderAdFloat)
    assert adfloat.tangent[0] == 2.0
    assert adfloat.adjoint[0] == 3.0

    # Check that a SecondOrderAdFloat converts to a SecondOrderAdType proto
    adfloat = SecondOrderAdFloat(
        FirstOrderAdFloat(1.0, (2.0,), (3.0,)),
        (FirstOrderAdFloat(2.0, (3.0,), (4.0,)),),
        (FirstOrderAdFloat(5.0, (6.0,), (7.0,)),),
    )
    adproto = _to_ad_proto(adfloat)
    assert isinstance(adproto, AdFloatType)
    assert adproto.HasField("second_order")
    assert adproto.second_order.value.value == 1.0
    assert adproto.second_order.value.tangent[0] == 2.0
    assert adproto.second_order.value.adjoint[0] == 3.0
    assert _from_ad_proto(adproto) == adfloat

    # Check that a SecondOrderAdType proto converts to a SecondOrderAdFloat
    adfloat = _from_ad_proto(adproto)
    assert adfloat == 1.0
    assert isinstance(adfloat, SecondOrderAdFloat)
    assert adfloat.value.tangent[0] == 2.0
    assert adfloat.value.adjoint[0] == 3.0
    assert adfloat.tangent[0] == 2.0
    assert adfloat.tangent[0].tangent[0] == 3.0
    assert adfloat.adjoint[0] == 5.0
    assert adfloat.adjoint[0].adjoint[0] == 7.0

    # Check that an empty AdFloatType proto (like x: {}) returns 0.0
    empty_proto = AdFloatType()
    result = _from_ad_proto(empty_proto)
    assert result == 0.0
