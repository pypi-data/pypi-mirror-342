# Copyright 2023 Luminary Cloud, Inc. All Rights Reserved.
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from luminarycloud._helpers import timestamp_to_datetime


def test_timestamp_to_datetime() -> None:
    want = datetime(2023, 7, 31, 13, 54, 12, 345678)
    timestamp = Timestamp(
        seconds=int(want.timestamp()),
        nanos=int(want.timestamp() * (10**9) % (10**9)),
    )
    got = timestamp_to_datetime(timestamp)
    assert got == want, "Did not get expected response"
