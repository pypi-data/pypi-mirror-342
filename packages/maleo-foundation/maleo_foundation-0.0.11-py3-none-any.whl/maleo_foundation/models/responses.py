from __future__ import annotations
from fastapi import status
from pydantic import Field, model_validator
from typing import Optional, Any
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_foundation.models.schemas.result import BaseResultSchemas

class BaseResponses:
    class Fail(BaseResultSchemas.Fail):
        other:Optional[Any] = Field("Please try again later or contact administrator.", description="Response's other information")

    class Unauthorized(Fail):
        code:str = "MAL-ATH-001"
        message:str = "Unauthorized Request"
        description:str = "You are unauthorized to request this resource"

    class Forbidden(Fail):
        code:str = "MAL-ATH-002"
        message:str = "Forbidden Request"
        description:str = "You are forbidden from requesting this resource"

    class NotFound(Fail):
        code:str = "MAL-NTF-001"
        message:str = "Not Found Error"
        description:str = "The resource you requested can not be found. Ensure your request is correct."

    class ValidationError(Fail):
        code:str = "MAL-VLD-001"
        message:str = "Validation Error"
        description:str = "Request validation failed due to missing or invalid fields. Check other for more info."

    class RateLimitExceeded(Fail):
        code:str = "MAL-RTL-001"
        message:str = "Rate Limit Exceeded"
        description:str = "This resource is requested too many times. Please try again later."

    class ServerError(Fail):
        code:str = "MAL-EXC-001"
        message:str = "Unexpected Server Error"
        description:str = "An unexpected error occurred while processing your request."

    class NoData(BaseResultSchemas.NoData): pass

    class SingleData(BaseResultSchemas.SingleData): pass

    class UnpaginatedMultipleData(BaseResultSchemas.UnpaginatedMultipleData): pass

    class PaginatedMultipleData(BaseResultSchemas.PaginatedMultipleData):
        @model_validator(mode="before")
        @classmethod
        def calculate_pagination(cls, values: dict) -> dict:
            """Calculates pagination metadata before validation."""
            total_data = values.get("total_data", 0)
            data = values.get("data", [])

            #* Get pagination values from inherited SimplePagination
            page = values.get("page", 1)
            limit = values.get("limit", 10)

            #* Calculate total pages
            total_pages = (total_data // limit) + (1 if total_data % limit > 0 else 0)

            #* Assign computed pagination object before validation
            values["pagination"] = BaseGeneralSchemas.ExtendedPagination(
                page=page,
                limit=limit,
                data_count=len(data),
                total_data=total_data,
                total_pages=total_pages
            )
            return values

    #* ----- ----- Responses Class ----- ----- *#
    other_responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthorized Response",
            "model": Unauthorized
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Forbidden Response",
            "model": Forbidden
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found Response",
            "model": NotFound
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation Error Response",
            "model": ValidationError
        },
        status.HTTP_429_TOO_MANY_REQUESTS: {
            "description": "Rate Limit Exceeded Response",
            "model": RateLimitExceeded
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal Server Error Response",
            "model": ServerError
        }
    }