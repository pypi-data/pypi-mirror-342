from typing import Awaitable, Callable, Union
from maleo_foundation.models.transfers.parameters.general import BaseGeneralParametersTransfers
from maleo_foundation.models.transfers.parameters.service import BaseServiceParametersTransfers
from maleo_foundation.models.transfers.results.service.general import BaseServiceGeneralResultsTransfers

class BaseServiceTypes:
    GetMultipleParameter = BaseServiceParametersTransfers.GetMultiple

    GetMultipleResult = Union[
        BaseServiceGeneralResultsTransfers.Fail,
        BaseServiceGeneralResultsTransfers.NoData,
        BaseServiceGeneralResultsTransfers.UnpaginatedMultipleData,
        BaseServiceGeneralResultsTransfers.PaginatedMultipleData
    ]

    SyncGetMultipleFunction = Callable[[GetMultipleParameter], GetMultipleResult]

    AsyncGetMultipleFunction = Callable[[GetMultipleParameter], Awaitable[GetMultipleResult]]

    GetSingleParameter = BaseGeneralParametersTransfers.GetSingle

    GetSingleResult = Union[
        BaseServiceGeneralResultsTransfers.Fail,
        BaseServiceGeneralResultsTransfers.NoData,
        BaseServiceGeneralResultsTransfers.SingleData
    ]

    SyncGetSingleFunction = Callable[[GetSingleParameter], GetSingleResult]

    AsyncGetSingleFunction = Callable[[GetSingleParameter], Awaitable[GetSingleResult]]

    CreateOrUpdateResult = Union[
        BaseServiceGeneralResultsTransfers.Fail,
        BaseServiceGeneralResultsTransfers.SingleData
    ]

    StatusUpdateResult = Union[
        BaseServiceGeneralResultsTransfers.Fail,
        BaseServiceGeneralResultsTransfers.SingleData
    ]