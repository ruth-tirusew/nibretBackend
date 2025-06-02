import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer, Boolean, Float, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base
from app.auctions.utils.enums import StatusEnum

class AuctionImages(Base):
    __tablename__ = 'auction_images'

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
    auction_id = Column(UUID(as_uuid=True), ForeignKey('auctions.id'))
    auction = relationship("Auctions", back_populates="pictures")

class Auctions(Base):
    __tablename__ = "auctions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    starting_bid = Column(Float, nullable=False)
    start_date = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    end_date = Column(DateTime(timezone=True), nullable=False)
    status = Column(
        Enum(StatusEnum),
        nullable=False,
        default=StatusEnum.PENDING,
        server_default="PENDING"
    )
    impression_count = Column(Integer, nullable=False, default=0, server_default="0")
    location_id = Column(UUID(as_uuid=True), ForeignKey("locations.id"), unique=True)
    location = relationship("Location", back_populates="auction")
    pictures = relationship(
        "AuctionImages", 
        back_populates="auction",
        cascade="all, delete-orphan"
    )

    def increment_impression(self, session):
        from sqlalchemy import update
        stmt = (
            update(Auction)
            .where(Auction.id == self.id)
            .values(impression_count=Auction.impression_count + 1)
        )
        session.execute(stmt)
        session.refresh(self)
