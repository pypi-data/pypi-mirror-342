from pydantic import Field
from maleo_foundation.models.schemas.general import BaseGeneralSchemas

class MaleoMetadataBloodTypeSchemas:
    class Key(BaseGeneralSchemas.Key):
        key:str = Field(..., max_length=20, description="Blood Type's key")

    class Name(BaseGeneralSchemas.Name):
        name:str = Field(..., max_length=20, description="Blood Type's name")