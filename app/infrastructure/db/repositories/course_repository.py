"""
course_repository.py

Repository for Course model database operations.
"""

import uuid
from app.infrastructure.db.models.course import Course
from app.infrastructure.db.repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session
from typing import Optional, List


class CourseRepository(BaseRepository[Course]):
    """Repository for Course CRUD operations"""
    
    def __init__(self):
        super().__init__(Course)

    @staticmethod
    def get_course_by_id(db: Session, course_id: str) -> Optional[Course]:
        """Get course by ID"""
        return db.query(Course).filter(Course.id == course_id).first()

    @staticmethod
    def get_course_by_code(db: Session, code: str) -> Optional[Course]:
        """Get course by code"""
        return db.query(Course).filter(Course.code == code).first()

    @staticmethod
    def get_all_courses(db: Session, skip: int = 0, limit: int = 100) -> List[Course]:
        """Get all courses with pagination"""
        return db.query(Course).offset(skip).limit(limit).all()

    @staticmethod
    def get_active_courses(db: Session) -> List[Course]:
        """Get all active courses"""
        return db.query(Course).filter(Course.is_active == True).all()

    @staticmethod
    def get_courses_by_instructor(db: Session, instructor_id: str) -> List[Course]:
        """Get courses by instructor"""
        return db.query(Course).filter(Course.instructor_id == instructor_id).all()

    @staticmethod
    def create_course(db: Session, course_data: dict) -> Course:
        """Create new course"""
        course = Course(
            id=str(uuid.uuid4()),
            **course_data
        )
        try:
            db.add(course)
            db.commit()
            db.refresh(course)
        except Exception as e:
            db.rollback()
            raise e
        return course

    @staticmethod
    def update_course(db: Session, course_id: str, update_data: dict) -> Optional[Course]:
        """Update course"""
        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            return None
        
        for key, value in update_data.items():
            if hasattr(course, key) and value is not None:
                setattr(course, key, value)
        
        try:
            db.commit()
            db.refresh(course)
        except Exception as e:
            db.rollback()
            raise e
        return course

    @staticmethod
    def delete_course(db: Session, course_id: str) -> bool:
        """Delete course"""
        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            return False
        try:
            db.delete(course)
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        return True
