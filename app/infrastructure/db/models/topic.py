"""
topic.py

Topic model representing a topic within a module.
Topics are the smallest learning units.
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


class Topic(BaseModel):
    """
    Topic table schema
    Represents a topic within a module
    """

    __tablename__ = "topics"

    # ---------- Primary Key ----------
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # ---------- Foreign Keys ----------
    module_id = Column(String(36), ForeignKey("modules.id", ondelete="CASCADE"), nullable=False, index=True)
    
    
    # ---------- Relationships ----------
    details = relationship("TopicDetail", backref="topic", lazy="select", cascade="all, delete-orphan")
    
    # ---------- Topic Information ----------
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=True)  # Rich text content
    order = Column(Integer, nullable=True)  # Display order within module
    
    # ---------- Learning Resources ----------
    learning_objectives = Column(Text, nullable=True)  # JSON list of objectives
    estimated_duration = Column(Integer, nullable=True)  # Duration in minutes
    
    # ---------- Status ----------
    is_active = Column(Boolean, default=True, index=True)
    is_published = Column(Boolean, default=False)
    
    # ---------- Timestamps ----------
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<Topic(id={self.id}, name={self.name}, module_id={self.module_id})>"
