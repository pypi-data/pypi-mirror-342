from pydantic import BaseModel, Field
from typing import List, Optional
from maleo_metadata.enums.user_type import MaleoMetadataUserTypeEnums
from maleo_metadata.models.transfers.general.user_type import UserTypeTransfers

class MaleoMetadataUserTypeExpandedSchemas:
    class SimpleUserType(BaseModel):
        user_type:MaleoMetadataUserTypeEnums.UserType = Field(..., description="User type")

    class OptionalSimpleUserType(BaseModel):
        user_type:Optional[MaleoMetadataUserTypeEnums.UserType] = Field(None, description="User type")

    class SimpleUserTypes(BaseModel):
        user_types:List[MaleoMetadataUserTypeEnums.UserType] = Field([], description="User types")

    class OptionalSimpleUserTypes(BaseModel):
        user_types:Optional[List[MaleoMetadataUserTypeEnums.UserType]] = Field(None, description="User types")

    class ExpandedUserType(BaseModel):
        user_type_details:UserTypeTransfers = Field(..., description="User type's details")

    class OptionalExpandedUserType(BaseModel):
        user_type_details:Optional[MaleoMetadataUserTypeEnums.UserType] = Field(None, description="User type's details")

    class ExpandedUserTypes(BaseModel):
        user_types_details:List[UserTypeTransfers] = Field([], description="User types's details")

    class OptionalExpandedUserTypes(BaseModel):
        user_types_details:Optional[List[MaleoMetadataUserTypeEnums.UserType]] = Field(None, description="User types's details")