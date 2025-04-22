from pydantic import BaseModel, Field
from typing import List, Optional
from maleo_metadata.enums.service import MaleoMetadataServiceEnums
from maleo_metadata.models.transfers.general.service import ServiceTransfers

class MaleoMetadataServiceExpandedSchemas:
    class SimpleService(BaseModel):
        service:MaleoMetadataServiceEnums.Service = Field(..., description="Service")

    class OptionalvService(BaseModel):
        service:Optional[MaleoMetadataServiceEnums.Service] = Field(None, description="Service")

    class SimpleServices(BaseModel):
        services:List[MaleoMetadataServiceEnums.Service] = Field([], description="Services")

    class OptionalSimpleServices(BaseModel):
        services:Optional[List[MaleoMetadataServiceEnums.Service]] = Field(None, description="Services")

    class ExpandedService(BaseModel):
        service_details:ServiceTransfers = Field(..., description="Service's details")

    class OptionalExpandedService(BaseModel):
        service_details:Optional[MaleoMetadataServiceEnums.Service] = Field(None, description="Service's details")

    class ExpandedServices(BaseModel):
        services_details:List[ServiceTransfers] = Field([], description="Services's details")

    class OptionalExpandedServices(BaseModel):
        services_details:Optional[List[MaleoMetadataServiceEnums.Service]] = Field(None, description="Services's details")