from datetime import datetime
from enum import Enum

from typing import List, Optional

from ..utils import propify, prop, safe_iso8601_date, kwargify
from ..models import Jsonable, Link, ObjectReference


@propify
class ApplicationConnection(Jsonable):
    services: List[ObjectReference] = prop(flatify="service", factory=list)
    sources: List[ObjectReference] = prop(flatify="source", factory=list)
    destinations: List[ObjectReference] = prop(flatify="destination", factory=list)
    status: Optional[str] = prop(None)
    external: Optional[bool] = prop(None)
    connection_to_application: Optional[ObjectReference] = prop(None)
    comment: Optional[str] = prop(None)
    uid: Optional[str] = prop(None)
    application_id: Optional[str] = prop(None, key="applicationId")
    open_tickets: List[ObjectReference] = prop(flatify="ticket", factory=list)
    name: Optional[str] = prop(None)


@propify
class Application(Jsonable):
    class Meta(Enum):
        ROOT = "application"

    id: Optional[int] = prop(None)
    comment: Optional[str] = prop(None)
    customer: Optional[ObjectReference] = prop(None)
    status: Optional[str] = prop(None)
    vendors: List[str] = prop(flatify="vendor", factory=list, jsonify=False)
    created: Optional[datetime] = prop(None, kwargify=safe_iso8601_date, jsonify=False)
    connections: List[ObjectReference] = prop(
        flatify="connection", factory=list, jsonify=False
    )
    decommissioned: Optional[bool] = prop(None)
    editors: List[ObjectReference] = prop(factory=list)
    viewers: List[ObjectReference] = prop(factory=list)
    open_tickets: List[ObjectReference] = prop(factory=list, flatify="ticket")
    connection_to_application_packs: List[ObjectReference] = prop(
        factory=list, flatify="connection_to_application_pack", jsonify=False
    )
    name: str = prop()
    owner: Optional[ObjectReference] = prop(None)
    modified: Optional[datetime] = prop(None, kwargify=safe_iso8601_date, jsonify=False)
