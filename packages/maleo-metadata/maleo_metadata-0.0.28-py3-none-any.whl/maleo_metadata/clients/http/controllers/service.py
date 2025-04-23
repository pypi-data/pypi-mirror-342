from maleo_foundation.models.transfers.results.client.controllers.http import BaseClientHTTPControllerResults
from maleo_metadata.clients.http.manager import MaleoMetadataHTTPClientManager
from maleo_metadata.models.transfers.parameters.general.service import MaleoMetadataServiceGeneralParametersTransfers
from maleo_metadata.models.transfers.parameters.client.service import MaleoMetadataServiceClientParametersTransfers

class MaleoMetadataServiceHTTPClientController:
    @staticmethod
    async def get_services(parameters:MaleoMetadataServiceClientParametersTransfers.GetMultiple) -> BaseClientHTTPControllerResults:
        """Fetch services from MaleoMetadata"""
        async with MaleoMetadataHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoMetadataHTTPClientManager.base_url}/v1/services/"

            #* Parse parameters to query params
            params = MaleoMetadataServiceClientParametersTransfers.GetMultipleQuery.model_validate(parameters.model_dump()).model_dump(exclude_none=True)

            #* Send request and wait for response
            response = await client.get(url=url, params=params)
            return BaseClientHTTPControllerResults(response=response)

    @staticmethod
    async def get_service(parameters:MaleoMetadataServiceGeneralParametersTransfers.GetSingle) -> BaseClientHTTPControllerResults:
        """Fetch service from MaleoMetadata"""
        async with MaleoMetadataHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoMetadataHTTPClientManager.base_url}/v1/services/{parameters.identifier}/{parameters.value}"

            #* Parse parameters to query params
            params = MaleoMetadataServiceGeneralParametersTransfers.GetSingleQuery.model_validate(parameters.model_dump()).model_dump(exclude_none=True)

            #* Send request and wait for response
            response = await client.get(url=url, params=params)
            return BaseClientHTTPControllerResults(response=response)