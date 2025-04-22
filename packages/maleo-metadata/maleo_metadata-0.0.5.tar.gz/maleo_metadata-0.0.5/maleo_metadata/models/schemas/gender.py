from pydantic import BaseModel, Field
from typing import Optional
from maleo_metadata.enums.gender import MaleoMetadataGenderEnums
from maleo_metadata.models.transfers.general.gender import GenderTransfers

class MaleoMetadataGenderSchemas:
    class Gender(BaseModel):
        gender:MaleoMetadataGenderEnums.Gender = Field(..., description="Gender")

    class OptionalGender(BaseModel):
        gender:Optional[MaleoMetadataGenderEnums.Gender] = Field(None, description="Gender")

    class GenderDetails(BaseModel):
        gender_details:GenderTransfers = Field(..., description="Gender's details")

    class OptionalGenderDetails(BaseModel):
        gender_details:Optional[MaleoMetadataGenderEnums.Gender] = Field(None, description="Gender's details")