from pydantic import BaseModel, Field
from typing import List, Optional
from maleo_metadata.enums.organization_type import MaleoMetadataOrganizationTypeEnums
from maleo_metadata.models.transfers.general.organization_type import OrganizationTypeTransfers

class MaleoMetadataOrganizationTypeExpandedSchemas:
    class SimpleOrganizationType(BaseModel):
        organization_type:MaleoMetadataOrganizationTypeEnums.OrganizationType = Field(..., description="Organization type")

    class OptionalSimpleOrganizationType(BaseModel):
        organization_type:Optional[MaleoMetadataOrganizationTypeEnums.OrganizationType] = Field(None, description="Organization type")

    class SimpleOrganizationTypes(BaseModel):
        organization_types:List[MaleoMetadataOrganizationTypeEnums.OrganizationType] = Field([], description="Organization types")

    class OptionalSimpleOrganizationTypes(BaseModel):
        organization_types:Optional[List[MaleoMetadataOrganizationTypeEnums.OrganizationType]] = Field(None, description="Organization types")

    class ExpandedOrganizationType(BaseModel):
        organization_type_details:OrganizationTypeTransfers = Field(..., description="Organization type's details")

    class OptionalExpandedOrganizationType(BaseModel):
        organization_type_details:Optional[OrganizationTypeTransfers] = Field(None, description="Organization type's details")

    class ExpandedOrganizationTypes(BaseModel):
        organization_types_details:List[OrganizationTypeTransfers] = Field([], description="Organization types's details")

    class OptionalExpandedOrganizationTypes(BaseModel):
        organization_types_details:Optional[List[OrganizationTypeTransfers]] = Field(None, description="Organization types's details")