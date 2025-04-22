from pydantic import BaseModel, Field
from typing import Optional
from maleo_metadata.enums.organization_type import MaleoMetadataOrganizationTypeEnums
from maleo_metadata.models.transfers.general.organization_type import OrganizationTypeTransfers

class MaleoMetadataOrganizationTypeSchemas:
    class OrganizationType(BaseModel):
        organization_type:MaleoMetadataOrganizationTypeEnums.OrganizationType = Field(..., description="Organization type")

    class OptionalOrganizationType(BaseModel):
        organization_type:Optional[MaleoMetadataOrganizationTypeEnums.OrganizationType] = Field(None, description="Organization type")

    class OrganizationTypeDetails(BaseModel):
        organization_type_details:OrganizationTypeTransfers = Field(..., description="Organization type's details")

    class OptionalOrganizationTypeDetails(BaseModel):
        organization_type_details:Optional[MaleoMetadataOrganizationTypeEnums.OrganizationType] = Field(None, description="Organization type's details")