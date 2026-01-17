# app/core/services/module_service.py

from sqlalchemy.orm import Session
from typing import List, Optional
from app.infrastructure.db.repositories.module_repository import ModuleRepository
from app.infrastructure.db.repositories.course_repository import CourseRepository
from app.infrastructure.db.models.module import Module
from app.core.dto.moduledto import ModuleDTO


class ModuleService:
    """Business logic for Module operations"""
    
    def __init__(self, db: Session, module_repo: ModuleRepository):
        self.db = db
        self.module_repo = module_repo

    def create_module(self, dto: ModuleDTO) -> Module:
        """Create new module"""
        # Verify course exists
        course = CourseRepository.get_course_by_id(self.db, dto.course_id)
        if not course:
            raise ValueError("Course not found")
        
        module_data = dto.model_dump(exclude_none=True)
        return ModuleRepository.create_module(self.db, module_data)

    def get_module(self, module_id: str) -> Optional[Module]:
        """Get module by ID"""
        return ModuleRepository.get_module_by_id(self.db, module_id)

    def get_course_modules(self, course_id: str) -> List[Module]:
        """Get all modules for course"""
        return ModuleRepository.get_modules_by_course(self.db, course_id)

    def get_active_course_modules(self, course_id: str) -> List[Module]:
        """Get active modules for course"""
        return ModuleRepository.get_active_modules_by_course(self.db, course_id)

    def update_module(self, module_id: str, dto: ModuleDTO) -> Module:
        """Update module"""
        module = ModuleRepository.get_module_by_id(self.db, module_id)
        if not module:
            raise ValueError("Module not found")
        
        update_data = dto.model_dump(exclude_none=True)
        return ModuleRepository.update_module(self.db, module_id, update_data)

    def delete_module(self, module_id: str) -> bool:
        """Delete module"""
        return ModuleRepository.delete_module(self.db, module_id)
