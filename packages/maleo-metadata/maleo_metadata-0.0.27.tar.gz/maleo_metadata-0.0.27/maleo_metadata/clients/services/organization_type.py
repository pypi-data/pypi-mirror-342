from fastapi import status
from maleo_foundation.utils.exceptions import BaseExceptions
from maleo_metadata.enums.general import MaleoMetadataGeneralEnums
from maleo_metadata.utils.logger import MaleoMetadataLoggerManager
from maleo_metadata.clients.http.controllers.organization_type import MaleoMetadataOrganizationTypeHTTPClientController
from maleo_metadata.models.transfers.parameters.general.organization_type import MaleoMetadataOrganizationTypeGeneralParametersTransfers
from maleo_metadata.models.transfers.parameters.client.organization_type import MaleoMetadataOrganizationTypeClientParametersTransfers
from maleo_metadata.models.transfers.results.general.organization_type import MaleoMetadataOrganizationTypeGeneralResultsTransfers
from maleo_metadata.types.results.general.organization_type import MaleoMetadataOrganizationTypeGeneralResultsTypes

class MaleoMetadataOrganizationTypeClientService:
    @staticmethod
    @BaseExceptions.service_exception_handler(
        operation="retrieving organization types",
        logger_factory=MaleoMetadataLoggerManager.get,
        fail_result_class=MaleoMetadataOrganizationTypeGeneralResultsTransfers.Fail
    )
    async def get_organization_types(
        parameters:MaleoMetadataOrganizationTypeClientParametersTransfers.GetMultiple,
        controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoMetadataOrganizationTypeGeneralResultsTypes.GetMultiple:
        """Retrieve organization types from MaleoMetadata"""
        #* Validate chosen controller type
        if not isinstance(controller_type, MaleoMetadataGeneralEnums.ClientControllerType):
            message = "Invalid controller type"
            description = "The provided controller type did not exists"
            return MaleoMetadataOrganizationTypeGeneralResultsTransfers.Fail(message=message, description=description)
        #* Retrieve organization types using chosen controller
        if controller_type == MaleoMetadataGeneralEnums.ClientControllerType.HTTP:
            controller_result = await MaleoMetadataOrganizationTypeHTTPClientController.get_organization_types(parameters=parameters)
        else:
            message = "Invalid controller type"
            description = "The provided controller type has not been implemented"
            return MaleoMetadataOrganizationTypeGeneralResultsTransfers.Fail(message=message, description=description)
        #* Return proper response
        if not controller_result.success:
            return MaleoMetadataOrganizationTypeGeneralResultsTransfers.Fail.model_validate(controller_result.content)
        else:
            if controller_result.content["data"] is None:
                return MaleoMetadataOrganizationTypeGeneralResultsTransfers.NoData.model_validate(controller_result.content)
            else:
                return MaleoMetadataOrganizationTypeGeneralResultsTransfers.MultipleData.model_validate(controller_result.content)

    @staticmethod
    @BaseExceptions.service_exception_handler(
        operation="retrieving organization type",
        logger_factory=MaleoMetadataLoggerManager.get,
        fail_result_class=MaleoMetadataOrganizationTypeGeneralResultsTransfers.Fail
    )
    async def get_organization_type(
        parameters:MaleoMetadataOrganizationTypeGeneralParametersTransfers.GetSingle,
        controller_type:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoMetadataOrganizationTypeGeneralResultsTypes.GetSingle:
        """Retrieve organization type from MaleoMetadata"""
        #* Validate chosen controller type
        if not isinstance(controller_type, MaleoMetadataGeneralEnums.ClientControllerType):
            message = "Invalid controller type"
            description = "The provided controller type did not exists"
            return MaleoMetadataOrganizationTypeGeneralResultsTransfers.Fail(message=message, description=description)
        #* Retrieve organization type using chosen controller
        if controller_type == MaleoMetadataGeneralEnums.ClientControllerType.HTTP:
            controller_result = await MaleoMetadataOrganizationTypeHTTPClientController.get_organization_type(parameters=parameters)
        else:
            message = "Invalid controller type"
            description = "The provided controller type has not been implemented"
            return MaleoMetadataOrganizationTypeGeneralResultsTransfers.Fail(message=message, description=description)
        #* Return proper response
        if not controller_result.success:
            if controller_result.status_code != status.HTTP_404_NOT_FOUND:
                return MaleoMetadataOrganizationTypeGeneralResultsTransfers.Fail.model_validate(controller_result.content)
            else:
                return MaleoMetadataOrganizationTypeGeneralResultsTransfers.NoData.model_validate(controller_result.content)
        else:
            return MaleoMetadataOrganizationTypeGeneralResultsTransfers.SingleData.model_validate(controller_result.content)