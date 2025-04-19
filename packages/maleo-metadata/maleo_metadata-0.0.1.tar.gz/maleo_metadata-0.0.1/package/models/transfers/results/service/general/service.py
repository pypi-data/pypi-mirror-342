from __future__ import annotations
from pydantic import Field
from maleo_foundation.models.transfers.results.service.general import BaseServiceGeneralResultsTransfers
from package.models.transfers.general.service import ServiceTransfers

class MaleoMetadataServiceServiceGeneralResultsTransfers:
    class Fail(BaseServiceGeneralResultsTransfers.Fail): pass

    class NoData(BaseServiceGeneralResultsTransfers.NoData): pass

    class SingleData(BaseServiceGeneralResultsTransfers.SingleData):
        data:ServiceTransfers = Field(..., description="Single service data")

    class UnpaginatedMultipleData(BaseServiceGeneralResultsTransfers.UnpaginatedMultipleData):
        data:list[ServiceTransfers] = Field(..., description="Multiple services data")

    class PaginatedMultipleData(BaseServiceGeneralResultsTransfers.PaginatedMultipleData):
        data:list[ServiceTransfers] = Field(..., description="Multiple services data")