from maleo_foundation.models.transfers.results.client.controllers.http import BaseClientHTTPControllerResults
from maleo_metadata.clients.http.manager import MaleoMetadataHTTPClientManager
from maleo_metadata.models.transfers.parameters.general.user_type import MaleoMetadataUserTypeGeneralParametersTransfers
from maleo_metadata.models.transfers.parameters.client.user_type import MaleoMetadataUserTypeClientParametersTransfers

class MaleoMetadataUserTypeHTTPClientController:
    @staticmethod
    async def get_user_types(parameters:MaleoMetadataUserTypeClientParametersTransfers.GetMultiple) -> BaseClientHTTPControllerResults:
        """Fetch user types from MaleoMetadata"""
        async with MaleoMetadataHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoMetadataHTTPClientManager.base_url}/v1/user-types/"

            #* Parse parameters to query params
            params = MaleoMetadataUserTypeClientParametersTransfers.GetMultipleQuery.model_validate(parameters.model_dump()).model_dump(exclude_none=True)

            #* Send request and wait for response
            response = await client.get(url=url, params=params)
            return BaseClientHTTPControllerResults(response=response)

    @staticmethod
    async def get_user_type(parameters:MaleoMetadataUserTypeGeneralParametersTransfers.GetSingle) -> BaseClientHTTPControllerResults:
        """Fetch user type from MaleoMetadata"""
        async with MaleoMetadataHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoMetadataHTTPClientManager.base_url}/v1/user-types/{parameters.identifier}/{parameters.value}"

            #* Parse parameters to query params
            params = MaleoMetadataUserTypeGeneralParametersTransfers.GetSingleQuery.model_validate(parameters.model_dump()).model_dump(exclude_none=True)

            #* Send request and wait for response
            response = await client.get(url=url, params=params)
            return BaseClientHTTPControllerResults(response=response)