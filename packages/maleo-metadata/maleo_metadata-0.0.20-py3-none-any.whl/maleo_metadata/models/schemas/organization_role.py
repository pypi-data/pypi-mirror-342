from pydantic import BaseModel, Field

class MaleoMetadataOrganizationRoleSchemas:
    class Key(BaseModel):
        key:str = Field(..., max_length=20, description="Organization Role's key")

    class Name(BaseModel):
        name:str = Field(..., max_length=20, description="Organization Role's name")