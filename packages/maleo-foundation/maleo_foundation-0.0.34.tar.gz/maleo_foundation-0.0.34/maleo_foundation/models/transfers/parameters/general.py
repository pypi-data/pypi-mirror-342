from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.enums import BaseEnums
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_foundation.models.types import BaseTypes

class BaseGeneralParametersTransfers:
    class GetSingleQuery(BaseGeneralSchemas.Statuses): pass

    class GetSingle(BaseGeneralSchemas.Statuses):
        identifier:BaseEnums.UniqueIdentifiers = Field(..., description="Identifier")
        value:BaseTypes.IdentifierValue = Field(..., description="Value")