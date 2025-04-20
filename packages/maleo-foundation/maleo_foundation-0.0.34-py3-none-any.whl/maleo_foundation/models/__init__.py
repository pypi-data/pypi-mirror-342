from __future__ import annotations
from .enums import BaseEnums
from .schemas import BaseSchemas
from .transfers import BaseTransfers
from .responses import BaseResponses
from .types import BaseTypes
from .extended_types import ExtendedTypes
from .expanded_types import ExpandedTypes

class BaseModels:
    Enums = BaseEnums
    Schemas = BaseSchemas
    Transfers = BaseTransfers
    Responses = BaseResponses
    Types = BaseTypes
    ExtendedTypes = ExtendedTypes
    ExpandedTypes = ExpandedTypes