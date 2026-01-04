from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Date,
    DateTime,
    Text
)
from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from typing import Optional, List

from app.infrastructure.db.models.user import User

class UserService:
    """
    Service class for User-related operations
    """
    def __init__(self, db: Session):
        self.db = db

    # ==================================================
    # CRUD OPERATIONS (ALL IN THIS FILE)
    # ==================================================

    # ----------------------------
    # CREATE USER
    # ----------------------------
    def create_user(db: Session, **data) -> User:
        """
        Create a new user

        :param db: SQLAlchemy session
        :param data: User fields as keyword arguments
        :return: Created User object
        """
        user = User(**data)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user


    # ----------------------------
    # READ USER BY ID
    # ----------------------------
    def get_user_by_id(self,db: Session, user_id: int) -> Optional[User]:
        """
        Fetch a user by ID (excluding deleted users)
        """
        return (
            db.query(User)
            .filter(User.id == user_id, User.is_deleted == False)
            .first()
        )


    # ----------------------------
    # READ USER BY EMAIL
    # ----------------------------
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """
        Fetch a user by email
        """
        return (
            db.query(User)
            .filter(User.email == email, User.is_deleted == False)
            .first()
        )


    # ----------------------------
    # LIST USERS
    # ----------------------------
    def list_users(
        db: Session,
        skip: int = 0,
        limit: int = 10
    ) -> List[User]:
        """
        Get list of users with pagination
        """
        return (
            db.query(User)
            .filter(User.is_deleted == False)
            .offset(skip)
            .limit(limit)
            .all()
        )


    # ----------------------------
    # UPDATE USER
    # ----------------------------
    def update_user(
            self,    
            db: Session,
            user_id: int,
            **updates
        ) -> Optional[User]:
        """
        Update user profile fields (partial update allowed)
        """
        user = self.get_user_by_id(db, user_id)
        if not user:
            return None

        for field, value in updates.items():
            if hasattr(user, field) and value is not None:
                setattr(user, field, value)

        db.commit()
        db.refresh(user)
        return user


    # ----------------------------
    # SOFT DELETE USER
    # ----------------------------
    def delete_user(self,db: Session, user_id: int) -> bool:
        """
        Soft delete a user (recommended)
        """
        user = self.get_user_by_id(db, user_id)
        if not user:
            return False

        user.is_deleted = True
        db.commit()
        return True


    # ----------------------------
    # HARD DELETE USER (OPTIONAL)
    # ----------------------------
    def hard_delete_user(db: Session, user_id: int) -> bool:
        """
        Permanently delete a user from database
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False

        db.delete(user)
        db.commit()
        return True
