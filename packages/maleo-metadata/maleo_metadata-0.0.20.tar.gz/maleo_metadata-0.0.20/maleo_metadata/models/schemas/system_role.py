from pydantic import BaseModel, Field

class MaleoMetadataSystemRoleSchemas:
    class Key(BaseModel):
        key:str = Field(..., max_length=20, description="System Role's key")

    class Name(BaseModel):
        name:str = Field(..., max_length=20, description="System Role's name")