# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
from pathlib import Path
from luminarycloud._helpers import util
import pytest


@pytest.fixture()
def cad_pipe_file_path(test_data_dir: Path) -> Path:
    return test_data_dir / "pipe.step"


def test_get_file_metadata(cad_pipe_file_path: Path) -> None:
    got = util.get_file_metadata(cad_pipe_file_path)

    assert got.name == "pipe"
    assert got.ext == "step"
    assert got.size == 8566
    assert (
        got.sha256_checksum
        == b"T\x1b\xf2+\x04\x9f\xe0\x14\xaa\x1d\xc8\x03ov\xc9m!F\x8cDS\x17\x14\x95\xc8y\x15\xa6\x9c4o\xbe"
    )
    # this is the known correct crc32c checksum of pipe.step (retrieved from the
    # DB, originally computed by the backend go code)
    assert got.crc32c_checksum == "q/7rCg=="
