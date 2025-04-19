from enum import Enum
from typing import Optional

from requests import HTTPError, JSONDecodeError

from pytos2.api import BaseAPI, get_app_api_session
from pytos2.utils import setup_logger


LOGGER = setup_logger("sa_api")


class SaAPI(BaseAPI):
    class Meta(Enum):
        PATH = "securechangeworkflow/api/secureapp"
        APP = "SCW"
        TOS2_ENV = "SC_SERVER_SERVICE"

    def __init__(
        self, hostname: Optional[str], username: Optional[str], password: Optional[str]
    ):
        self.hostname, self.username, self.password, session = get_app_api_session(
            app=self, hostname=hostname, username=username, password=password
        )

        super().__init__(session)

    def get_application_identities(self):
        return self.session.get("repository/application_identities")

    def get_applications(self):
        return self.session.get("repository/applications")

    def get_application(self, application_id):
        return self.session.get(f"repository/applications/{application_id}")

    def add_application(self, application):
        apps = [application] if not isinstance(application, list) else application

        r = self.session.post(
            "repository/applications", json={"applications": {"application": apps}}
        )
        return r

    def update_application(self, application_id, application):
        return self.session.put(
            f"repository/applications/{application_id}",
            json={"application": application},
        )

    def update_applications(self, applications):
        return self.session.put(
            "repository/applications/",
            json={"applications": {"application": applications}},
        )

    def delete_application(self, application_id):
        return self.session.delete(f"repository/applications/{application_id}")

    def get_application_connections(self, application_id):
        return self.session.get(f"repository/applications/{application_id}/connections")

    def get_application_connection(self, application_id, connection_id):
        r = self.session.get(
            f"repository/applications/{application_id}/connections/{connection_id}",
        )
        return r

    def get_application_history(
        self,
        application_id,
        start_date=None,
        end_date=None,
        count=None,
        start=None,
        type=None,
        user=None,
        show_members=None,
    ):
        return self.session.get(
            f"repository/applications/{application_id}/history",
            params={
                "start_date": start_date,
                "end_date": end_date,
                "count": count,
                "start": start,
                "type": type,
                "user": user,
                "showMembers": show_members,
            },
        )
