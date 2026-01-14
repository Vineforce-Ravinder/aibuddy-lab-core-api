"""
course.py

Course model representing a learning course in the system.
A course contains multiple modules.
"""

import uuid
from app.infrastructure.db.base_model import BaseModel
from sqlalchemy import (
    Column,
    String,
    Text,
    Boolean,
    DateTime,
    ForeignKey
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from typing import List


class Course(BaseModel):
    """
    Course table schema
    Represents a complete course with modules and topics
    """

    __tablename__ = "courses"

    # ---------- Primary Key ----------
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # ---------- Course Information ----------
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    code = Column(String(50), unique=True, nullable=False)
    
    # ---------- Metadata ----------
    instructor_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    duration_hours = Column(String(100), nullable=True)
    level = Column(String(50), nullable=True)  # beginner, intermediate, advanced
    
    # ---------- Status ----------
    is_active = Column(Boolean, default=True, index=True)
    is_published = Column(Boolean, default=False)
    
    # ---------- Timestamps ----------
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # ---------- Relationships ----------
    modules = relationship("Module", backref="course", lazy="select", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Course(id={self.id}, name={self.name}, code={self.code})>"
