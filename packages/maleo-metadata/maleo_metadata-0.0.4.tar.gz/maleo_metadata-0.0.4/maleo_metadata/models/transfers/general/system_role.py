from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from pydantic import Field

class SystemRoleTransfers(
    BaseGeneralSchemas.Name,
    BaseGeneralSchemas.Key,
    BaseGeneralSchemas.Order,
    BaseGeneralSchemas.Status,
    BaseGeneralSchemas.Timestamps,
    BaseGeneralSchemas.Identifiers
):
    key:str = Field(..., max_length=20, description="System role's key")
    name:str = Field(..., max_length=20, description="System role's name")