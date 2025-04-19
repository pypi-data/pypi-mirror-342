from __future__ import annotations
from pydantic import Field
from typing import Union
from uuid import UUID
from maleo_metadata.models.enums.service import MaleoMetadataServiceEnums
from maleo_foundation.models.transfers.parameters.general import BaseGeneralParametersTransfers

class MaleoMetadataServiceGeneralParametersTransfers:
    class GetSingleQuery(BaseGeneralParametersTransfers.GetSingleQuery): pass

    class GetSingle(BaseGeneralParametersTransfers.GetSingle):
        identifier:MaleoMetadataServiceEnums.UniqueIdentifiers = Field(..., description="Identifier")
        value:Union[int, UUID] = Field(..., description="Value")