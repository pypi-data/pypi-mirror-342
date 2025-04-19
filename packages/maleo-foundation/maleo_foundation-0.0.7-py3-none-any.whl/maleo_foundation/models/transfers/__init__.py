from __future__ import annotations
from .parameters import BaseParametersTransfers
from .results import BaseResultsTransfers

class BaseTransfers:
    Parameters = BaseParametersTransfers
    Results = BaseResultsTransfers