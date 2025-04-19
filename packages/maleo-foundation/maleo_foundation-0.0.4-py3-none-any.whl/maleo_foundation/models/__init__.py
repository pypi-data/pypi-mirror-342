from __future__ import annotations
from .enums import BaseEnums
from .schemas import BaseSchemas
from .transfers import BaseTransfers
from .responses import BaseResponses
from .types import BaseTypes

class BaseModels:
    Enums = BaseEnums
    Schemas = BaseSchemas
    Transfers = BaseTransfers
    Responses = BaseResponses
    Types = BaseTypes