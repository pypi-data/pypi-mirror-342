from __future__ import annotations
from .query import BaseQueryTypes
from .service import BaseServiceTypes
from .client import BaseClientTypes

class BaseTypes:
    Query = BaseQueryTypes
    Service = BaseServiceTypes
    Client = BaseClientTypes