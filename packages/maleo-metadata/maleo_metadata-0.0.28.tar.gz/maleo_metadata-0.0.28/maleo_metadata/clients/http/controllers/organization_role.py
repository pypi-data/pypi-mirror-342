from maleo_foundation.models.transfers.results.client.controllers.http import BaseClientHTTPControllerResults
from maleo_metadata.clients.http.manager import MaleoMetadataHTTPClientManager
from maleo_metadata.models.transfers.parameters.general.organization_role import MaleoMetadataOrganizationRoleGeneralParametersTransfers
from maleo_metadata.models.transfers.parameters.client.organization_role import MaleoMetadataOrganizationRoleClientParametersTransfers

class MaleoMetadataOrganizationRoleHTTPClientController:
    @staticmethod
    async def get_organization_roles(parameters:MaleoMetadataOrganizationRoleClientParametersTransfers.GetMultiple) -> BaseClientHTTPControllerResults:
        """Fetch organization roles from MaleoMetadata"""
        async with MaleoMetadataHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoMetadataHTTPClientManager.base_url}/v1/organization-roles/"

            #* Parse parameters to query params
            params = MaleoMetadataOrganizationRoleClientParametersTransfers.GetMultipleQuery.model_validate(parameters.model_dump()).model_dump(exclude_none=True)

            #* Send request and wait for response
            response = await client.get(url=url, params=params)
            return BaseClientHTTPControllerResults(response=response)

    @staticmethod
    async def get_organization_role(parameters:MaleoMetadataOrganizationRoleGeneralParametersTransfers.GetSingle) -> BaseClientHTTPControllerResults:
        """Fetch organization role from MaleoMetadata"""
        async with MaleoMetadataHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoMetadataHTTPClientManager.base_url}/v1/organization-roles/{parameters.identifier}/{parameters.value}"

            #* Parse parameters to query params
            params = MaleoMetadataOrganizationRoleGeneralParametersTransfers.GetSingleQuery.model_validate(parameters.model_dump()).model_dump(exclude_none=True)

            #* Send request and wait for response
            response = await client.get(url=url, params=params)
            return BaseClientHTTPControllerResults(response=response)