from enum import Enum
from typing import Optional, List

from attr.converters import optional

from pytos2.models import Jsonable
from pytos2.utils import propify, prop

from netaddr import IPAddress


@propify
class JoinCloud(Jsonable):
    id: Optional[int] = prop(None, converter=optional(int))
    name: str = prop(None)
    clouds: List[int] = prop(factory=list)
