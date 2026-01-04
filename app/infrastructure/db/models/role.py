
import uuid
from app.infrastructure.db.base_model import BaseModel
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Text
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


# ============================
# Role MODEL (SCHEMA)
# ============================

class Role(BaseModel):
    
    __tablename__ = "roles"


    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    code = Column(Integer, unique=True, nullable=False)
    
    # One role -> many users
    users = relationship("User", back_populates="role")