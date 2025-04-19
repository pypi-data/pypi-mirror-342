from __future__ import annotations
from datetime import date, datetime, timedelta, timezone
from pydantic import BaseModel, Field, model_validator, field_serializer, FieldSerializationInfo
from typing import Optional, Any
from uuid import UUID
from maleo_foundation.models.enums import BaseEnums
from maleo_foundation.constants import REFRESH_TOKEN_DURATION_DAYS, ACCESS_TOKEN_DURATION_MINUTES

class BaseGeneralSchemas:
    class IDs(BaseModel):
        ids:Optional[list[int]] = Field(None, description="Specific IDs")

    class Search(BaseModel):
        search:Optional[str] = Field(None, description="Search parameter string.")

    class DateFilter(BaseModel):
        name:str = Field(..., description="Column name.")
        from_date:Optional[datetime] = Field(None, description="From date.")
        to_date:Optional[datetime] = Field(None, description="To date.")

    class Statuses(BaseModel):
        statuses:Optional[list[BaseEnums.StatusType]] = Field(None, description="Data's status")

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
        expand:Optional[list[str]] = Field(None, description="Expanded field(s)")

    class PrivateKey(BaseModel):
        private_key:str = Field(..., description="Private key in str format.")

    class PublicKey(BaseModel):
        public_key:str = Field(..., description="Public key in str format.")

    class KeyPair(PublicKey, PrivateKey): pass

    class TokenPayload(BaseModel):
        t:BaseEnums.TokenType = Field(..., description="Token Type")
        sr:UUID = Field(..., description="System role")
        u:UUID = Field(..., description="user")
        o:Optional[UUID] = Field(..., description="Organization")
        uor:Optional[list[UUID]] = Field(..., description="User Organization Role")
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