from __future__ import annotations
from datetime import date, datetime, timedelta, timezone
from pydantic import BaseModel, Field, model_validator, field_serializer, FieldSerializationInfo
from typing import Any
from uuid import UUID
from maleo_foundation.constants import REFRESH_TOKEN_DURATION_DAYS, ACCESS_TOKEN_DURATION_MINUTES
from maleo_foundation.enums import BaseEnums
from maleo_foundation.types import BaseTypes

class BaseGeneralSchemas:
    class IdentifierType(BaseModel):
        identifier:BaseEnums.IdentifierTypes = Field(..., description="Data's identifier type")

    class IdentifierValue(BaseModel):
        value:BaseTypes.IdentifierValue = Field(..., description="Data's identifier value")

    class Ids(BaseModel):
        ids:BaseTypes.OptionalListOfIntegers = Field(None, description="Specific Ids")

    class Search(BaseModel):
        search:BaseTypes.OptionalString = Field(None, description="Search parameter string.")

    class DateFilter(BaseModel):
        name:str = Field(..., description="Column name.")
        from_date:BaseTypes.OptionalDatetime = Field(None, description="From date.")
        to_date:BaseTypes.OptionalDatetime = Field(None, description="To date.")

    class Statuses(BaseModel):
        statuses:BaseTypes.OptionalListOfStatuses = Field(None, description="Data's status")

    class SortColumn(BaseModel):
        name:str = Field(..., description="Column name.")
        order:BaseEnums.SortOrder = Field(..., description="Sort order.")

    class SimplePagination(BaseModel):
        page:int = Field(1, ge=1, description="Page number, must be >= 1.")
        limit:int = Field(10, ge=1, le=100, description="Page size, must be 1 <= limit <= 100.")

    class ExtendedPagination(SimplePagination):
        data_count:int = Field(..., description="Fetched data count")
        total_data:int = Field(..., description="Total data count")
        total_pages:int = Field(..., description="Total pages count")

    class StatusUpdate(BaseModel):
        action:BaseEnums.StatusUpdateAction = Field(..., description="Status update's action to be executed")

    class Expand(BaseModel):
        expand:BaseTypes.OptionalListOfStrings = Field(None, description="Expanded field(s)")

    class PrivateKey(BaseModel):
        private_key:str = Field(..., description="Private key in str format.")

    class PublicKey(BaseModel):
        public_key:str = Field(..., description="Public key in str format.")

    class KeyPair(PublicKey, PrivateKey): pass

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
        deleted_at:BaseTypes.OptionalDatetime = Field(..., description="Data's deleted_at timestamp")
        restored_at:BaseTypes.OptionalDatetime = Field(..., description="Data's restored_at timestamp")
        deactivated_at:BaseTypes.OptionalDatetime = Field(..., description="Data's deactivated_at timestamp")
        activated_at:datetime = Field(..., description="Data's activated_at timestamp")

        @field_serializer('created_at', 'updated_at', 'deleted_at', 'restored_at', 'deactivated_at', 'activated_at')
        def serialize_timestamps(self, value:BaseTypes.OptionalDatetime, info:FieldSerializationInfo) -> str:
            """Serializes datetime/date fields to ISO format."""
            if value is not None:
                return value.isoformat()
            return value

    class Status(BaseModel):
        status:BaseEnums.StatusType = Field(..., description="Data's status")

    class Order(BaseModel):
        order:BaseTypes.OptionalInteger = Field(..., description="Data's order")

    class Key(BaseModel):
        key:str = Field(..., description="Data's key")

    class Name(BaseModel):
        name:str = Field(..., description="Data's name")

    class Secret(BaseModel):
        secret:UUID = Field(..., description="Data's secret")

    class TokenPayload(BaseModel):
        t:BaseEnums.TokenType = Field(..., description="Token Type")
        sr:UUID = Field(..., description="System role")
        u:UUID = Field(..., description="user")
        o:BaseTypes.OptionalUUID = Field(..., description="Organization")
        uor:BaseTypes.OptionalListOfUUIDs = Field(..., description="User Organization Role")
        iat_dt:datetime = Field(datetime.now(timezone.utc), description="Issued at (datetime)")
        iat:int = Field(None, description="Issued at (integer)")
        exp_dt:datetime = Field(None, description="Expired at (datetime)")
        exp:int = Field(None, description="Expired at (integet)")

        @model_validator(mode="before")
        @classmethod
        def set_iat_and_exp(cls, values:dict):
            iat_dt = values.get("iat_dt", None)
            if not iat_dt:
                iat_dt = datetime.now(timezone.utc)
            else:
                if not isinstance(iat_dt, datetime):
                    iat_dt = datetime.fromisoformat(iat_dt)
            values["iat_dt"] = iat_dt
            #* Convert `iat` to timestamp (int)
            values["iat"] = int(iat_dt.timestamp())
            exp_dt = values.get("exp_dt", None)
            if not exp_dt:
                if values["t"] == BaseEnums.TokenType.REFRESH:
                    exp_dt = iat_dt + timedelta(days=REFRESH_TOKEN_DURATION_DAYS)
                elif values["t"] == BaseEnums.TokenType.ACCESS:
                    exp_dt = iat_dt + timedelta(minutes=ACCESS_TOKEN_DURATION_MINUTES)
            else:
                if not isinstance(exp_dt, datetime):
                    exp_dt = datetime.fromisoformat(exp_dt)
            values["exp_dt"] = exp_dt
            #* Convert `exp_dt` to timestamp (int)
            values["exp"] = int(exp_dt.timestamp())
            return values
        
        @field_serializer('*')
        def serialize_fields(self, value, info: FieldSerializationInfo) -> Any:
            """Recursively serialize UUIDs, datetimes, and dates in complex structures."""

            def serialize(v: Any) -> Any:
                if isinstance(v, UUID):
                    return str(v)
                if isinstance(v, (datetime, date)):
                    return v.isoformat()
                if isinstance(v, list):
                    return [serialize(item) for item in v]
                if isinstance(v, tuple):
                    return tuple(serialize(item) for item in v)
                if isinstance(v, dict):
                    return {serialize(k): serialize(val) for k, val in v.items()}
                return v

            return serialize(value)