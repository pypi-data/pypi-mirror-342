# Copyright 2023-2024 Luminary Cloud, Inc. All Rights Reserved.
from pathlib import Path

import pytest


@pytest.fixture()
def client_simulation_param_json_path(test_data_dir: Path) -> Path:
    return test_data_dir / "client_param_naca0012_inv.json"


@pytest.fixture()
def client_simulation_param_json_bytes(client_simulation_param_json_path: Path) -> bytes:
    with open(client_simulation_param_json_path, "rb") as fp:
        params_json_bytes = fp.read()
    return params_json_bytes
