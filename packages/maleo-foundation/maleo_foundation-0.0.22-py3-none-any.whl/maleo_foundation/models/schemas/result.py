from pydantic import BaseModel, Field
from typing import Literal, Optional, Any
from maleo_foundation.models.schemas.general import BaseGeneralSchemas

class BaseResultSchemas:
    class Base(BaseModel):
        success:bool = Field(..., description="Success status")
        code:Optional[str] = Field(None, description="Optional result code")
        message:Optional[str] = Field(None, description="Optional message")
        description:Optional[str] = Field(None, description="Optional description")
        data:Any = Field(..., description="Data")
        other:Optional[Any] = Field(None, description="Optional other information")

    #* ----- ----- ----- Intermediary ----- ----- ----- *#
    class Fail(Base):
        success:Literal[False] = Field(False, description="Success status")
        data:None = Field(None, description="No data")

    class Success(Base):
        success:Literal[True] = Field(True, description="Success status")
        data:Any = Field(..., description="Data")

    #* ----- ----- ----- Derived ----- ----- ----- *#
    class NoData(Success):
        success:Literal[True] = Field(True, description="Success status")
        data:None = Field(None, description="No data")

    class SingleData(Success):
        success:Literal[True] = Field(True, description="Success status")
        data:Any = Field(..., description="Fetched single data")

    class UnpaginatedMultipleData(Success):
        success:Literal[True] = Field(True, description="Success status")
        data:list[Any] = Field(..., description="Unpaginated multiple data")

    class PaginatedMultipleData(
        UnpaginatedMultipleData,
        BaseGeneralSchemas.SimplePagination
    ):
        total_data:int = Field(..., ge=0, description="Total data count")
        pagination:BaseGeneralSchemas.ExtendedPagination = Field(..., description="Pagination metadata")