# app/core/services/course_service.py

from sqlalchemy.orm import Session
from typing import List, Optional
from app.infrastructure.db.repositories.course_repository import CourseRepository
from app.infrastructure.db.repositories.user_repository import UserRepository
from app.infrastructure.db.models.course import Course
from app.core.dto.coursedto import CourseDTO, CourseUpdateDTO


class CourseService:
    """Business logic for Course operations"""
    
    def __init__(self, db: Session, course_repo: CourseRepository):
        self.db = db
        self.course_repo = course_repo

    def create_course(self, dto: CourseDTO) -> Course:
        """Create new course"""
        # Check if code already exists
        existing = CourseRepository.get_course_by_code(self.db, dto.code)
        if existing:
            raise ValueError(f"Course with code {dto.code} already exists")
        
        # Validate instructor_id if provided
        if dto.instructor_id:
            instructor = UserRepository.get_user_by_id(self.db, dto.instructor_id)
            if not instructor:
                raise ValueError(f"Instructor with ID {dto.instructor_id} does not exist")
        
        course_data = dto.model_dump(exclude_none=True)
        return CourseRepository.create_course(self.db, course_data)

    def get_course(self, course_id: str) -> Optional[Course]:
        """Get course by ID"""
        return CourseRepository.get_course_by_id(self.db, course_id)

    def get_all_courses(self, skip: int = 0, limit: int = 100) -> List[Course]:
        """Get all courses"""
        return CourseRepository.get_all_courses(self.db, skip, limit)

    def get_active_courses(self) -> List[Course]:
        """Get active courses"""
        return CourseRepository.get_active_courses(self.db)

    def get_instructor_courses(self, instructor_id: str) -> List[Course]:
        """Get courses by instructor"""
        return CourseRepository.get_courses_by_instructor(self.db, instructor_id)

    def update_course(self, course_id: str, dto: CourseUpdateDTO) -> Course:
        """Update course"""
        course = CourseRepository.get_course_by_id(self.db, course_id)
        if not course:
            raise ValueError("Course not found")
        
        # Check if new code conflicts
        if dto.code and dto.code != course.code:
            existing = CourseRepository.get_course_by_code(self.db, dto.code)
            if existing:
                raise ValueError(f"Course with code {dto.code} already exists")
        
        # Validate instructor_id if provided
        if dto.instructor_id:
            instructor = UserRepository.get_user_by_id(self.db, dto.instructor_id)
            if not instructor:
                raise ValueError(f"Instructor with ID {dto.instructor_id} does not exist")
        
        update_data = dto.model_dump(exclude_none=True)
        return CourseRepository.update_course(self.db, course_id, update_data)

    def delete_course(self, course_id: str) -> bool:
        """Delete course"""
        return CourseRepository.delete_course(self.db, course_id)
