from pydantic import Field
from maleo_foundation.models.schemas.general import BaseGeneralSchemas

class MaleoMetadataServiceSchemas:
    class Key(BaseGeneralSchemas.Key):
        key:str = Field(..., max_length=20, description="Service's key")

    class Name(BaseGeneralSchemas.Name):
        name:str = Field(..., max_length=20, description="Service's name")