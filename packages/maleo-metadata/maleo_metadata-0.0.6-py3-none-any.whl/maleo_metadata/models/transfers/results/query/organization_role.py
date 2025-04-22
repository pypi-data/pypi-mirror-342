from __future__ import annotations
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_foundation.models.transfers.results.service.query import BaseServiceQueryResultsTransfers

class MaleoMetadataOrganizationRoleQueryResultsTransfers:
    class Row(
        BaseGeneralSchemas.Name,
        BaseGeneralSchemas.Key,
        BaseGeneralSchemas.Order,
        BaseServiceQueryResultsTransfers.Row
    ): pass

    class Fail(BaseServiceQueryResultsTransfers.Fail): pass

    class NoData(BaseServiceQueryResultsTransfers.NoData): pass

    class SingleData(BaseServiceQueryResultsTransfers.SingleData):
        data:MaleoMetadataOrganizationRoleQueryResultsTransfers.Row

    class MultipleData(BaseServiceQueryResultsTransfers.UnpaginatedMultipleData):
        data:list[MaleoMetadataOrganizationRoleQueryResultsTransfers.Row]