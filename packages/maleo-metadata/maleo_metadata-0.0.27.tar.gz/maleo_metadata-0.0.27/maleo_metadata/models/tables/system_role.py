from sqlalchemy import Column, Integer, String
from maleo_metadata.utils.db import MaleoMetadataDatabaseManager

class SystemRolesTable(MaleoMetadataDatabaseManager.Base):
    __tablename__ = "system_roles"
    order = Column(name="order", type_=Integer)
    key = Column(name="key", type_=String(20), unique=True, nullable=False)
    name = Column(name="name", type_=String(20), unique=True, nullable=False)