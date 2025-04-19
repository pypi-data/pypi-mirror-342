from __future__ import annotations
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_foundation.models.transfers.results.service.query import BaseServiceQueryResultsTransfers

class MaleoMetadataServiceServiceQueryResultsTransfers:
    class Row(
        BaseGeneralSchemas.Name,
        BaseGeneralSchemas.Key,
        BaseGeneralSchemas.Order,
        BaseServiceQueryResultsTransfers.Row
    ): pass

    class Fail(BaseServiceQueryResultsTransfers.Fail): pass

    class NoData(BaseServiceQueryResultsTransfers.NoData): pass

    class SingleData(BaseServiceQueryResultsTransfers.SingleData):
        data:MaleoMetadataServiceServiceQueryResultsTransfers.Row

    class UnpaginatedMultipleData(BaseServiceQueryResultsTransfers.UnpaginatedMultipleData):
        data:list[MaleoMetadataServiceServiceQueryResultsTransfers.Row]

    class PaginatedMultipleData(BaseServiceQueryResultsTransfers.PaginatedMultipleData):
        data:list[MaleoMetadataServiceServiceQueryResultsTransfers.Row]