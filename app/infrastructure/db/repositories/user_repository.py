
import uuid
from app.infrastructure.db.models.user import User
from sqlalchemy.orm import Session
from typing import Optional, List

from app.infrastructure.db.repositories.base_repository import BaseRepository


# ============================
# CRUD OPERATIONS (Restored)
# ============================

class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)
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
