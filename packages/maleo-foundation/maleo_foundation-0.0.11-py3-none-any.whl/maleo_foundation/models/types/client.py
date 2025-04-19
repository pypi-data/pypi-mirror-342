from typing import Awaitable, Callable, Union
from maleo_foundation.models.transfers.parameters.general import BaseGeneralParametersTransfers
from maleo_foundation.models.transfers.parameters.client import BaseClientParametersTransfers
from maleo_foundation.models.transfers.results.client.service import BaseClientServiceResultsTransfers

class BaseClientTypes:
    GetMultipleParameter = BaseClientParametersTransfers.GetMultiple

    GetMultipleResult = Union[
        BaseClientServiceResultsTransfers.Fail,
        BaseClientServiceResultsTransfers.NoData,
        BaseClientServiceResultsTransfers.UnpaginatedMultipleData,
        BaseClientServiceResultsTransfers.PaginatedMultipleData
    ]

    SyncGetMultipleFunction = Callable[[GetMultipleParameter], GetMultipleResult]

    AsyncGetMultipleFunction = Callable[[GetMultipleParameter], Awaitable[GetMultipleResult]]

    GetSingleParameter = BaseGeneralParametersTransfers.GetSingle

    GetSingleResult = Union[
        BaseClientServiceResultsTransfers.Fail,
        BaseClientServiceResultsTransfers.NoData,
        BaseClientServiceResultsTransfers.SingleData
    ]

    SyncGetSingleFunction = Callable[[GetSingleParameter], GetSingleResult]

    AsyncGetSingleFunction = Callable[[GetSingleParameter], Awaitable[GetSingleResult]]

    CreateOrUpdateResult = Union[
        BaseClientServiceResultsTransfers.Fail,
        BaseClientServiceResultsTransfers.SingleData
    ]

    StatusUpdateResult = Union[
        BaseClientServiceResultsTransfers.Fail,
        BaseClientServiceResultsTransfers.SingleData
    ]