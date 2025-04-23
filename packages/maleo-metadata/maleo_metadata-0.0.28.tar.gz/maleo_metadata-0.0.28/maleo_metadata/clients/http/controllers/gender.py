from maleo_foundation.models.transfers.results.client.controllers.http import BaseClientHTTPControllerResults
from maleo_metadata.clients.http.manager import MaleoMetadataHTTPClientManager
from maleo_metadata.models.transfers.parameters.general.gender import MaleoMetadataGenderGeneralParametersTransfers
from maleo_metadata.models.transfers.parameters.client.gender import MaleoMetadataGenderClientParametersTransfers

class MaleoMetadataGenderHTTPClientController:
    @staticmethod
    async def get_genders(parameters:MaleoMetadataGenderClientParametersTransfers.GetMultiple) -> BaseClientHTTPControllerResults:
        """Fetch genders from MaleoMetadata"""
        async with MaleoMetadataHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoMetadataHTTPClientManager.base_url}/v1/genders/"

            #* Parse parameters to query params
            params = MaleoMetadataGenderClientParametersTransfers.GetMultipleQuery.model_validate(parameters.model_dump()).model_dump(exclude_none=True)

            #* Send request and wait for response
            response = await client.get(url=url, params=params)
            return BaseClientHTTPControllerResults(response=response)

    @staticmethod
    async def get_gender(parameters:MaleoMetadataGenderGeneralParametersTransfers.GetSingle) -> BaseClientHTTPControllerResults:
        """Fetch gender from MaleoMetadata"""
        async with MaleoMetadataHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoMetadataHTTPClientManager.base_url}/v1/genders/{parameters.identifier}/{parameters.value}"

            #* Parse parameters to query params
            params = MaleoMetadataGenderGeneralParametersTransfers.GetSingleQuery.model_validate(parameters.model_dump()).model_dump(exclude_none=True)

            #* Send request and wait for response
            response = await client.get(url=url, params=params)
            return BaseClientHTTPControllerResults(response=response)