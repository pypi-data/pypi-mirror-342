from __future__ import annotations
import re
import urllib.parse
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, Self, Any
from maleo_foundation.models.enums import BaseEnums
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_foundation.models.schemas.parameter import BaseParameterSchemas
from maleo_foundation.constants import SORT_COLUMN_PATTERN, DATE_FILTER_PATTERN

class BaseServiceParametersTransfers:
    class GetMultipleQuery(
        BaseParameterSchemas.Filters,
        BaseParameterSchemas.Sorts,
        BaseGeneralSchemas.Search,
        BaseGeneralSchemas.SimplePagination,
        BaseGeneralSchemas.Statuses
    ):
        @field_validator("sort")
        @classmethod
        def validate_sort_columns(cls, values):
            if not isinstance(values, list):
                return ["id.asc"]
            return [value for value in values if SORT_COLUMN_PATTERN.match(value)]

        @field_validator("filter")
        @classmethod
        def validate_date_filters(cls, values):
            if isinstance(values, list):
                decoded_values = [urllib.parse.unquote(value) for value in values]
                #* Replace space followed by 2 digits, colon, 2 digits with + and those digits
                fixed_values = []
                for value in decoded_values:
                    #* Look for the pattern: space followed by 2 digits, colon, 2 digits
                    fixed_value = re.sub(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+) (\d{2}:\d{2})', r'\1+\2', value)
                    fixed_values.append(fixed_value)
                final_values = [value for value in fixed_values if DATE_FILTER_PATTERN.match(value)]
                return final_values

    class GetMultiple(
        BaseParameterSchemas.DateFilters,
        BaseParameterSchemas.SortColumns,
        GetMultipleQuery
    ):
        @model_validator(mode="after")
        def set_sort_columns(self) -> Self:
            #* Process sort parameters
            sort_columns = []
            for item in self.sorts:
                parts = item.split('.')
                if len(parts) == 2 and parts[1].lower() in ["asc", "desc"]:
                    try:
                        sort_columns.append(BaseGeneralSchemas.SortColumn(name=parts[0], order=BaseEnums.SortOrder(parts[1].lower())))
                    except ValueError:
                        continue

            #* Only update if we have valid sort columns, otherwise keep the default
            if sort_columns:
                self.sort_columns = sort_columns
            return self

        @model_validator(mode="after")
        def set_date_filters(self) -> Self:
            #* Process filter parameters
            date_filters = []
            for filter_item in self.filters:
                parts = filter_item.split('|')
                if len(parts) >= 2 and parts[0]:
                    name = parts[0]
                    from_date = None
                    to_date = None

                    #* Process each part to extract from and to dates
                    for part in parts[1:]:
                        if part.startswith('from::'):
                            try:
                                from_date_str = part.replace('from::', '')
                                from_date = datetime.fromisoformat(from_date_str)
                            except ValueError:
                                continue
                        elif part.startswith('to::'):
                            try:
                                to_date_str = part.replace('to::', '')
                                to_date = datetime.fromisoformat(to_date_str)
                            except ValueError:
                                continue

                    #* Only add filter if at least one date is specified
                    if from_date or to_date:
                        date_filters.append(BaseGeneralSchemas.DateFilter(name=name, from_date=from_date, to_date=to_date))

            #* Update date_filters
            self.date_filters = date_filters
            return self

    class UniqueFieldCheck(BaseModel):
        operation:BaseEnums.OperationType = Field(..., description="Operation to be conducted")
        field:BaseEnums.UniqueIdentifiers = Field(..., description="Field to be checked")
        new_value:Optional[Any] = Field(..., description="New field's value")
        old_value:Optional[Any] = Field(None, description="Old field's value")
        nullable:bool = Field(False, description="Whether to allow null field's value")
        suggestion:Optional[str] = Field(None, description="Suggestion on discrepancy")

    UniqueFieldChecks = list[UniqueFieldCheck]

    status_update_criterias:dict[
        BaseEnums.StatusUpdateAction,
        Optional[list[BaseEnums.StatusType]]
    ] = {
        BaseEnums.StatusUpdateAction.DELETE: None,
        BaseEnums.StatusUpdateAction.RESTORE: None,
        BaseEnums.StatusUpdateAction.DEACTIVATE: [
            BaseEnums.StatusType.INACTIVE,
            BaseEnums.StatusType.ACTIVE,
        ],
        BaseEnums.StatusUpdateAction.ACTIVATE: [
            BaseEnums.StatusType.INACTIVE,
            BaseEnums.StatusType.ACTIVE,
        ]
    }