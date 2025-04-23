from pydantic import BaseModel, Field
from typing import List, Optional
from maleo_metadata.enums.organization_role import MaleoMetadataOrganizationRoleEnums
from maleo_metadata.models.transfers.general.organization_role import OrganizationRoleTransfers

class MaleoMetadataOrganizationRoleExpandedSchemas:
    class SimpleOrganizationRole(BaseModel):
        organization_role:MaleoMetadataOrganizationRoleEnums.OrganizationRole = Field(..., description="Organization role")

    class OptionalSimpleOrganizationRole(BaseModel):
        organization_role:Optional[MaleoMetadataOrganizationRoleEnums.OrganizationRole] = Field(None, description="Organization role")

    class SimpleOrganizationRoles(BaseModel):
        organization_roles:List[MaleoMetadataOrganizationRoleEnums.OrganizationRole] = Field([], description="Organization roles")

    class OptionalSimpleOrganizationRoles(BaseModel):
        organization_roles:Optional[List[MaleoMetadataOrganizationRoleEnums.OrganizationRole]] = Field(None, description="Organization roles")

    class ExpandedOrganizationRole(BaseModel):
        organization_role_details:OrganizationRoleTransfers = Field(..., description="Organization role's details")

    class OptionalExpandedOrganizationRole(BaseModel):
        organization_role_details:Optional[OrganizationRoleTransfers] = Field(None, description="Organization role's details")

    class ExpandedOrganizationRoles(BaseModel):
        organization_roles_details:List[OrganizationRoleTransfers] = Field([], description="Organization roles's details")

    class OptionalExpandedOrganizationRoles(BaseModel):
        organization_roles_details:Optional[List[OrganizationRoleTransfers]] = Field(None, description="Organization roles's details")