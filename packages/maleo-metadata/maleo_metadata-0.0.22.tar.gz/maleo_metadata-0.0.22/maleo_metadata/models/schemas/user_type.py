from pydantic import Field
from maleo_foundation.models.schemas.general import BaseGeneralSchemas

class MaleoMetadataUserTypeSchemas:
    class Key(BaseGeneralSchemas.Key):
        key:str = Field(..., max_length=20, description="User Type's key")

    class Name(BaseGeneralSchemas.Name):
        name:str = Field(..., max_length=20, description="User Type's name")