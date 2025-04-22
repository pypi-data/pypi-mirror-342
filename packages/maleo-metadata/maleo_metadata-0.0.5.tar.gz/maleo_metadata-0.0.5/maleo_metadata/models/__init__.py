from __future__ import annotations
from .tables import MaleoMetadataTables
from .transfers import MaleoMetadataTransfers
from .responses import MaleoMetadataResponses
from .schemas import MaleoMetadataSchemass

class MaleoMetadataModels:
    Tables = MaleoMetadataTables
    Transfers = MaleoMetadataTransfers
    Responses = MaleoMetadataResponses
    Schemas = MaleoMetadataSchemass