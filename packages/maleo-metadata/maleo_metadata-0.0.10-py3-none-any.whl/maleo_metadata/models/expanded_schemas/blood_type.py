from pydantic import BaseModel, Field
from typing import List, Optional
from maleo_metadata.enums.blood_type import MaleoMetadataBloodTypeEnums
from maleo_metadata.models.transfers.general.blood_type import BloodTypeTransfers

class MaleoMetadataBloodTypeExpandedSchemas:
    class SimpleBloodType(BaseModel):
        blood_type:MaleoMetadataBloodTypeEnums.BloodType = Field(..., description="Blood type")

    class OptionalSimpleBloodType(BaseModel):
        blood_type:Optional[MaleoMetadataBloodTypeEnums.BloodType] = Field(None, description="Blood type")

    class SimpleBloodTypes(BaseModel):
        blood_types:List[MaleoMetadataBloodTypeEnums.BloodType] = Field([], description="Blood types")

    class OptionalSimpleBloodTypes(BaseModel):
        blood_types:Optional[List[MaleoMetadataBloodTypeEnums.BloodType]] = Field(None, description="Blood types")

    class ExpandedBloodType(BaseModel):
        blood_type_details:BloodTypeTransfers = Field(..., description="Blood type's details")

    class OptionalExpandedBloodType(BaseModel):
        blood_type_details:Optional[BloodTypeTransfers] = Field(None, description="Blood type's details")

    class ExpandedBloodTypes(BaseModel):
        blood_types_details:List[BloodTypeTransfers] = Field([], description="Blood types's details")

    class OptionalExpandedBloodType(BaseModel):
        blood_types_details:Optional[List[BloodTypeTransfers]] = Field(None, description="Blood types's details")