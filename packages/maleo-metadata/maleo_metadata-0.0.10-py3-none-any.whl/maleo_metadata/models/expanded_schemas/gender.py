from pydantic import BaseModel, Field
from typing import List, Optional
from maleo_metadata.enums.gender import MaleoMetadataGenderEnums
from maleo_metadata.models.transfers.general.gender import GenderTransfers

class MaleoMetadataGenderExpandedSchemas:
    class SimpleGender(BaseModel):
        gender:MaleoMetadataGenderEnums.Gender = Field(..., description="Gender")

    class OptionalSimpleGender(BaseModel):
        gender:Optional[MaleoMetadataGenderEnums.Gender] = Field(None, description="Gender")

    class SimpleGenders(BaseModel):
        genders:List[MaleoMetadataGenderEnums.Gender] = Field([], description="Genders")

    class OptionalSimpleGenders(BaseModel):
        genders:Optional[List[MaleoMetadataGenderEnums.Gender]] = Field(None, description="Genders")

    class ExpandedGender(BaseModel):
        gender_details:GenderTransfers = Field(..., description="Gender's details")

    class OptionalExpandedGender(BaseModel):
        gender_details:Optional[GenderTransfers] = Field(None, description="Gender's details")

    class ExpandedGenders(BaseModel):
        genders_details:List[GenderTransfers] = Field([], description="Genders's details")

    class OptionalExpandedGender(BaseModel):
        genders_details:Optional[List[GenderTransfers]] = Field(None, description="Genders's details")