from pydantic import BaseModel, Field
from uuid import UUID

class MaleoMetadataServiceSchemas:
    class Key(BaseModel):
        key:str = Field(..., max_length=20, description="Service's key")

    class Name(BaseModel):
        name:str = Field(..., max_length=20, description="Service's name")