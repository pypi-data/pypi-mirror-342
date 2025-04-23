from fastapi import status
from maleo_foundation.utils.exceptions import BaseExceptions
from maleo_metadata.enums.general import MaleoMetadataGeneralEnums
from maleo_metadata.utils.logger import MaleoMetadataLoggerManager
from maleo_metadata.clients.http.controllers.organization_role import MaleoMetadataOrganizationRoleHTTPClientController
from maleo_metadata.models.transfers.parameters.general.organization_role import MaleoMetadataOrganizationRoleGeneralParametersTransfers
from maleo_metadata.models.transfers.parameters.client.organization_role import MaleoMetadataOrganizationRoleClientParametersTransfers
from maleo_metadata.models.transfers.results.general.organization_role import MaleoMetadataOrganizationRoleGeneralResultsTransfers
from maleo_metadata.types.results.general.organization_role import MaleoMetadataOrganizationRoleGeneralResultsTypes

class MaleoMetadataOrganizationRoleClientService:
    @staticmethod
    @BaseExceptions.service_exception_handler(
        operation="retrieving organization roles",
        logger_factory=MaleoMetadataLoggerManager.get,
        fail_result_class=MaleoMetadataOrganizationRoleGeneralResultsTransfers.Fail
    )
    async def get_organization_roles(
        parameters:MaleoMetadataOrganizationRoleClientParametersTransfers.GetMultiple,
        controller_role:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoMetadataOrganizationRoleGeneralResultsTypes.GetMultiple:
        """Retrieve organization roles from MaleoMetadata"""
        #* Validate chosen controller role
        if not isinstance(controller_role, MaleoMetadataGeneralEnums.ClientControllerType):
            message = "Invalid controller role"
            description = "The provided controller role did not exists"
            return MaleoMetadataOrganizationRoleGeneralResultsTransfers.Fail(message=message, description=description)
        #* Retrieve organization roles using chosen controller
        if controller_role == MaleoMetadataGeneralEnums.ClientControllerType.HTTP:
            controller_result = await MaleoMetadataOrganizationRoleHTTPClientController.get_organization_roles(parameters=parameters)
        else:
            message = "Invalid controller role"
            description = "The provided controller role has not been implemented"
            return MaleoMetadataOrganizationRoleGeneralResultsTransfers.Fail(message=message, description=description)
        #* Return proper response
        if not controller_result.success:
            return MaleoMetadataOrganizationRoleGeneralResultsTransfers.Fail.model_validate(controller_result.content)
        else:
            if controller_result.content["data"] is None:
                return MaleoMetadataOrganizationRoleGeneralResultsTransfers.NoData.model_validate(controller_result.content)
            else:
                return MaleoMetadataOrganizationRoleGeneralResultsTransfers.MultipleData.model_validate(controller_result.content)

    @staticmethod
    @BaseExceptions.service_exception_handler(
        operation="retrieving organization role",
        logger_factory=MaleoMetadataLoggerManager.get,
        fail_result_class=MaleoMetadataOrganizationRoleGeneralResultsTransfers.Fail
    )
    async def get_organization_role(
        parameters:MaleoMetadataOrganizationRoleGeneralParametersTransfers.GetSingle,
        controller_role:MaleoMetadataGeneralEnums.ClientControllerType = MaleoMetadataGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoMetadataOrganizationRoleGeneralResultsTypes.GetSingle:
        """Retrieve organization role from MaleoMetadata"""
        #* Validate chosen controller role
        if not isinstance(controller_role, MaleoMetadataGeneralEnums.ClientControllerType):
            message = "Invalid controller role"
            description = "The provided controller role did not exists"
            return MaleoMetadataOrganizationRoleGeneralResultsTransfers.Fail(message=message, description=description)
        #* Retrieve organization role using chosen controller
        if controller_role == MaleoMetadataGeneralEnums.ClientControllerType.HTTP:
            controller_result = await MaleoMetadataOrganizationRoleHTTPClientController.get_organization_role(parameters=parameters)
        else:
            message = "Invalid controller role"
            description = "The provided controller role has not been implemented"
            return MaleoMetadataOrganizationRoleGeneralResultsTransfers.Fail(message=message, description=description)
        #* Return proper response
        if not controller_result.success:
            if controller_result.status_code != status.HTTP_404_NOT_FOUND:
                return MaleoMetadataOrganizationRoleGeneralResultsTransfers.Fail.model_validate(controller_result.content)
            else:
                return MaleoMetadataOrganizationRoleGeneralResultsTransfers.NoData.model_validate(controller_result.content)
        else:
            return MaleoMetadataOrganizationRoleGeneralResultsTransfers.SingleData.model_validate(controller_result.content)