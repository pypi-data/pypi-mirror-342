from maleo_foundation.models.transfers.results.client.controllers.http import BaseClientHTTPControllerResults
from maleo_metadata.clients.http.manager import MaleoMetadataHTTPClientManager
from maleo_metadata.models.transfers.parameters.general.system_role import MaleoMetadataSystemRoleGeneralParametersTransfers
from maleo_metadata.models.transfers.parameters.client.system_role import MaleoMetadataSystemRoleClientParametersTransfers

class MaleoMetadataSystemRoleHTTPClientController:
    @staticmethod
    async def get_system_roles(parameters:MaleoMetadataSystemRoleClientParametersTransfers.GetMultiple) -> BaseClientHTTPControllerResults:
        """Fetch system roles from MaleoMetadata"""
        async with MaleoMetadataHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoMetadataHTTPClientManager.base_url}/v1/system-roles/"

            #* Parse parameters to query params
            params = MaleoMetadataSystemRoleClientParametersTransfers.GetMultipleQuery.model_validate(parameters.model_dump()).model_dump(exclude_none=True)

            #* Send request and wait for response
            response = await client.get(url=url, params=params)
            return BaseClientHTTPControllerResults(response=response)

    @staticmethod
    async def get_system_role(parameters:MaleoMetadataSystemRoleGeneralParametersTransfers.GetSingle) -> BaseClientHTTPControllerResults:
        """Fetch system role from MaleoMetadata"""
        async with MaleoMetadataHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoMetadataHTTPClientManager.base_url}/v1/system-roles/{parameters.identifier}/{parameters.value}"

            #* Parse parameters to query params
            params = MaleoMetadataSystemRoleGeneralParametersTransfers.GetSingleQuery.model_validate(parameters.model_dump()).model_dump(exclude_none=True)

            #* Send request and wait for response
            response = await client.get(url=url, params=params)
            return BaseClientHTTPControllerResults(response=response)