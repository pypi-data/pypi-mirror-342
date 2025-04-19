import json
import re

import pytest  # type: ignore
import responses

from pytos2.secureapp import SaAPI
from pytos2.secureapp.entrypoint import Sa

from tests.securechange.conftest import users_mock, scw


@pytest.fixture
def sa_api():
    return SaAPI(username="username", password="password", hostname="198.18.0.1")


@pytest.fixture
def sa():
    return Sa(username="username", password="password", hostname="198.18.0.1")


@pytest.fixture
def application_identities_mock():
    application_identities_json = json.load(
        open("tests/secureapp/json/application_identities.json")
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/application_identities",
        json=application_identities_json,
    )


@pytest.fixture
def failure_mock():
    responses.add(
        responses.GET,
        re.compile("https://198.18.0.1/securechangeworkflow/api/secureapp.*"),
        status=500,
    )


@pytest.fixture
def applications_mock():
    applications_json = json.load(open("tests/secureapp/json/applications.json"))
    application_54_json = json.load(open("tests/secureapp/json/application_54.json"))

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications",
        json=applications_json,
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/54",
        json=application_54_json,
    )


@pytest.fixture
def application_connections_mock():
    application_connections_json = json.load(
        open("tests/secureapp/json/app_60_connections.json")
    )

    application_connection_126_json = json.load(
        open("tests/secureapp/json/app_60_connection_126.json")
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/60/connections",
        json=application_connections_json,
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/60/connections/126",
        json=application_connection_126_json,
    )


@pytest.fixture
def application_history_mock():
    application_history_json = json.load(
        open("tests/secureapp/json/app_60_history.json")
    )

    responses.add(
        responses.GET,
        "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/60/history",
        json=application_history_json,
    )
