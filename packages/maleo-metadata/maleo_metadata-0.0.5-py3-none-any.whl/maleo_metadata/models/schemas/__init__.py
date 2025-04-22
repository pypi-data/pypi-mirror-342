from __future__ import annotations
from .blood_type import MaleoMetadataBloodTypeSchemas
from .gender import MaleoMetadataGenderSchemas
from .organization_role import MaleoMetadataOrganizationRoleSchemas
from .organization_type import MaleoMetadataOrganizationTypeSchemas
from .service import MaleoMetadataServiceSchemas
from .system_role import MaleoMetadataSystemRoleSchemas
from .user_type import MaleoMetadataUserTypeSchemas

class MaleoMetadataSchemass:
    BloodType = MaleoMetadataBloodTypeSchemas
    Genders = MaleoMetadataGenderSchemas
    OrganizationRoles = MaleoMetadataOrganizationRoleSchemas
    OrganizationTypes = MaleoMetadataOrganizationTypeSchemas
    Services = MaleoMetadataServiceSchemas
    SystemRoles = MaleoMetadataSystemRoleSchemas
    UserType = MaleoMetadataUserTypeSchemas