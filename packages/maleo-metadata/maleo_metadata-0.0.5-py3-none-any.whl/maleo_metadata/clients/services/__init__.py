from __future__ import annotations
from .blood_type import MaleoMetadataBloodTypeClientService
from .gender import MaleoMetadataGenderClientService
from .organization_role import MaleoMetadataOrganizationRoleClientService
from .organization_type import MaleoMetadataOrganizationTypeClientService
from .service import MaleoMetadataServiceClientService
from .system_role import MaleoMetadataSystemRoleClientService
from .user_type import MaleoMetadataUserTypeClientService

class MaleoMetadataClientServices:
    BloodType = MaleoMetadataBloodTypeClientService
    Gender = MaleoMetadataGenderClientService
    OrganizationRole = MaleoMetadataOrganizationRoleClientService
    OrganizationType = MaleoMetadataOrganizationTypeClientService
    Service = MaleoMetadataServiceClientService
    SystemRole = MaleoMetadataSystemRoleClientService
    UserType = MaleoMetadataUserTypeClientService