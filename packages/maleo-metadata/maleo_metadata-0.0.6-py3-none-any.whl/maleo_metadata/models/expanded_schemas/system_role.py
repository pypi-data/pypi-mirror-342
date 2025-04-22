from pydantic import BaseModel, Field
from typing import Optional
from maleo_metadata.enums.system_role import MaleoMetadataSystemRoleEnums
from maleo_metadata.models.transfers.general.system_role import SystemRoleTransfers

class MaleoMetadataSystemRoleExpandedSchemas:
    class SystemRole(BaseModel):
        system_role:MaleoMetadataSystemRoleEnums.SystemRole = Field(..., description="System role")

    class OptionalSystemRole(BaseModel):
        system_role:Optional[MaleoMetadataSystemRoleEnums.SystemRole] = Field(None, description="System role")

    class SystemRoleDetails(BaseModel):
        system_role_details:SystemRoleTransfers = Field(..., description="System role's details")

    class OptionalSystemRoleDetails(BaseModel):
        system_role_details:Optional[MaleoMetadataSystemRoleEnums.SystemRole] = Field(None, description="System role's details")