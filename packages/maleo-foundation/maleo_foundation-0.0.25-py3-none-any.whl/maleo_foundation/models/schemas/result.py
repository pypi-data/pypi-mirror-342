from pydantic import BaseModel, Field
from typing import Literal, Optional, Any
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_foundation.models.types.general import BaseGeneralTypes

class BaseResultSchemas:
    class Base(BaseModel):
        success:bool = Field(..., description="Success status")
        code:BaseGeneralTypes.OptionalString = Field(None, description="Optional result code")
        message:BaseGeneralTypes.OptionalString = Field(None, description="Optional message")
        description:BaseGeneralTypes.OptionalString = Field(None, description="Optional description")
        data:Any = Field(..., description="Data")
        other:BaseGeneralTypes.OptionalAny = Field(None, description="Optional other information")

    #* ----- ----- ----- Intermediary ----- ----- ----- *#
    class Fail(Base):
        success:BaseGeneralTypes.LiteralFalse = Field(False, description="Success status")
        data:None = Field(None, description="No data")

    class Success(Base):
        success:BaseGeneralTypes.LiteralTrue = Field(True, description="Success status")
        data:Any = Field(..., description="Data")

    #* ----- ----- ----- Derived ----- ----- ----- *#
    class NoData(Success):
        data:None = Field(None, description="No data")

    class SingleData(Success):
        data:Any = Field(..., description="Fetched single data")

    class UnpaginatedMultipleData(Success):
        data:BaseGeneralTypes.ListOfAny = Field(..., description="Unpaginated multiple data")

    class PaginatedMultipleData(
        UnpaginatedMultipleData,
        BaseGeneralSchemas.SimplePagination
    ):
        total_data:int = Field(..., ge=0, description="Total data count")
        pagination:BaseGeneralSchemas.ExtendedPagination = Field(..., description="Pagination metadata")