from datetime import datetime
from netaddr import IPAddress
import pytest
from pytos2.api import ApiError
import responses

from pytos2.secureapp.history import (
    HistoryConnectionBaseSnapshot,
    HistoryConnectionDetails,
)
from pytos2.securetrack.service_object import TCPServiceObject

from . import conftest  # noqa

from pytos2.secureapp.entrypoint import Sa
from pytos2.secureapp.application_identities import ApplicationIdentity
from dateutil.tz import tzoffset


class TestEntrypoint:
    @responses.activate
    def test_application_identities(self, sa: Sa, application_identities_mock):
        # print(dir(sa))
        identity = sa.application_identities[0]
        assert isinstance(identity, ApplicationIdentity)

    @responses.activate
    def test_application_identites_error(self, sa: Sa, failure_mock):
        with pytest.raises(ValueError):
            sa.application_identities

    @responses.activate
    def test_applications(self, sa: Sa, applications_mock):
        applications = sa.get_applications()
        assert applications[0].id == 60
        assert (
            applications[0].connections[0].link.href
            == "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/60/connections/126"
        )
        assert applications[0].owner and applications[0].owner.name == "r"

    @responses.activate
    def test_application(self, sa: Sa, applications_mock):
        application = sa.get_application(54)
        assert application.id == 54
        assert application.owner.name == "Jessica.Sanchez"
        assert (
            application.open_tickets[0].link.href
            == "https://198.18.0.1/securechangeworkflow/api/securechange/tickets/35"
        )

    @responses.activate
    def test_update_application(self, sa: Sa, applications_mock):
        responses.add(
            responses.PUT,
            "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/54",
            status=200,
            body="",
        )

        responses.add(
            responses.PUT,
            "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/1337",
            status=404,
            json={
                "result": {
                    "code": "NOT_FOUND_ERROR",
                    "message": "There is no application with the specified ID 1337.",
                }
            },
        )

        application = sa.get_application(54)
        application.name = "New Name"

        sa.update_application(application)
        with pytest.raises(ApiError):
            sa.update_application(1337, name="New Name")

        sa.update_application(54, name="New Name", owner=7)

    @responses.activate
    def test_create_application(self, scw, sa: Sa, applications_mock, users_mock):
        responses.add(
            responses.POST,
            "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications",
            status=201,
            headers={
                "Location": "https://198.18.0.1/securechange/api/secureapp/repository/applications/54"
            },
        )

        application = sa.add_application(
            name="VPN users access to RnD users", owner="r"
        )

        # Input and output don't really matter because we're mocking the response
        assert application.id == 54
        assert application.owner.name == "Jessica.Sanchez"
        assert application.name == "VPN users access to RnD users"

    @responses.activate
    def test_delete_application(self, sa: Sa, applications_mock):
        responses.add(
            responses.DELETE,
            "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/54",
            status=200,
            body="",
        )

        responses.add(
            responses.DELETE,
            "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/1337",
            status=404,
            json={
                "result": {
                    "code": "NOT_FOUND_ERROR",
                    "message": "There is no application with the specified ID 1337.",
                }
            },
        )

        sa.delete_application(54)

        with pytest.raises(ApiError):
            sa.delete_application(1337)

    @responses.activate
    def test_bulk_update_applications(self, sa: Sa, applications_mock):
        responses.add(
            responses.PUT,
            "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/",
            status=200,
            body="",
        )

        app = sa.get_application(54)

        sa.bulk_update_applications([app])

    @responses.activate
    def test_application_error(self, sa: Sa, failure_mock):
        with pytest.raises(ValueError):
            sa.get_application(54)

        with pytest.raises(ValueError):
            sa.get_applications()

    @responses.activate
    def test_application_connections(self, sa: Sa, application_connections_mock):
        connections = sa.get_application_connections(60)
        assert connections[0].id == 126
        assert connections[0].name == "Connection 1"
        assert connections[0].sources[0].name == "CRM_01"

    @responses.activate
    def test_application_connection(self, sa: Sa, application_connections_mock):
        connection = sa.get_application_connection(60, 126)
        assert connection.name == "Connection 1"
        assert connection.sources[0].name == "CRM_01"

    @responses.activate
    def test_application_connection_error(self, sa: Sa, failure_mock):
        with pytest.raises(ValueError):
            sa.get_application_connection(60, 126)

        with pytest.raises(ValueError):
            sa.get_application_connections(60)

    @responses.activate
    def test_application_history(self, sa: Sa, application_history_mock):
        history = sa.get_application_history(60)

        assert history[0].change_description == "Connection deleted"

        assert history[0].change_details.xsi_type.value == "historyConnectionDetailsDTO"
        assert isinstance(history[0].change_details, HistoryConnectionDetails)

        assert history[0].change_details.removed_sources[0].name == "Any"
        assert history[0].change_details.removed_sources[0].id == 1
        assert history[0].change_details.removed_sources[0].display_name == "Any"
        assert (
            history[0].change_details.removed_sources[0].link.href
            == "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/network_objects/1"
        )

        assert history[0].change_details.removed_destinations[0].name == "CRM_01"
        assert history[0].change_details.removed_destinations[0].id == 762
        assert (
            history[0].change_details.removed_destinations[0].display_name == "CRM_01"
        )
        assert (
            history[0].change_details.removed_destinations[0].link.href
            == "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/60/network_objects/762"
        )

        assert history[0].change_details.removed_services[0].name == "amitay2"
        assert history[0].change_details.removed_services[0].id == 235
        assert history[0].change_details.removed_services[0].display_name == "amitay2"
        assert (
            history[0].change_details.removed_services[0].link.href
            == "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/services/235"
        )

        assert history[0].date == datetime(
            2024, 4, 15, 3, 26, 57, 257000, tzinfo=tzoffset(None, -25200)
        )
        assert history[0].modified_object.display_name == "Connection 2"
        assert history[0].modified_object.id == 203
        assert (
            history[0].modified_object.link.href
            == "https://198.18.0.1/securechangeworkflow/api/secureapp/repository/applications/60/connections/203"
        )
        assert history[0].modified_object.name == "Connection 2"
        assert history[0].snapshot.comment == ""
        assert history[0].snapshot.id == 203
        assert history[0].snapshot.name == "Connection 2"

        assert isinstance(history[0].snapshot, HistoryConnectionBaseSnapshot)
        assert history[0].snapshot.xsi_type.value == "historyConnectionDTO"

        assert history[0].type == "Connection"
        assert history[0].user.display_name == "Henry Carr"
        assert history[0].user.id == 4
        assert (
            history[0].user.link.href
            == "https://198.18.0.1/securechangeworkflow/api/securechange/users/4"
        )
        assert history[0].user.name == "Henry Carr"

        assert "Connection changed" in history[3].change_description
        assert history[3].snapshot.id == 236
        assert history[3].snapshot.name == "Connection 3"
        assert history[3].snapshot.services[0].name == "http"
        assert isinstance(history[3].snapshot.services[0], TCPServiceObject)
        assert history[3].snapshot.services[0].min_port == 80
        assert history[3].snapshot.services[0].max_port == 80
        assert history[3].snapshot.services[0].protocol == 6

        assert history[3].snapshot.destinations[0].name == "CRM_01"
        assert history[3].snapshot.destinations[0].ip == IPAddress("192.168.205.33")

        # Covering empty case in find_in_detail_list
        assert history[4].change_details.removed_sources == []

        assert history[4].change_details.added_destinations[0].id == 3245
        assert history[4].change_details.added_destinations[0].name == "EDL_server2"
        assert (
            history[4].change_details.added_destinations[0].display_name
            == "EDL_server2"
        )

        assert history[5].change_details.added_services[0].id == 233
        assert history[5].change_details.added_services[0].name == "amitay5"

        assert history[11].change_details.added_sources[0].id == 3244
        assert history[11].change_details.added_sources[0].name == "EDL_subnet"

    @responses.activate
    def test_application_history_error(self, sa: Sa, failure_mock):
        with pytest.raises(ValueError):
            sa.get_application_history(60)
