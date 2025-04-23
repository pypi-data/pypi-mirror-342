from __future__ import annotations
from .general import BaseGeneralClients
from .google import GoogleClients
from .utils import BaseClientUtils

class BaseClients:
    General = BaseGeneralClients
    Google = GoogleClients
    Utils = BaseClientUtils