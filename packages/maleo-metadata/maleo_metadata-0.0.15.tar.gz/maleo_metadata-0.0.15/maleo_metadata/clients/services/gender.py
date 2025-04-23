from fastapi import status
from maleo_foundation.utils.exceptions import BaseExceptions
from maleo_metadata.enums.general import MaleoMetadataGeneralEnums
from maleo_metadata.utils.logger import MaleoMetadataLoggerManager
from maleo_metadata.clients.http.controllers.gender import MaleoMetadataGenderHTTPClientController
from maleo_metadata.models.transfers.parameters.general.gender import MaleoMetadataGenderGeneralParametersTransfers
from maleo_metadata.models.transfers.parameters.client.gender import MaleoMetadataGenderClientParametersTransfers
from maleo_metadata.models.transfers.results.general.gender import MaleoMetadataGenderGeneralResultsTransfers
from maleo_metadata.types.results.general.gender import MaleoMetadataGenderGeneralResultsTypes

class MaleoMetadataGenderClientService:
    @staticmethod
    @BaseExceptions.service_exception_handler(
        operation="retrieving genders",
        logger_factory=MaleoMetadataLoggerManager.get,
        fail_result_class=MaleoMetadataGenderGeneralResultsTransfers.Fail
    )
    async def get_genders(
        parameters:MaleoMetadataGenderClientParametersTransfers.GetMultiple,
        controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoMetadataGenderGeneralResultsTypes.GetMultiple:
        """Retrieve genders from MaleoMetadata"""
        #* Validate chosen controller type
        if not isinstance(controller_type, MaleoMetadataGeneralEnums.ClientControllerType):
            message = "Invalid controller type"
            description = "The provided controller type did not exists"
            return MaleoMetadataGenderGeneralResultsTransfers.Fail(message=message, description=description)
        #* Retrieve genders using chosen controller
        if controller_type == MaleoMetadataGeneralEnums.ClientControllerType.HTTP:
            controller_result = await MaleoMetadataGenderHTTPClientController.get_genders(parameters=parameters)
        else:
            message = "Invalid controller type"
            description = "The provided controller type has not been implemented"
            return MaleoMetadataGenderGeneralResultsTransfers.Fail(message=message, description=description)
        #* Return proper response
        if not controller_result.success:
            return MaleoMetadataGenderGeneralResultsTransfers.Fail.model_validate(controller_result.content)
        else:
            if controller_result.content["data"] is None:
                return MaleoMetadataGenderGeneralResultsTransfers.NoData.model_validate(controller_result.content)
            else:
                return MaleoMetadataGenderGeneralResultsTransfers.MultipleData.model_validate(controller_result.content)

    @staticmethod
    @BaseExceptions.service_exception_handler(
        operation="retrieving gender",
        logger_factory=MaleoMetadataLoggerManager.get,
        fail_result_class=MaleoMetadataGenderGeneralResultsTransfers.Fail
    )
    async def get_gender(
        parameters:MaleoMetadataGenderGeneralParametersTransfers.GetSingle,
        controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoMetadataGenderGeneralResultsTypes.GetSingle:
        """Retrieve gender from MaleoMetadata"""
        #* Validate chosen controller type
        if not isinstance(controller_type, MaleoMetadataGeneralEnums.ClientControllerType):
            message = "Invalid controller type"
            description = "The provided controller type did not exists"
            return MaleoMetadataGenderGeneralResultsTransfers.Fail(message=message, description=description)
        #* Retrieve gender using chosen controller
        if controller_type == MaleoMetadataGeneralEnums.ClientControllerType.HTTP:
            controller_result = await MaleoMetadataGenderHTTPClientController.get_gender(parameters=parameters)
        else:
            message = "Invalid controller type"
            description = "The provided controller type has not been implemented"
            return MaleoMetadataGenderGeneralResultsTransfers.Fail(message=message, description=description)
        #* Return proper response
        if not controller_result.success:
            if controller_result.status_code != status.HTTP_404_NOT_FOUND:
                return MaleoMetadataGenderGeneralResultsTransfers.Fail.model_validate(controller_result.content)
            else:
                return MaleoMetadataGenderGeneralResultsTransfers.NoData.model_validate(controller_result.content)
        else:
            return MaleoMetadataGenderGeneralResultsTransfers.SingleData.model_validate(controller_result.content)