from pydantic import BaseModel, Field
from typing import Optional
from maleo_metadata.enums.service import MaleoMetadataServiceEnums
from maleo_metadata.models.transfers.general.service import ServiceTransfers

class MaleoMetadataServiceExpandedSchemas:
    class Service(BaseModel):
        service:MaleoMetadataServiceEnums.Service = Field(..., description="Service")

    class OptionalService(BaseModel):
        service:Optional[MaleoMetadataServiceEnums.Service] = Field(None, description="Service")

    class ServiceDetails(BaseModel):
        service_details:ServiceTransfers = Field(..., description="Service's details")

    class OptionalServiceDetails(BaseModel):
        service_details:Optional[MaleoMetadataServiceEnums.Service] = Field(None, description="Service's details")