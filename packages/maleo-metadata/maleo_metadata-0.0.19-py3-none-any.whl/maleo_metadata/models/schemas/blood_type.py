from pydantic import BaseModel, Field

class MaleoMetadataBloodTypeSchemas:
    class Key(BaseModel):
        key:str = Field(..., max_length=2, description="Blood Type's key")

    class Name(BaseModel):
        name:str = Field(..., max_length=2, description="Blood Type's name")