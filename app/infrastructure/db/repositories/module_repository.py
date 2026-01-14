"""
module_repository.py

Repository for Module model database operations.
"""

import uuid
from app.infrastructure.db.models.module import Module
from app.infrastructure.db.repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session
from typing import Optional, List


class ModuleRepository(BaseRepository[Module]):
    """Repository for Module CRUD operations"""
    
    def __init__(self):
        super().__init__(Module)

    @staticmethod
    def get_module_by_id(db: Session, module_id: str) -> Optional[Module]:
        """Get module by ID"""
        return db.query(Module).filter(Module.id == module_id).first()

    @staticmethod
    def get_modules_by_course(db: Session, course_id: str) -> List[Module]:
        """Get all modules for a course"""
        return db.query(Module).filter(Module.course_id == course_id).order_by(Module.order).all()

    @staticmethod
    def get_active_modules_by_course(db: Session, course_id: str) -> List[Module]:
        """Get active modules for a course"""
        return db.query(Module).filter(
            Module.course_id == course_id,
            Module.is_active == True
        ).order_by(Module.order).all()

    @staticmethod
    def create_module(db: Session, module_data: dict) -> Module:
        """Create new module"""
        module = Module(
            id=str(uuid.uuid4()),
            **module_data
        )
        try:
            db.add(module)
            db.commit()
            db.refresh(module)
        except Exception as e:
            db.rollback()
            raise e
        return module

    @staticmethod
    def update_module(db: Session, module_id: str, update_data: dict) -> Optional[Module]:
        """Update module"""
        module = db.query(Module).filter(Module.id == module_id).first()
        if not module:
            return None
        
        for key, value in update_data.items():
            if hasattr(module, key) and value is not None:
                setattr(module, key, value)
        
        try:
            db.commit()
            db.refresh(module)
        except Exception as e:
            db.rollback()
            raise e
        return module

    @staticmethod
    def delete_module(db: Session, module_id: str) -> bool:
        """Delete module"""
        module = db.query(Module).filter(Module.id == module_id).first()
        if not module:
            return False
        try:
            db.delete(module)
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        return True
