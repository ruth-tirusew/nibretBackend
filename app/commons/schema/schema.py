from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime, Text, DECIMAL
from sqlalchemy.orm import relationship, sessionmaker
import uuid

from app.database import Base


class TranslateModel(Base):
    __abstract__ = True
    
    name = Column(String)
    tr_name = Column(String, nullable=True)
    description = Column(Text)
    tr_description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Location(TranslateModel):
    __tablename__ = 'locations'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    longitude = Column(DECIMAL(precision=25, scale=20))
    latitude = Column(DECIMAL(precision=25, scale=20))
    
    property = relationship("Property", back_populates="location", uselist=False)
    auction = relationship("Auctions", back_populates="location", uselist=False)


