from __future__ import annotations
from pydantic import BaseModel, Field
from maleo_foundation.enums import BaseEnums
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_foundation.types import BaseTypes

class BaseGeneralParametersTransfers:
    class GetSingleQuery(BaseGeneralSchemas.Statuses): pass

    class BaseGetSingle(
        BaseGeneralSchemas.IdentifierValue,
        BaseGeneralSchemas.IdentifierType
    ):
        pass

    class GetSingle(BaseGeneralSchemas.Statuses, BaseGetSingle): pass