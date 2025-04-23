from maleo_foundation.models.transfers.results.client.controllers.http import BaseClientHTTPControllerResults
from maleo_metadata.clients.http.manager import MaleoMetadataHTTPClientManager
from maleo_metadata.models.transfers.parameters.general.blood_type import MaleoMetadataBloodTypeGeneralParametersTransfers
from maleo_metadata.models.transfers.parameters.client.blood_type import MaleoMetadataBloodTypeClientParametersTransfers

class MaleoMetadataBloodTypeHTTPClientController:
    @staticmethod
    async def get_blood_types(parameters:MaleoMetadataBloodTypeClientParametersTransfers.GetMultiple) -> BaseClientHTTPControllerResults:
        """Fetch blood types from MaleoMetadata"""
        async with MaleoMetadataHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoMetadataHTTPClientManager.base_url}/v1/blood-types/"

            #* Parse parameters to query params
            params = MaleoMetadataBloodTypeClientParametersTransfers.GetMultipleQuery.model_validate(parameters.model_dump()).model_dump(exclude_none=True)

            #* Send request and wait for response
            response = await client.get(url=url, params=params)
            return BaseClientHTTPControllerResults(response=response)

    @staticmethod
    async def get_blood_type(parameters:MaleoMetadataBloodTypeGeneralParametersTransfers.GetSingle) -> BaseClientHTTPControllerResults:
        """Fetch blood type from MaleoMetadata"""
        async with MaleoMetadataHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoMetadataHTTPClientManager.base_url}/v1/blood-types/{parameters.identifier}/{parameters.value}"

            #* Parse parameters to query params
            params = MaleoMetadataBloodTypeGeneralParametersTransfers.GetSingleQuery.model_validate(parameters.model_dump()).model_dump(exclude_none=True)

            #* Send request and wait for response
            response = await client.get(url=url, params=params)
            return BaseClientHTTPControllerResults(response=response)