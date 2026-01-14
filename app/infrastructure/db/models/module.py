"""
module.py

Module model representing a module within a course.
A module contains multiple topics.
"""

import uuid
from app.infrastructure.db.base_model import BaseModel
from sqlalchemy import (
    Column,
    String,
    Text,
    Integer,
    Boolean,
    DateTime,
    ForeignKey
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from typing import List


class Module(BaseModel):
    """
    Module table schema
    Represents a module within a course
    """

    __tablename__ = "modules"

    # ---------- Primary Key ----------
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # ---------- Foreign Key ----------
    course_id = Column(String(36), ForeignKey("courses.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # ---------- Module Information ----------
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    order = Column(Integer, nullable=True)  # Display order within course
    
    # ---------- Status ----------
    is_active = Column(Boolean, default=True, index=True)
    
    # ---------- Timestamps ----------
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # ---------- Relationships ----------
    topics = relationship("Topic", backref="module", lazy="select", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Module(id={self.id}, name={self.name}, course_id={self.course_id})>"
