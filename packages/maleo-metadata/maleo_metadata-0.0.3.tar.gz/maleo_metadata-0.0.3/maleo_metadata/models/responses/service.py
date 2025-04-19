from pydantic import Field
from maleo_foundation.models.responses import BaseResponses
from maleo_metadata.models.transfers.general.service import ServiceTransfers

class MaleoMetadataServiceResponses:
    class GetMultiple(BaseResponses.PaginatedMultipleData):
        data:list[ServiceTransfers] = Field(..., description="Services")

    class GetSingle(BaseResponses.SingleData):
        data:ServiceTransfers = Field(..., description="service")