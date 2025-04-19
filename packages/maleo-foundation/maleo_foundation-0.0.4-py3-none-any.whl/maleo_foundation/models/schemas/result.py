from datetime import datetime, date
from pydantic import BaseModel, FieldSerializationInfo, Field, field_serializer, field_validator
from typing import Literal, Optional, Union, Any
from uuid import UUID
from maleo_foundation.models.enums import BaseEnums
from maleo_foundation.models.schemas.general import BaseGeneralSchemas

class BaseResultSchemas:
    class Identifiers(BaseModel):
        id:int = Field(..., ge=1, description="Data's ID, must be >= 1.")
        uuid:UUID = Field(..., description="Data's UUID.")

        @field_serializer('uuid')
        def serialize_uuid(self, value:UUID, info:FieldSerializationInfo) -> str:
            """Serializes UUID to a hex string."""
            return str(value)

    class Timestamps(BaseModel):
        created_at:datetime = Field(..., description="Data's created_at timestamp")
        updated_at:datetime = Field(..., description="Data's updated_at timestamp")
        deleted_at:Optional[datetime] = Field(..., description="Data's deleted_at timestamp")
        restored_at:Optional[datetime] = Field(..., description="Data's restored_at timestamp")
        deactivated_at:Optional[datetime] = Field(..., description="Data's deactivated_at timestamp")
        activated_at:datetime = Field(..., description="Data's activated_at timestamp")

        @field_serializer('created_at', 'updated_at', 'deleted_at', 'restored_at', 'deactivated_at', 'activated_at')
        def serialize_timestamps(self, value:Union[datetime, date], info:FieldSerializationInfo) -> str:
            """Serializes datetime/date fields to ISO format."""
            return value.isoformat()

    class Status(BaseModel):
        status:BaseEnums.StatusType = Field(..., description="Data's status")

    class Row(Status, Timestamps, Identifiers):
        @field_validator('*', mode="before")
        def set_none(cls, values):
            if isinstance(values, str) and (values == "" or len(values) == 0):
                return None
            return values
        
        @field_serializer('*')
        def serialize_fields(self, value, info:FieldSerializationInfo) -> Any:
            """Serializes all unique-typed fields."""
            if isinstance(value, UUID):
                return str(value)
            if isinstance(value, datetime) or isinstance(value, date):
                return value.isoformat()
            return value

        class Config:
            from_attributes=True

    #* ----- ----- ----- Base ----- ----- ----- *#
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
        total_data:int = Field(..., description="Total data count")
        pagination:BaseGeneralSchemas.ExtendedPagination = Field(..., description="Pagination metadata")