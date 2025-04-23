from maleo_foundation.enums import BaseEnums
from maleo_foundation.types import BaseTypes
from maleo_foundation.utils.logger import BaseLogger
from maleo_foundation.clients.utils.logger import ClientLoggerManager

class MaleoMetadataLoggerManager(ClientLoggerManager):
    @classmethod
    def initialize(
        cls,
        base_dir:str,
        service_name:BaseTypes.OptionalString = None,
        level:BaseEnums.LoggerLevel = BaseEnums.LoggerLevel.INFO
    ) -> BaseLogger:
        """Initialize MaleoMetadata's client logger if not already initialized."""
        return super().initialize(
            base_dir=base_dir,
            client_name="MaleoMetadata",
            service_name=service_name,
            level=level
        )

    @classmethod
    def get(cls) -> BaseLogger:
        """Return client logger (if exist) or raise Runtime Error"""
        return super().get()