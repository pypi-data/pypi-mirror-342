from pydantic import BaseModel, Field
from typing import List, Optional
from maleo_metadata.enums.organization_role import MaleoMetadataOrganizationRoleEnums
from maleo_metadata.models.transfers.general.organization_role import OrganizationRoleTransfers

class MaleoMetadataOrganizationRoleSchemas:
    class OrganizationRole(BaseModel):
        organization_role:MaleoMetadataOrganizationRoleEnums.OrganizationRole = Field(..., description="Organization role")

    class OptionalOrganizationRole(BaseModel):
        organization_role:Optional[MaleoMetadataOrganizationRoleEnums.OrganizationRole] = Field(None, description="Organization role")

    class OrganizationRoles(BaseModel):
        organization_roles:List[MaleoMetadataOrganizationRoleEnums.OrganizationRole] = Field([], description="Organization roles")

    class OrganizationRoleDetails(BaseModel):
        organization_role_details:OrganizationRoleTransfers = Field(..., description="Organization role's details")

    class OptionalOrganizationRoleDetails(BaseModel):
        organization_role_details:Optional[MaleoMetadataOrganizationRoleEnums.OrganizationRole] = Field(None, description="Organization role's details")

    class OrganizationRolesDetails(BaseModel):
        organization_roles_details:List[OrganizationRoleTransfers] = Field([], description="Organization roles's details")