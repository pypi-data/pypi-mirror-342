# Copyright 2023-2024 Luminary Cloud, Inc. All Rights Reserved.
from unittest.mock import MagicMock

import json
import pytest
import tempfile
from google.protobuf.json_format import Parse
from luminarycloud import (
    Project,
    SimulationTemplate,
    get_simulation_template,
)
from pathlib import Path
from luminarycloud._proto.client.simulation_pb2 import SimulationParam
from luminarycloud._proto.api.v0.luminarycloud.simulation_template import (
    simulation_template_pb2 as simtemplatepb,
)


@pytest.fixture()
def client_simulation_param_json_path(test_data_dir: Path) -> Path:
    return test_data_dir / "client_param_naca0012_inv.json"


@pytest.fixture()
def client_simulation_param(client_simulation_param_json_path: Path) -> bytes:
    with open(client_simulation_param_json_path, "rb") as fp:
        return Parse(fp.read(), SimulationParam())


def test_simulation_template_attr() -> None:
    simtemplate = SimulationTemplate(
        simtemplatepb.SimulationTemplate(
            id="simtemplate-id",
            name="name",
            parameters=SimulationParam(),
        )
    )
    assert simtemplate.id == "simtemplate-id"
    assert simtemplate.name == "name"
    assert isinstance(simtemplate.parameters, SimulationParam)


def test_get_simtemplate(mock_client: MagicMock) -> None:
    mock_client.GetSimulationTemplate.return_value = simtemplatepb.GetSimulationTemplateResponse(
        simulation_template=simtemplatepb.SimulationTemplate(),
    )
    got = get_simulation_template("simulation-id")
    assert isinstance(got, SimulationTemplate), "Did not get expected type of response"
    mock_client.GetSimulationTemplate.assert_called_with(
        simtemplatepb.GetSimulationTemplateRequest(id="simulation-id")
    )


def test_list_simtemplates(mock_client: MagicMock, project: Project) -> None:
    mock_client.ListSimulationTemplates.return_value = (
        simtemplatepb.ListSimulationTemplatesResponse(
            simulation_templates=[
                simtemplatepb.SimulationTemplate(),
                simtemplatepb.SimulationTemplate(),
            ],
        )
    )
    got = project.list_simulation_templates()
    assert len(got) == 2, "Did not get expected number of simulation templates"
    mock_client.ListSimulationTemplates.assert_called_with(
        simtemplatepb.ListSimulationTemplatesRequest(project_id="project-id")
    )


def test_update_simtemplate(
    mock_client: MagicMock, simulation_template: SimulationTemplate
) -> None:
    mock_client.UpdateSimulationTemplate.return_value = (
        simtemplatepb.UpdateSimulationTemplateResponse(
            simulation_template=simtemplatepb.SimulationTemplate(
                id="simtemplate-id",
                name="simtemplate-name",
            )
        )
    )
    simulation_template.update(name="simtemplate-name", parameters=SimulationParam())
    assert (
        simulation_template.name == "simtemplate-name"
    ), "simtemplate wrapper did not forward reply from mock client"
    mock_client.UpdateSimulationTemplate.assert_called_with(
        simtemplatepb.UpdateSimulationTemplateRequest(
            id="simtemplate-id",
            name="simtemplate-name",
            parameters=SimulationParam(),
        )
    )


def test_create_simtemplate(mock_client: MagicMock, project: Project) -> None:
    mock_client.CreateSimulationTemplate.return_value = (
        simtemplatepb.CreateSimulationTemplateResponse(
            simulation_template=simtemplatepb.SimulationTemplate(
                id="simtemplate-id",
                name="simtemplate-name",
            )
        )
    )
    params = SimulationParam()
    project.create_simulation_template(name="simtemplate-name", parameters=params)
    mock_client.CreateSimulationTemplate.assert_called_with(
        simtemplatepb.CreateSimulationTemplateRequest(
            project_id=project.id, name="simtemplate-name", parameters=params
        )
    )


def test_create_simconfig_from_json(
    mock_client: MagicMock,
    project: Project,
    client_simulation_param_json_path: Path,
    client_simulation_param: SimulationParam,
) -> None:
    mock_client.CreateSimulationTemplate.return_value = (
        simtemplatepb.CreateSimulationTemplateResponse(
            simulation_template=simtemplatepb.SimulationTemplate(
                id="simtemplate-id",
                name="simtemplate-name",
            )
        )
    )
    project.create_simulation_template(
        name="simtemplate-name",
        params_json_path=client_simulation_param_json_path,
    )
    mock_client.CreateSimulationTemplate.assert_called_with(
        simtemplatepb.CreateSimulationTemplateRequest(
            project_id=project.id, name="simtemplate-name", parameters=client_simulation_param
        )
    )


def test_create_simconfig_from_json_with_unknown_fields(
    mock_client: MagicMock,
    project: Project,
    client_simulation_param_json_path: Path,
    client_simulation_param: SimulationParam,
) -> None:
    with open(client_simulation_param_json_path, "rb") as fp:
        params_dict = json.load(fp)
        params_dict["unknown_field_B#K@(nf82)"] = 1

    with tempfile.NamedTemporaryFile(mode="w", delete=False) as fp:
        json.dump(params_dict, fp)
        fp.close()

        mock_client.CreateSimulationTemplate.return_value = (
            simtemplatepb.CreateSimulationTemplateResponse(
                simulation_template=simtemplatepb.SimulationTemplate(
                    id="simtemplate-id",
                    name="simtemplate-name",
                )
            )
        )
        project.create_simulation_template(
            name="simtemplate-name",
            params_json_path=fp.name,
        )

    mock_client.CreateSimulationTemplate.assert_called_with(
        simtemplatepb.CreateSimulationTemplateRequest(
            project_id=project.id, name="simtemplate-name", parameters=client_simulation_param
        )
    )


def test_delete_simtemplate(
    mock_client: MagicMock, simulation_template: SimulationTemplate
) -> None:
    simulation_template.delete()
    mock_client.DeleteSimulationTemplate.assert_called_with(
        simtemplatepb.DeleteSimulationTemplateRequest(
            id=simulation_template.id,
        )
    )
