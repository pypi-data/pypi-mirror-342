from __future__ import annotations
from .general import MaleoMetadataServiceGeneralResultsTransfers
from .query import MaleoMetadataServiceQueryResultsTransfers

class MaleoMetadataServiceResultsTransfers:
    General = MaleoMetadataServiceGeneralResultsTransfers
    Query = MaleoMetadataServiceQueryResultsTransfers