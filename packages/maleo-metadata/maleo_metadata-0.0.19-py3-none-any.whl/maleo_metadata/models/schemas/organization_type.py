from pydantic import BaseModel, Field

class MaleoMetadataOrganizationTypeSchemas:
    class Key(BaseModel):
        key:str = Field(..., max_length=2, description="Organization Type's key")

    class Name(BaseModel):
        name:str = Field(..., max_length=2, description="Organization Type's name")