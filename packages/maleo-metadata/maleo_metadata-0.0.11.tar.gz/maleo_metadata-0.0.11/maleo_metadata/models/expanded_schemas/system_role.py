from pydantic import BaseModel, Field
from typing import List, Optional
from maleo_metadata.enums.system_role import MaleoMetadataSystemRoleEnums
from maleo_metadata.models.transfers.general.system_role import SystemRoleTransfers

class MaleoMetadataSystemRoleExpandedSchemas:
    class SimpleSystemRole(BaseModel):
        system_role:MaleoMetadataSystemRoleEnums.SystemRole = Field(..., description="System role")

    class OptionalSimpleSystemRole(BaseModel):
        system_role:Optional[MaleoMetadataSystemRoleEnums.SystemRole] = Field(None, description="System role")

    class SimpleSystemRoles(BaseModel):
        system_roles:List[MaleoMetadataSystemRoleEnums.SystemRole] = Field(..., description="System roles")

    class OptionalSimpleSystemRoles(BaseModel):
        system_roles:Optional[List[MaleoMetadataSystemRoleEnums.SystemRole]] = Field(None, description="System roles")

    class ExpandedSystemRole(BaseModel):
        system_role_details:SystemRoleTransfers = Field(..., description="System role's details")

    class OptionalExpandedSystemRole(BaseModel):
        system_role_details:Optional[MaleoMetadataSystemRoleEnums.SystemRole] = Field(None, description="System role's details")

    class ExpandedSystemRoles(BaseModel):
        system_roles_details:List[SystemRoleTransfers] = Field([], description="System roles's details")

    class OptionalExpandedSystemRoles(BaseModel):
        system_roles_details:Optional[List[MaleoMetadataSystemRoleEnums.SystemRole]] = Field(None, description="System role's details")