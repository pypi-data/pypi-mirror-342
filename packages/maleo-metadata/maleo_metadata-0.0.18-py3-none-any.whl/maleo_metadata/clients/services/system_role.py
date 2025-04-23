from fastapi import status
from maleo_foundation.utils.exceptions import BaseExceptions
from maleo_metadata.enums.general import MaleoMetadataGeneralEnums
from maleo_metadata.utils.logger import MaleoMetadataLoggerManager
from maleo_metadata.clients.http.controllers.system_role import MaleoMetadataSystemRoleHTTPClientController
from maleo_metadata.models.transfers.parameters.general.system_role import MaleoMetadataSystemRoleGeneralParametersTransfers
from maleo_metadata.models.transfers.parameters.client.system_role import MaleoMetadataSystemRoleClientParametersTransfers
from maleo_metadata.models.transfers.results.general.system_role import MaleoMetadataSystemRoleGeneralResultsTransfers
from maleo_metadata.types.results.general.system_role import MaleoMetadataSystemRoleGeneralResultsTypes

class MaleoMetadataSystemRoleClientService:
    @staticmethod
    @BaseExceptions.service_exception_handler(
        operation="retrieving system roles",
        logger_factory=MaleoMetadataLoggerManager.get,
        fail_result_class=MaleoMetadataSystemRoleGeneralResultsTransfers.Fail
    )
    async def get_system_roles(
        parameters:MaleoMetadataSystemRoleClientParametersTransfers.GetMultiple,
        controller_role:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoMetadataSystemRoleGeneralResultsTypes.GetMultiple:
        """Retrieve system roles from MaleoMetadata"""
        #* Validate chosen controller role
        if not isinstance(controller_role, MaleoMetadataGeneralEnums.ClientControllerType):
            message = "Invalid controller role"
            description = "The provided controller role did not exists"
            return MaleoMetadataSystemRoleGeneralResultsTransfers.Fail(message=message, description=description)
        #* Retrieve system roles using chosen controller
        if controller_role == MaleoMetadataGeneralEnums.ClientControllerType.HTTP:
            controller_result = await MaleoMetadataSystemRoleHTTPClientController.get_system_roles(parameters=parameters)
        else:
            message = "Invalid controller role"
            description = "The provided controller role has not been implemented"
            return MaleoMetadataSystemRoleGeneralResultsTransfers.Fail(message=message, description=description)
        #* Return proper response
        if not controller_result.success:
            return MaleoMetadataSystemRoleGeneralResultsTransfers.Fail.model_validate(controller_result.content)
        else:
            if controller_result.content["data"] is None:
                return MaleoMetadataSystemRoleGeneralResultsTransfers.NoData.model_validate(controller_result.content)
            else:
                return MaleoMetadataSystemRoleGeneralResultsTransfers.MultipleData.model_validate(controller_result.content)

    @staticmethod
    @BaseExceptions.service_exception_handler(
        operation="retrieving system role",
        logger_factory=MaleoMetadataLoggerManager.get,
        fail_result_class=MaleoMetadataSystemRoleGeneralResultsTransfers.Fail
    )
    async def get_system_role(
        parameters:MaleoMetadataSystemRoleGeneralParametersTransfers.GetSingle,
        controller_role:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoMetadataSystemRoleGeneralResultsTypes.GetSingle:
        """Retrieve system role from MaleoMetadata"""
        #* Validate chosen controller role
        if not isinstance(controller_role, MaleoMetadataGeneralEnums.ClientControllerType):
            message = "Invalid controller role"
            description = "The provided controller role did not exists"
            return MaleoMetadataSystemRoleGeneralResultsTransfers.Fail(message=message, description=description)
        #* Retrieve system role using chosen controller
        if controller_role == MaleoMetadataGeneralEnums.ClientControllerType.HTTP:
            controller_result = await MaleoMetadataSystemRoleHTTPClientController.get_system_role(parameters=parameters)
        else:
            message = "Invalid controller role"
            description = "The provided controller role has not been implemented"
            return MaleoMetadataSystemRoleGeneralResultsTransfers.Fail(message=message, description=description)
        #* Return proper response
        if not controller_result.success:
            if controller_result.status_code != status.HTTP_404_NOT_FOUND:
                return MaleoMetadataSystemRoleGeneralResultsTransfers.Fail.model_validate(controller_result.content)
            else:
                return MaleoMetadataSystemRoleGeneralResultsTransfers.NoData.model_validate(controller_result.content)
        else:
            return MaleoMetadataSystemRoleGeneralResultsTransfers.SingleData.model_validate(controller_result.content)