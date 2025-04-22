from pydantic import BaseModel, Field
from typing import Optional
from maleo_metadata.enums.user_type import MaleoMetadataUserTypeEnums
from maleo_metadata.models.transfers.general.user_type import UserTypeTransfers

class MaleoMetadataUserTypeExpandedSchemas:
    class UserType(BaseModel):
        user_type:MaleoMetadataUserTypeEnums.UserType = Field(..., description="User type")

    class OptionalUserType(BaseModel):
        user_type:Optional[MaleoMetadataUserTypeEnums.UserType] = Field(None, description="User type")

    class UserTypeDetails(BaseModel):
        user_type_details:UserTypeTransfers = Field(..., description="User type's details")

    class OptionalUserTypeDetails(BaseModel):
        user_type_details:Optional[MaleoMetadataUserTypeEnums.UserType] = Field(None, description="User type's details")