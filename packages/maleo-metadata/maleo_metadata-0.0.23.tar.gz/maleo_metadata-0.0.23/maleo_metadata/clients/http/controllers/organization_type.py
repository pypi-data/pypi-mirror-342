from maleo_foundation.models.transfers.results.client.controllers.http import BaseClientHTTPControllerResults
from maleo_metadata.clients.http.manager import MaleoMetadataHTTPClientManager
from maleo_metadata.models.transfers.parameters.general.organization_type import MaleoMetadataOrganizationTypeGeneralParametersTransfers
from maleo_metadata.models.transfers.parameters.client.organization_type import MaleoMetadataOrganizationTypeClientParametersTransfers

class MaleoMetadataOrganizationTypeHTTPClientController:
    @staticmethod
    async def get_organization_types(parameters:MaleoMetadataOrganizationTypeClientParametersTransfers.GetMultiple) -> BaseClientHTTPControllerResults:
        """Fetch organization types from MaleoMetadata"""
        async with MaleoMetadataHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoMetadataHTTPClientManager.base_url}/v1/organization-types/"

            #* Parse parameters to query params
            params = MaleoMetadataOrganizationTypeClientParametersTransfers.GetMultipleQuery.model_validate(parameters.model_dump()).model_dump(exclude_none=True)

            #* Send request and wait for response
            response = await client.get(url=url, params=params)
            return BaseClientHTTPControllerResults(response=response)

    @staticmethod
    async def get_organization_type(parameters:MaleoMetadataOrganizationTypeGeneralParametersTransfers.GetSingle) -> BaseClientHTTPControllerResults:
        """Fetch organization type from MaleoMetadata"""
        async with MaleoMetadataHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoMetadataHTTPClientManager.base_url}/v1/organization-types/{parameters.identifier}/{parameters.value}"

            #* Parse parameters to query params
            params = MaleoMetadataOrganizationTypeGeneralParametersTransfers.GetSingleQuery.model_validate(parameters.model_dump()).model_dump(exclude_none=True)

            #* Send request and wait for response
            response = await client.get(url=url, params=params)
            return BaseClientHTTPControllerResults(response=response)