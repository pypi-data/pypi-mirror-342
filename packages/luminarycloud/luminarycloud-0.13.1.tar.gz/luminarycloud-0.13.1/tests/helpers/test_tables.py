# Copyright 2025 Luminary Cloud, Inc. All Rights Reserved.

import os
from tempfile import TemporaryDirectory

from luminarycloud.tables import create_rectilinear_table
from luminarycloud.enum import TableType


def test_table_conversion() -> None:
    with TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, "data.csv")
        with open(file_path, "w") as f:
            f.write(
                """Coord,Col 2,Bananas
            0,10,5
            1,,3
            3,3.14,-1"""
            )
        table = create_rectilinear_table(TableType.PROFILE_BC, file_path)

        assert table.header.axis_label[0].name == "Coord"
        assert table.header.record_label[0].name == "Col 2"
        assert table.header.record_label[1].name == "Bananas"

        assert table.axis[0].coordinate[0].adfloat.value == 0
        assert table.axis[0].coordinate[1].adfloat.value == 1
        assert table.axis[0].coordinate[2].adfloat.value == 3

        assert table.record[0].entry[0].adfloat.value == 10
        assert table.record[0].entry[1].HasField("empty")
        assert table.record[0].entry[2].adfloat.value == 3.14

        assert table.record[1].entry[0].adfloat.value == 5
        assert table.record[1].entry[1].adfloat.value == 3
        assert table.record[1].entry[2].adfloat.value == -1
