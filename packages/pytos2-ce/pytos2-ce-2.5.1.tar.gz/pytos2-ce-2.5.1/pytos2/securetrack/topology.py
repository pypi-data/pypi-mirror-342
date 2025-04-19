from typing import Optional

from pytos2.utils import propify, prop
from pytos2.models import Jsonable


@propify
class TopologySyncStatus(Jsonable):
    percentage: Optional[int] = prop(None)
    description: Optional[str] = prop(None)


@propify
class TopologyMode(Jsonable):
    domain_id: int = prop(None, key="domainId")
    device_id: int = prop(None, key="mgmtId")
    mode: str = prop("")  # Will be "DISABLED" or "ENABLED"
