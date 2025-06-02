from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, foreign, remote
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql import func
from enum import Enum as PyEnum
import uuid

from app.database import Base

class ActionType(PyEnum):
    READ = "READ"
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"

class ActivityStatus(PyEnum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

class ActivityLog(Base):
    __tablename__ = "activity_logs"
    __table_args__ = (
        # Indexes
        Index('ix_activity_logs_content', 'content_type', 'object_id'),
        Index('ix_activity_logs_timestamp', 'timestamp'),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    actor_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    actor = relationship("User", back_populates="activities")
    
    action_type = Column(Enum(ActionType), nullable=False)
    status = Column(Enum(ActivityStatus), nullable=False)
    content_type = Column(String(50), nullable=True)
    object_id = Column(UUID(as_uuid=True), nullable=True)
    
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
  
    @property
    def content_object(self):
        if not self.content_type or not self.object_id:
            return None

        from app.models.registry import model_registry
        model_class = model_registry.get(self.content_type)
        if not model_class:
            return None

        from app.database import SessionLocal
        db = SessionLocal()
        try:
            return db.query(model_class).filter(model_class.id == self.object_id).first()
        finally:
            db.close()
            
    def set_content_object(self, obj):
        if obj is None:
            self.content_type = None
            self.object_id = None
        else:
            self.content_type = obj.__tablename__ 
            self.object_id = obj.id

    def __repr__(self):
        return f"<ActivityLog(id={self.id}, action={self.action_type}, object={self.content_type}:{self.object_id})>"

class GenericAssociation(Base):
    __tablename__ = 'generic_associations'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    object_id = Column(UUID(as_uuid=True), nullable=False)
    object_type = Column(String(50), nullable=False)
    
    activity_log_id = Column(UUID(as_uuid=True), ForeignKey('activity_logs.id'))
    activity_log = relationship("ActivityLog", back_populates="generic_association")

ActivityLog.generic_association = relationship(
    "GenericAssociation",
    uselist=False,
    back_populates="activity_log",
    cascade="all, delete-orphan"
)
