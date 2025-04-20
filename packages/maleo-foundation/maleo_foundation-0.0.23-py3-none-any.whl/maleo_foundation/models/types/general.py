from datetime import datetime
from typing import Optional, Union, Literal, List, Any
from uuid import UUID
from maleo_foundation.models.enums import BaseEnums
from maleo_foundation.models.schemas.general import BaseGeneralSchemas

class BaseGeneralTypes:
    #* Any-related types
    ListOfAny = List[Any]
    OptionalAny = Optional[Any]

    #* Boolean-related types
    LiteralFalse = Literal[False]
    LiteralTrue = Literal[True]

    #* Float-related types
    ListOfFloats = List[float]
    OptionalFloat = Optional[float]
    OptionalListOfFloats = Optional[List[float]]

    #* Integer-related types
    ListOfIntegers = List[int]
    OptionalInteger = Optional[int]
    OptionalListOfIntegers = Optional[List[int]]

    #* String-related types
    ListOfStrings = List[str]
    OptionalString = Optional[str]
    OptionalListOfStrings = Optional[List[str]]

    #* Datetime-related types
    OptionalDatetime = Optional[datetime]

    #* UUID-related types
    ListOfUUIDs = List[UUID]
    OptionalUUID = Optional[UUID]
    OptionalListOfUUIDs = Optional[List[UUID]]

    #* Statuses-related types
    ListOfStatuses = List[BaseEnums.StatusType]
    OptionalListOfStatuses = Optional[List[BaseEnums.StatusType]]

    #* DateFilter-related types
    ListOfDateFilters = List[BaseGeneralSchemas.DateFilter]

    #* SortColumn-related types
    ListOfSortColumns = List[BaseGeneralSchemas.SortColumn]

    #* Miscellanous types
    IdentifierValue = Union[int, UUID, str]