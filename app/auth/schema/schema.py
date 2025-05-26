import uuid
from enum import Enum
from sqlalchemy import Column, String, Enum as SQLEnum, TIMESTAMP, text, Boolean
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base
from app.auth.utils.enums import Role


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    phone = Column(String(20), unique=True, nullable=False)
    password = Column(String(60), unique=True, nullable=True)
    role = Column(SQLEnum(Role), nullable=False, default=Role.CUSTOMER)
    created_at = Column(TIMESTAMP(timezone=True), 
                       server_default=text('now()'))
    is_active = Column(Boolean, default=True)
    saved_properties =relationship("Property", back_populates="created_by")