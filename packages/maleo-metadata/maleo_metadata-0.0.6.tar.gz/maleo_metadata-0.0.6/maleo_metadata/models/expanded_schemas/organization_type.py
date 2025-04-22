from pydantic import BaseModel, Field
from typing import Optional
from maleo_metadata.enums.organization_type import MaleoMetadataOrganizationTypeEnums
from maleo_metadata.models.transfers.general.organization_type import OrganizationTypeTransfers

class MaleoMetadataOrganizationTypeExpandedSchemas:
    class SimpleOrganizationType(BaseModel):
        organization_type:MaleoMetadataOrganizationTypeEnums.OrganizationType = Field(..., description="Organization type")

    class OptionalSimpleOrganizationType(BaseModel):
        organization_type:Optional[MaleoMetadataOrganizationTypeEnums.OrganizationType] = Field(None, description="Organization type")

    class ExpandedOrganizationType(BaseModel):
        organization_type_details:OrganizationTypeTransfers = Field(..., description="Organization type's details")

    class OptionalExpandedOrganizationType(BaseModel):
        organization_type_details:Optional[OrganizationTypeTransfers] = Field(None, description="Organization type's details")