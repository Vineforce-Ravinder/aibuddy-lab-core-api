
import uuid
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Date,
    DateTime,
    Text
)
from sqlalchemy.orm import Session,relationship

from sqlalchemy.sql import func
from app.infrastructure.db.session import Base



class BaseModel(Base):
    """
    Abstract base model
    This table will NOT be created in database
    """

    __abstract__ = True

    # Common fields across all models    
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)

    # ---------- Audit Fields ----------
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    created_by = Column(String(36), nullable=True)  # User ID who created this user
    updated_by = Column(String(36), nullable=True)  # User ID who last updated this user
    deleted_by = Column(String(36), nullable=True)  # User ID who deleted this user
    