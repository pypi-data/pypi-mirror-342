from pydantic import BaseModel, Field
from typing import Optional
from maleo_metadata.enums.blood_type import MaleoMetadataBloodTypeEnums
from maleo_metadata.models.transfers.general.blood_type import BloodTypeTransfers

class MaleoMetadataBloodTypeExpandedSchemas:
    class SimpleBloodType(BaseModel):
        blood_type:MaleoMetadataBloodTypeEnums.BloodType = Field(..., description="Blood type")

    class OptionalSimpleBloodType(BaseModel):
        blood_type:Optional[MaleoMetadataBloodTypeEnums.BloodType] = Field(None, description="Blood type")

    class ExpandedBloodType(BaseModel):
        blood_type_details:BloodTypeTransfers = Field(..., description="Blood type's details")

    class OptionalExpandedBloodType(BaseModel):
        blood_type_details:Optional[BloodTypeTransfers] = Field(None, description="Blood type's details")