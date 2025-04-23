from fastapi import status
from maleo_foundation.utils.exceptions import BaseExceptions
from maleo_metadata.enums.general import MaleoMetadataGeneralEnums
from maleo_metadata.utils.logger import MaleoMetadataLoggerManager
from maleo_metadata.clients.http.controllers.service import MaleoMetadataServiceHTTPClientController
from maleo_metadata.models.transfers.parameters.general.service import MaleoMetadataServiceGeneralParametersTransfers
from maleo_metadata.models.transfers.parameters.client.service import MaleoMetadataServiceClientParametersTransfers
from maleo_metadata.models.transfers.results.general.service import MaleoMetadataServiceGeneralResultsTransfers
from maleo_metadata.types.results.general.service import MaleoMetadataServiceGeneralResultsTypes

class MaleoMetadataServiceClientService:
    @staticmethod
    @BaseExceptions.service_exception_handler(
        operation="retrieving services",
        logger_factory=MaleoMetadataLoggerManager.get,
        fail_result_class=MaleoMetadataServiceGeneralResultsTransfers.Fail
    )
    async def get_services(
        parameters:MaleoMetadataServiceClientParametersTransfers.GetMultiple,
        controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoMetadataServiceGeneralResultsTypes.GetMultiple:
        """Retrieve services from MaleoMetadata"""
        #* Validate chosen controller type
        if not isinstance(controller_type, MaleoMetadataGeneralEnums.ClientControllerType):
            message = "Invalid controller type"
            description = "The provided controller type did not exists"
            return MaleoMetadataServiceGeneralResultsTransfers.Fail(message=message, description=description)
        #* Retrieve services using chosen controller
        if controller_type == MaleoMetadataGeneralEnums.ClientControllerType.HTTP:
            controller_result = await MaleoMetadataServiceHTTPClientController.get_services(parameters=parameters)
        else:
            message = "Invalid controller type"
            description = "The provided controller type has not been implemented"
            return MaleoMetadataServiceGeneralResultsTransfers.Fail(message=message, description=description)
        #* Return proper response
        if not controller_result.success:
            return MaleoMetadataServiceGeneralResultsTransfers.Fail.model_validate(controller_result.content)
        else:
            if controller_result.content["data"] is None:
                return MaleoMetadataServiceGeneralResultsTransfers.NoData.model_validate(controller_result.content)
            else:
                return MaleoMetadataServiceGeneralResultsTransfers.MultipleData.model_validate(controller_result.content)

    @staticmethod
    @BaseExceptions.service_exception_handler(
        operation="retrieving service",
        logger_factory=MaleoMetadataLoggerManager.get,
        fail_result_class=MaleoMetadataServiceGeneralResultsTransfers.Fail
    )
    async def get_service(
        parameters:MaleoMetadataServiceGeneralParametersTransfers.GetSingle,
        controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoMetadataServiceGeneralResultsTypes.GetSingle:
        """Retrieve service from MaleoMetadata"""
        #* Validate chosen controller type
        if not isinstance(controller_type, MaleoMetadataGeneralEnums.ClientControllerType):
            message = "Invalid controller type"
            description = "The provided controller type did not exists"
            return MaleoMetadataServiceGeneralResultsTransfers.Fail(message=message, description=description)
        #* Retrieve service using chosen controller
        if controller_type == MaleoMetadataGeneralEnums.ClientControllerType.HTTP:
            controller_result = await MaleoMetadataServiceHTTPClientController.get_service(parameters=parameters)
        else:
            message = "Invalid controller type"
            description = "The provided controller type has not been implemented"
            return MaleoMetadataServiceGeneralResultsTransfers.Fail(message=message, description=description)
        #* Return proper response
        if not controller_result.success:
            if controller_result.status_code != status.HTTP_404_NOT_FOUND:
                return MaleoMetadataServiceGeneralResultsTransfers.Fail.model_validate(controller_result.content)
            else:
                return MaleoMetadataServiceGeneralResultsTransfers.NoData.model_validate(controller_result.content)
        else:
            return MaleoMetadataServiceGeneralResultsTransfers.SingleData.model_validate(controller_result.content)