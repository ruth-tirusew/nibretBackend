import uuid
from datetime import datetime
from math import radians, sin, cos, sqrt, atan2
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, UniqueConstraint, \
    DECIMAL, Integer, Boolean, Float, Enum, func, event
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship, sessionmaker

from app.auth.schema import User
from app.database import Base
from app.properties.utils.enums import PropertyType, OwnerType


class TranslateModel(Base):
    __abstract__ = True
    
    name = Column(String)
    tr_name = Column(String, nullable=True)
    description = Column(Text)
    tr_description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class HomeOwners(TranslateModel):
    __tablename__ = 'home_owners'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(Enum(OwnerType), default=OwnerType.REGULAR)
    
    properties = relationship("Property", back_populates="owner")

class Location(TranslateModel):
    __tablename__ = 'locations'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    longitude = Column(DECIMAL(precision=25, scale=20))
    latitude = Column(DECIMAL(precision=25, scale=20))
    
    property = relationship("Property", back_populates="location", uselist=False)

    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):
        R = 6371  # Earth radius in km
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        return R * c

    @classmethod
    def find_nearby_places(cls, session, latitude, longitude, radius_km):
        places = session.query(cls).all()
        return [
            place for place in places
            if cls.calculate_distance(
                latitude,
                longitude,
                float(place.latitude),
                float(place.longitude)
            ) <= radius_km
        ]

class Property(TranslateModel):
    __tablename__ = 'properties'
        
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    location_id = Column(UUID(as_uuid=True), ForeignKey('locations.id'), unique=True)
    price = Column(Float)
    bedroom = Column(Integer, default=0)
    bathroom = Column(Integer, default=0)
    area = Column(Float)
    currency = Column(String, default="ETB")
    discount = Column(Float)
    sold_out = Column(Boolean, default=False)
    owner_id = Column(UUID(as_uuid=True), ForeignKey('home_owners.id'))
    is_store = Column(Boolean, default=False)
    type = Column(Enum(PropertyType))
    move_in_date = Column(DateTime)
    rental = Column(Boolean, default=False)
    furnished = Column(Boolean, default=False)
    created_by_id = Column(UUID(as_uuid=True), ForeignKey('user_accounts.id'))
    impression_count = Column(Integer, default=0)

    created_by_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    location = relationship("Location", back_populates="property")
    owner = relationship("HomeOwners", back_populates="properties")
    created_by = relationship("User", back_populates="saved_properties")
    pictures = relationship("Image", back_populates="property")

    def increment_impression(self, session):
        session.query(Property).filter(Property.id == self.id).update(
            {Property.impression_count: Property.impression_count + 1},
            synchronize_session=False
        )
        session.refresh(self)

class Image(Base):
    __tablename__ = 'images'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True
    )
    is_cover = Column(Boolean, default=False)
    image_url = Column(String(255))
    blur_hash = Column(Text, nullable=True)

    property_id = Column(UUID(as_uuid=True), ForeignKey('properties.id'))
    property = relationship("Property", back_populates="pictures")

    def __repr__(self):
        return f"<Image for {self.property.name if self.property else 'Unknown Property'}>"

   


@event.listens_for(TranslateModel, 'before_update', propagate=True)
def update_updated_at(mapper, connection, target):
    target.updated_at = datetime.utcnow()
