# Copyright 2023 Luminary Cloud, Inc. All Rights Reserved.
from pathlib import Path

import pytest


@pytest.fixture
def test_data_dir() -> Path:
    return Path(__file__).parents[1] / "testdata"
