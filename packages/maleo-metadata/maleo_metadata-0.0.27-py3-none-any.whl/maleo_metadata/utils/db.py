from sqlalchemy.orm import declarative_base
from maleo_foundation.db import DatabaseManager

class MaleoMetadataDatabaseManager(DatabaseManager):
    Base = declarative_base(cls=DatabaseManager.BaseMixin)
    metadata = Base.metadata