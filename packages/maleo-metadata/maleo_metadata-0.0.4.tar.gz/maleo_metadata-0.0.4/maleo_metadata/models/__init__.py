from __future__ import annotations
from .tables import MaleoMetadataTables
from .transfers import MaleoMetadataTransfers
from .responses import MaleoMetadataResponses

class MaleoMetadataModels:
    Tables = MaleoMetadataTables
    Transfers = MaleoMetadataTransfers
    Responses = MaleoMetadataResponses