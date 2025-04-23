from __future__ import annotations
from .http import MaleoMetadataHTTPClient
from .services import MaleoMetadataClientServices

class MaleoMetadataClients:
    HTTP = MaleoMetadataHTTPClient
    Services = MaleoMetadataClientServices