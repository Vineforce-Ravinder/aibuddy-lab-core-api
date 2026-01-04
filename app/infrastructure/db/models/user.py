"""
user_module.py

This file contains:
1. User database schema (SQLAlchemy ORM)
2. All CRUD operations for User
3. Designed for Alembic migrations and production use

IMPORTANT:
- This is a SINGLE file implementation
- Schema and CRUD are kept together intentionally
"""

# ============================
# IMPORTS
# ============================

import uuid
from app.infrastructure.db.base_model import BaseModel
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Date,
    DateTime,
    Text,
    ForeignKey
)
from sqlalchemy.sql import func
from sqlalchemy.orm import Session,relationship
from typing import Optional, List

# ============================
# USER MODEL (SCHEMA)
# ============================

class User(BaseModel):
    """
    User table schema
    Represents a complete user profile
    """

    __tablename__ = "users"

    # ---------- Primary Key ----------
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    # ---------- Authentication ----------
    email = Column(String(150), unique=True, nullable=False, index=True)
    phone_number = Column(String(20), unique=True, nullable=True)
    password_hash = Column(String(255), nullable=False)
    last_login = Column(DateTime(timezone=True), nullable=True)

    # ---------- Profile Information ----------
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=True)
    username = Column(String(100), unique=True, nullable=True)
    gender = Column(String(20), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    profile_image = Column(Text, nullable=True)

    # ---------- Address ----------
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    pincode = Column(String(20), nullable=True)

    
    # 🔑 FOREIGN KEY
    role_id = Column(
        Integer,
        ForeignKey("roles.id", ondelete="RESTRICT"),
        nullable=False
    )

    # Many users -> one role
    role = relationship("Role", back_populates="users")    
    # ============================
