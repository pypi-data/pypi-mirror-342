from pydantic import BaseModel, Field
from maleo_foundation.models.enums import BaseEnums
from maleo_foundation.models.schemas.general import BaseGeneralSchemas

class BaseParameterSchemas:
    class Filters(BaseModel):
        filters:list[str] = Field([], description="Filters for date range, e.g. 'created_at|from::<ISO_DATETIME>|to::<ISO_DATETIME>'.")

    class DateFilters(BaseModel):
        date_filters:list[BaseGeneralSchemas.DateFilter] = Field([], description="Date filters to be applied")

    class Sorts(BaseModel):
        sorts:list[str] = Field(["id.asc"], description="Sorting columns in 'column_name.asc' or 'column_name.desc' format.")

    class SortColumns(BaseModel):
        sort_columns:list[BaseGeneralSchemas.SortColumn] = Field([BaseGeneralSchemas.SortColumn(name="id", order=BaseEnums.SortOrder.ASC)], description="List of columns to be sorted")