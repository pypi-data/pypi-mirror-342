from __future__ import annotations
from .manager import MaleoMetadataHTTPClientManager
from .controllers import MaleoMetadataHTTPClientControllers

class MaleoMetadataHTTPClient:
    Manager = MaleoMetadataHTTPClientManager
    Controllers = MaleoMetadataHTTPClientControllers