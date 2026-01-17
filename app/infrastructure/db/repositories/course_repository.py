"""
course_repository.py

Repository for Course model database operations.
"""

import uuid
from app.infrastructure.db.models.course import Course
from app.infrastructure.db.models.module import Module
from app.infrastructure.db.models.topic import Topic
from app.infrastructure.db.models.topicdetail import TopicDetail
from app.infrastructure.db.repositories.base_repository import BaseRepository
from app.infrastructure.mappers.course_mapper import CourseMapper
from sqlalchemy.orm import Session, joinedload
from typing import Optional, List, Dict, Any


class CourseRepository(BaseRepository[Course]):
    """Repository for Course CRUD operations"""
    
    def __init__(self):
        super().__init__(Course)

    def get_by_id(self, course_id: str):
        return (
            self.db.query(Course)
            .options(
                joinedload(Course.modules)
                .joinedload(Module.topics)
                .joinedload(Topic.details)
            )
            .filter(Course.id == course_id)
            .first()
        )
    
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

    def create_or_update(self, course_dto: Dict[str, Any]) -> Course:
        """
        Create or update course with full hierarchy (modules, topics, details).
        Checks each level for existing records and updates or inserts accordingly.
        """
        course_id = course_dto.get("id")
        code = course_dto.get("code")
        
        # Find existing course by ID or code
        existing_course = None
        if course_id:
            existing_course = self.db.query(Course).filter(Course.id == course_id).first()
        elif code:
            existing_course = self.db.query(Course).filter(Course.code == code).first()
        
        try:
            if existing_course:
                # Update course fields
                existing_course.title = course_dto.get("title", existing_course.name)
                existing_course.description = course_dto.get("description", existing_course.description)
                existing_course.level = course_dto.get("level", existing_course.level)
                
                # Handle modules: update existing, create new, delete removed
                self._sync_modules(existing_course, course_dto.get("modules", []))
                
                self.db.commit()
                self.db.refresh(existing_course)
                return existing_course
            else:
                # Create new course with hierarchy
                new_course = CourseMapper.dto_to_model(course_dto)
                self.db.add(new_course)
                self.db.commit()
                self.db.refresh(new_course)
                return new_course
        except Exception as e:
            self.db.rollback()
            raise e
    
    def _sync_modules(self, course: Course, modules_data: List[Dict[str, Any]]) -> None:
        """Sync modules: update existing, create new, delete removed"""
        existing_module_ids = {m.id for m in course.modules}
        new_module_ids = {m.get("id") for m in modules_data if m.get("id")}
        
        # Delete modules not in new data
        modules_to_delete = [m for m in course.modules if m.id not in new_module_ids]
        for module in modules_to_delete:
            self.db.delete(module)
        
        # Update or create modules
        for module_data in modules_data:
            module_id = module_data.get("id")
            existing_module = next((m for m in course.modules if m.id == module_id), None)
            
            if existing_module:
                # Update module
                existing_module.title = module_data.get("title", existing_module.title)
                existing_module.description = module_data.get("description", existing_module.description)
                existing_module.order = module_data.get("order", existing_module.order)
                
                # Sync topics within module
                self._sync_topics(existing_module, module_data.get("topics", []))
            else:
                # Create new module
                new_module = CourseMapper._map_module(module_data, course.id)
                course.modules.append(new_module)
    
    def _sync_topics(self, module: Module, topics_data: List[Dict[str, Any]]) -> None:
        """Sync topics: update existing, create new, delete removed"""
        # Delete topics not in new data
        topic_ids_to_keep = {t.get("id") for t in topics_data if t.get("id")}
        topics_to_delete = [t for t in module.topics if t.id not in topic_ids_to_keep]
        for topic in topics_to_delete:
            self.db.delete(topic)
        
        # Update or create topics
        for topic_data in topics_data:
            topic_id = topic_data.get("id")
            existing_topic = next((t for t in module.topics if t.id == topic_id), None)
            
            if existing_topic:
                # Update topic
                existing_topic.title = topic_data.get("title", existing_topic.title)
                existing_topic.description = topic_data.get("description", existing_topic.description)
                existing_topic.order = topic_data.get("order", existing_topic.order)
                
                # Sync details within topic
                self._sync_topic_details(existing_topic, topic_data.get("details", []))
            else:
                # Create new topic
                new_topic = CourseMapper._map_topic(topic_data, module.id)
                module.topics.append(new_topic)
    
    def _sync_topic_details(self, topic: Topic, details_data: List[Dict[str, Any]]) -> None:
        """Sync topic details: update existing, create new, delete removed"""
        # Delete details not in new data
        detail_ids_to_keep = {d.get("id") for d in details_data if d.get("id")}
        details_to_delete = [d for d in topic.details if d.id not in detail_ids_to_keep]
        for detail in details_to_delete:
            self.db.delete(detail)
        
        # Update or create details
        for detail_data in details_data:
            detail_id = detail_data.get("id")
            existing_detail = next((d for d in topic.details if d.id == detail_id), None)
            
            if existing_detail:
                # Update detail
                existing_detail.detail_type = detail_data.get("detail_type", existing_detail.detail_type)
                existing_detail.content = detail_data.get("content", existing_detail.content)
                existing_detail.order = detail_data.get("order", existing_detail.order)
            else:
                # Create new detail
                new_detail = CourseMapper._map_detail(detail_data, topic.id)
                topic.details.append(new_detail)
