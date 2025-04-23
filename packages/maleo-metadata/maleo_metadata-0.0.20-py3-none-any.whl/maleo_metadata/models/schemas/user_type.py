from pydantic import BaseModel, Field

class MaleoMetadataUserTypeSchemas:
    class Key(BaseModel):
        key:str = Field(..., max_length=2, description="User Type's key")

    class Name(BaseModel):
        name:str = Field(..., max_length=2, description="User Type's name")