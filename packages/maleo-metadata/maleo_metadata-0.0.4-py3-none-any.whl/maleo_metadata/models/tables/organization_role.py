from sqlalchemy import Column, Integer, String
from maleo_foundation.db import DatabaseManager

class OrganizationRolesTable(DatabaseManager.Base):
    __tablename__ = "organization_roles"
    order = Column(name="order", type_=Integer)
    key = Column(name="key", type_=String(20), unique=True, nullable=False)
    name = Column(name="name", type_=String(20), unique=True, nullable=False)