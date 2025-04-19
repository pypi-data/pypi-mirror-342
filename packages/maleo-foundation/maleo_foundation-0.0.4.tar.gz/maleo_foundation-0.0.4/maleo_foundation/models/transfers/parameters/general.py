from __future__ import annotations
from pydantic import Field
from typing import Union
from uuid import UUID
from maleo_foundation.models.enums import BaseEnums
from maleo_foundation.models.schemas.general import BaseGeneralSchemas

class BaseGeneralParametersTransfers:
    class GetSingleQuery(BaseGeneralSchemas.Statuses): pass

    class GetSingle(BaseGeneralSchemas.Statuses):
        identifier:BaseEnums.UniqueIdentifiers = Field(..., description="Identifier")
        value:Union[int, UUID] = Field(..., description="Value")