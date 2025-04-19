from datetime import date, datetime
from typing import Union, Optional, List

from requests import Response
from requests.exceptions import HTTPError

# avoid circular imports
import pytos2
from pytos2.api import ApiError
from pytos2.models import DateFilterType, coerce_date_filter_type  # noqa
from .api import SaAPI
from pytos2.utils import NoInstance, get_api_node
from .application_identities import ApplicationIdentity
from .applications import Application, ApplicationConnection
from .history import HistoryRecord
from pytos2.securechange.user import SCWUser
from pytos2.models import ObjectReference


class Sa:
    default: Union["Sa", NoInstance] = NoInstance(
        "Sa.default",
        "No Sa instance has been initialized yet, initialize with `Sa(*args, **kwargs)`",
    )

    def __init__(
        self,
        hostname: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        default=True,
    ):
        self.api: SaAPI = SaAPI(hostname, username, password)
        if default:
            Sa.default = self

        self._application_identities: List[ApplicationIdentity] = []

    @property
    def application_identities(self) -> List[ApplicationIdentity]:
        if not self._application_identities:
            res = self._get_application_identities()
            self._application_identities = res
        return self._application_identities

    def _get_application_identities(self, cache=True) -> List[ApplicationIdentity]:
        res = self.api.get_application_identities()
        data = self.api.handle_json(res, "application_identities")
        return [
            ApplicationIdentity.kwargify(a)
            for a in get_api_node(
                data, "application_identities.application_identity", listify=True
            )
        ]

    def get_applications(self) -> List[Application]:
        """
        This function returns a list of all applications in SecureApp.

        Method: GET
        URL: /securechangeworkflow/api/secureapp/repository/applications

        Usage:
            apps = sa.get_applications()
        """

        res = self.api.get_applications()
        data = self.api.handle_json(res, "get_applications")
        return [
            Application.kwargify(a)
            for a in get_api_node(data, "applications.application", listify=True)
        ]

    def get_application(self, application_id: str) -> Application:
        """
        This function returns a single application by its ID.

        Method: GET
        URL: /securechangeworkflow/api/secureapp/repository/applications/60

        Usage:
            app = sa.get_application(60)
        """

        res = self.api.get_application(application_id)
        data = self.api.handle_json(res, "get_application")
        application = get_api_node(data, "application")
        if isinstance(application, list) and application:
            application = application[0]

        return Application.kwargify(application)

    def add_application(
        self,
        name: Optional[str] = None,
        comment: Optional[str] = None,
        owner: Union[None, SCWUser, int, str] = None,
        editors: Optional[List[Union[SCWUser, int]]] = None,
        viewers: Optional[List[Union[SCWUser, int]]] = None,
        customer: Optional[
            int
        ] = None,  # TODO: Add customer to this once it's implemented.
    ):
        """
        This function creates a new application.

        Method: POST
        URL: /securechangeworkflow/api/secureapp/repository/applications

        Usage:
            Example 1:
            app = sa.add_application(name="My App", comment="This is my app")

            Example 2:
            app = sa.add_application(
                name="My App",
                owner=100,
                editors=[101, 102],
                viewers=[103, 104]
            )
        """

        from pytos2.securechange import Scw

        if isinstance(owner, str):
            owner = Scw.default.get_user(owner)
        if owner:
            owner = owner if isinstance(owner, int) else owner.id

        editors = editors or []
        viewers = viewers or []

        editors = [e if isinstance(e, int) else e.id for e in editors]
        viewers = [v if isinstance(v, int) else v.id for v in viewers]

        app = Application(
            name=name,
            comment=comment,
            owner=ObjectReference(id=owner) if owner else None,
            editors=[ObjectReference(id=e.id) for e in editors],
            viewers=[ObjectReference(id=v.id) for v in viewers],
            customer=ObjectReference(id=customer) if customer else None,
        )

        res = self.api.add_application(app._json)
        res = self.api.handle_response(res, "add_application")
        if res.status_code == 201:
            loc = res.headers.get("Location", "")
            new_app_id = loc.split("/")[-1]
            return self.get_application(new_app_id)
        else:
            # This should never happen, but just in case...
            raise ApiError(
                f"Failed to add application from status code: {res.status_code} and response: {res.text}"
            )  # noqa

    def update_application(
        self,
        application_id: Union[int, Application],
        name: Optional[str] = None,
        comment: Optional[str] = None,
        owner: Union[None, SCWUser, int] = None,
        editors: Optional[List[Union[SCWUser, int]]] = None,
        viewers: Optional[List[Union[SCWUser, int]]] = None,
    ):
        """
        This function updates an existing application.

        Method: PUT
        URL: /securechangeworkflow/api/secureapp/repository/applications/60

        Usage:
            Example 1:
            sa.update_application(60, name="My App", comment="This is my app")

            Example 2:
            sa.update_application(
                60,
                name="My App",
                owner=100,
                editors=[101, 102],
                viewers=[103, 104]
            )
        """
        if owner:
            owner = owner if isinstance(owner, int) else owner.id

        editors = (
            [e if isinstance(e, int) else e.id for e in editors] if editors else None
        )
        viewers = (
            [v if isinstance(v, int) else v.id for v in viewers] if viewers else None
        )

        if isinstance(application_id, Application):
            app = application_id
            application_id = app.id
        else:
            app = Application(
                name=name,
                comment=comment,
                owner=ObjectReference(id=owner) if owner else None,
                editors=(
                    [ObjectReference(id=e.id) for e in editors] if editors else None
                ),
                viewers=(
                    [ObjectReference(id=v.id) for v in viewers] if viewers else None
                ),
            )

        res = self.api.update_application(application_id, app._json)
        res = self.api.handle_response(res, "update_application")

    def delete_application(self, application_id: int):
        """
        This function deletes an application by its ID.

        Method: DELETE
        URL: /securechangeworkflow/api/secureapp/repository/applications/60

        Usage:
            sa.delete_application(60)
        """

        res = self.api.delete_application(application_id)
        self.api.handle_response(res, "delete_application")

    def bulk_update_applications(self, apps: List[Application]):
        res = self.api.update_applications([a._json for a in apps])
        self.api.handle_response(res, "bulk_update_applications")

    def get_application_connections(
        self, application_id: int
    ) -> List[ApplicationConnection]:
        """
        This function returns a list of all connections for a given application.

        Method: GET
        URL: /securechangeworkflow/api/secureapp/repository/applications/60/connections

        Usage:
            connections = sa.get_application_connections(60)
        """

        res = self.api.get_application_connections(application_id)
        data = self.api.handle_json(res, "get_application_connections")
        connections = get_api_node(data, "connections.connection", listify=True)
        return [ApplicationConnection.kwargify(c) for c in connections]

    def get_application_connection(
        self, application_id: int, connection_id: int
    ) -> ApplicationConnection:
        """
        This function returns a single connection for a given application.

        Method: GET
        URL: /securechangeworkflow/api/secureapp/repository/applications/60/connections/100

        Usage:
            connection = sa.get_application_connection(60, 100)
        """

        res = self.api.get_application_connection(application_id, connection_id)
        data = self.api.handle_json(res, "get_application_connection")
        conn = get_api_node(data, "connection")
        return ApplicationConnection.kwargify(conn)

    def get_application_history(
        self,
        application_id: int,
        start_date: DateFilterType = None,
        end_date: DateFilterType = None,
        count: Optional[int] = None,
        start: Optional[int] = None,
        type: Optional[str] = None,
        user: Optional[str] = None,
        show_members: Optional[bool] = None,
    ):
        """
        This function returns the history of a given application.

        Method: GET
        URL: /securechangeworkflow/api/secureapp/repository/applications/60/history

        Usage:
            history = sa.get_application_history(60)
        """

        start_date = coerce_date_filter_type(start_date)
        end_date = coerce_date_filter_type(end_date)

        res = self.api.get_application_history(
            application_id,
            start_date=start_date,
            end_date=end_date,
            count=count,
            start=start,
            type=type,
            user=user,
            show_members=show_members,
        )
        data = self.api.handle_json(res, "get_application_history")
        history = get_api_node(data, "history_records.history_record", listify=True)
        return [HistoryRecord.kwargify(h) for h in history]
