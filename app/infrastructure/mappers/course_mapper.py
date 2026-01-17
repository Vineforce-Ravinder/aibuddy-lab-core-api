"""
course_mapper.py

Mapper for converting CourseDTO to Course model with full hierarchy
"""

from typing import Dict, Any
from app.infrastructure.db.models.course import Course
from app.infrastructure.db.models.module import Module
from app.infrastructure.db.models.topic import Topic
from app.infrastructure.db.models.topicdetail import TopicDetail
import uuid


class CourseMapper:
    """Mapper for converting CourseDTO to Course model with full hierarchy"""
    
    @staticmethod
    def dto_to_model(course_dto: Dict[str, Any]) -> Course:
        """Convert DTO to Course model with nested modules, topics, and details"""
        course = Course(
            id=course_dto.get("id") or str(uuid.uuid4()),
            name=course_dto.get("name"),
            code=course_dto.get("code"),
            description=course_dto.get("description"),
            instructor_id=course_dto.get("instructor_id"),
            duration_hours=course_dto.get("duration_hours"),
            level=course_dto.get("level"),
        )
        
        modules = course_dto.get("modules", [])
        course.modules = [CourseMapper._map_module(m, course.id) for m in modules]
        
        return course
    
    @staticmethod
    def _map_module(module_data: Dict[str, Any], course_id: str) -> Module:
        """Map module data to Module model"""
        module = Module(
            id=module_data.get("id") or str(uuid.uuid4()),
            course_id=course_id,
            name=module_data.get("name"),
            description=module_data.get("description"),
            order=module_data.get("order", 0)
        )
        
        topics = module_data.get("topics", [])
        module.topics = [CourseMapper._map_topic(t, module.id) for t in topics]
        
        return module
    
    @staticmethod
    def _map_topic(topic_data: Dict[str, Any], module_id: str) -> Topic:
        """Map topic data to Topic model"""
        topic = Topic(
            id=topic_data.get("id") or str(uuid.uuid4()),
            module_id=module_id,
            name=topic_data.get("name"),
            description=topic_data.get("description"),
            order=topic_data.get("order", 0)
        )
        
        details = topic_data.get("details", [])
        topic.details = [CourseMapper._map_detail(d, topic.id) for d in details]
        
        return topic
    
    @staticmethod
    def _map_detail(detail_data: Dict[str, Any], topic_id: str) -> TopicDetail:
        """Map detail data to TopicDetail model"""
        return TopicDetail(
            id=detail_data.get("id") or str(uuid.uuid4()),
            topic_id=topic_id,
            detail_type=detail_data.get("detail_type"),
            content=detail_data.get("content"),
            order=detail_data.get("order", 0)
        )
