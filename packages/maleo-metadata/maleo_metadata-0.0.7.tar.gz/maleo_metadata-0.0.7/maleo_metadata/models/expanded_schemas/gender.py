from pydantic import BaseModel, Field
from typing import Optional
from maleo_metadata.enums.gender import MaleoMetadataGenderEnums
from maleo_metadata.models.transfers.general.gender import GenderTransfers

class MaleoMetadataGenderExpandedSchemas:
    class SimpleGender(BaseModel):
        gender:MaleoMetadataGenderEnums.Gender = Field(..., description="Gender")

    class OptionalSimpleGender(BaseModel):
        gender:Optional[MaleoMetadataGenderEnums.Gender] = Field(None, description="Gender")

    class ExpandedGender(BaseModel):
        gender_details:GenderTransfers = Field(..., description="Gender's details")

    class OptionalExpandedGender(BaseModel):
        gender_details:Optional[GenderTransfers] = Field(None, description="Gender's details")