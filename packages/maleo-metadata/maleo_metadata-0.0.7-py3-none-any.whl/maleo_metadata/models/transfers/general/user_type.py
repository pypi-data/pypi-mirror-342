from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from pydantic import Field

class UserTypeTransfers(
    BaseGeneralSchemas.Name,
    BaseGeneralSchemas.Key,
    BaseGeneralSchemas.Order,
    BaseGeneralSchemas.Status,
    BaseGeneralSchemas.Timestamps,
    BaseGeneralSchemas.Identifiers
):
    key:str = Field(..., max_length=2, description="User type's key")
    name:str = Field(..., max_length=2, description="User type's name")