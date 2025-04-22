from __future__ import annotations
from .formatter import BaseFormatter
from .logger import BaseLogger
from .exceptions import BaseExceptions

class BaseUtils:
    Formatter = BaseFormatter
    Logger = BaseLogger
    Exceptions = BaseExceptions