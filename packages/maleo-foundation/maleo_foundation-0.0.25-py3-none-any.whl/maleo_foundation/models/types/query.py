from typing import Awaitable, Callable, Union
from maleo_foundation.models.transfers.parameters.general import BaseGeneralParametersTransfers
from maleo_foundation.models.transfers.parameters.service import BaseServiceParametersTransfers
from maleo_foundation.models.transfers.results.service.query import BaseServiceQueryResultsTransfers

class BaseQueryTypes:
    GetMultipleParameter = BaseServiceParametersTransfers.GetMultiple

    GetMultipleResult = Union[
        BaseServiceQueryResultsTransfers.Fail,
        BaseServiceQueryResultsTransfers.NoData,
        BaseServiceQueryResultsTransfers.UnpaginatedMultipleData,
        BaseServiceQueryResultsTransfers.PaginatedMultipleData
    ]

    SyncGetMultipleFunction = Callable[[GetMultipleParameter], GetMultipleResult]

    AsyncGetMultipleFunction = Callable[[GetMultipleParameter], Awaitable[GetMultipleResult]]

    GetSingleParameter = BaseGeneralParametersTransfers.GetSingle

    GetSingleResult = Union[
        BaseServiceQueryResultsTransfers.Fail,
        BaseServiceQueryResultsTransfers.NoData,
        BaseServiceQueryResultsTransfers.SingleData
    ]

    SyncGetSingleFunction = Callable[[GetSingleParameter], GetSingleResult]

    AsyncGetSingleFunction = Callable[[GetSingleParameter], Awaitable[GetSingleResult]]

    CreateOrUpdateResult = Union[
        BaseServiceQueryResultsTransfers.Fail,
        BaseServiceQueryResultsTransfers.SingleData
    ]

    StatusUpdateResult = Union[
        BaseServiceQueryResultsTransfers.Fail,
        BaseServiceQueryResultsTransfers.SingleData
    ]