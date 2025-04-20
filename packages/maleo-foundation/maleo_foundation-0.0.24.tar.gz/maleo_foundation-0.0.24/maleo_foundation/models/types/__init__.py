from __future__ import annotations
from .general import BaseGeneralTypes
from .parameter import BaseParameterTypes
from .query import BaseQueryTypes
from .service import BaseServiceTypes
from .client import BaseClientTypes

class BaseTypes:
    General = BaseGeneralTypes
    Parameter = BaseParameterTypes
    Query = BaseQueryTypes
    Service = BaseServiceTypes
    Client = BaseClientTypes