from __future__ import annotations
from .models import MaleoMetadataModels
from .clients import MaleoMetadataClients

class MaleoMetadataPackage:
    Models = MaleoMetadataModels
    Clients = MaleoMetadataClients