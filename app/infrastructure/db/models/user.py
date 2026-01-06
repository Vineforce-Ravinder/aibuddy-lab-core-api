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
from sqlalchemy.orm import Session, relationship
from typing import Optional, List, TYPE_CHECKING

# FIX 1: TYPE_CHECKING to prevent circular import error
if TYPE_CHECKING:
    from app.infrastructure.db.models.role import Role

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
    # FIX 2: Changed to nullable=True to prevent crash if role is missing on create
    role_id = Column(
        Integer,
        ForeignKey("roles.id", ondelete="RESTRICT"),
        nullable=True 
    )

    # Many users -> one role
    role = relationship("Role", back_populates="users")


# ============================
# CRUD OPERATIONS (Restored)
# ============================

class UserRepository:
    """
    Repository class to handle all database operations for the User model.
    Follows Single Responsibility Principle for data access.
    """

    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def update_user(db: Session, user_id: str, update_data: dict) -> Optional[User]:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None

        for key, value in update_data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        try:
            db.commit()
            db.refresh(user)
        except Exception as e:
            db.rollback()
            raise e
            
        return user

    @staticmethod
    def delete_user(db: Session, user_id: str) -> bool:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False

        try:
            db.delete(user)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise e
