

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

class TopicDetail(BaseModel):
    """
    Topic table schema
    Represents a topic within a module
    """

    __tablename__ = "topic_details"

    # ---------- Primary Key ----------
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # ---------- Foreign Keys ----------
    topic_id = Column(String(36), ForeignKey("topics.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # ---------- Topic Detail Information ----------
    detail_type = Column(String(100), nullable=False)  # e.g., "video", "quiz", "reading"
    content = Column(Text, nullable=False)  # e.g., URL for video, text for reading, etc.
    order = Column(Integer, nullable=False, default=0)  # Order of the detail within the topic
    