from __future__ import annotations
from pydantic import model_validator
from typing import Any
from typing import Self
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_foundation.models.schemas.parameter import BaseParameterSchemas

class BaseClientParametersTransfers:
    class GetMultiple(
        BaseGeneralSchemas.SimplePagination,
        BaseParameterSchemas.SortColumns,
        BaseGeneralSchemas.Search,
        BaseGeneralSchemas.Statuses,
        BaseParameterSchemas.DateFilters,
        BaseGeneralSchemas.IDs,
    ):
        pass

    class GetMultipleQuery(
        BaseParameterSchemas.Sorts,
        BaseParameterSchemas.Filters,
        GetMultiple
    ):
        @model_validator(mode="after")
        def set_sort(self) -> Self:
            #* Process sort_columns parameters
            sort = []
            for item in self.sort_columns:
                sort.append(f"{item.name}.{item.order.value}")

            #* Only update if we have valid sort, otherwise keep the default
            if sort:
                self.sorts = sort

            return self

        @model_validator(mode="after")
        def set_filter(self) -> Self:
            #* Process filter parameters
            filter = []
            for item in self.date_filters:
                if item.from_date or item.to_date:
                    filter_string = item.name
                    if item.from_date:
                        filter_string += f"|from::{item.from_date.isoformat()}"
                    if item.to_date:
                        filter_string += f"|to::{item.to_date.isoformat()}"
                    filter.append(filter_string)

            #* Only update if we have valid filter, otherwise keep the default
            if filter:
                self.filters = filter

            return self
            
        def to_query_params(self) -> dict[str, Any]:
            params = {
                "page": self.page,
                "limit": self.limit,
                "search": self.search,
                "sorts": self.sorts,
                "filters": self.filters,
            }
            if hasattr(self, "statuses") and self.statuses is not None:
                params["statuses"] = self.statuses
            return params