"""
course_mapper_marshmallow.py

Alternative automapper using Marshmallow for schema validation and serialization
Install: pip install marshmallow
"""

from marshmallow import Schema, fields, post_load, pre_dump
from typing import Dict, Any, List, Optional
from app.infrastructure.db.models.course import Course
from app.infrastructure.db.models.module import Module
from app.infrastructure.db.models.topic import Topic
from app.infrastructure.db.models.topicdetail import TopicDetail
import uuid


# ============================================
# Schema Definitions (Nested)
# ============================================

class TopicDetailSchema(Schema):
    """Schema for TopicDetail model"""
    id = fields.Str(allow_none=True)
    detail_type = fields.Str(required=True)
    content = fields.Str(required=True)
    order = fields.Int(missing=0)
    
    @post_load
    def make_detail(self, data, **kwargs):
        """Convert to TopicDetail model"""
        return TopicDetail(
            id=data.get("id") or str(uuid.uuid4()),
            topic_id=None,  # Will be set by parent
            detail_type=data.get("detail_type"),
            content=data.get("content"),
            order=data.get("order", 0)
        )


class TopicSchema(Schema):
    """Schema for Topic model"""
    id = fields.Str(allow_none=True)
    name = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    order = fields.Int(missing=0)
    details = fields.Nested(TopicDetailSchema, many=True, missing=[])
    
    @post_load
    def make_topic(self, data, **kwargs):
        """Convert to Topic model"""
        topic = Topic(
            id=data.get("id") or str(uuid.uuid4()),
            module_id=None,  # Will be set by parent
            name=data.get("name"),
            description=data.get("description"),
            order=data.get("order", 0)
        )
        
        # Link details to topic
        details = data.get("details", [])
        for detail in details:
            detail.topic_id = topic.id
        topic.details = details
        
        return topic


class ModuleSchema(Schema):
    """Schema for Module model"""
    id = fields.Str(allow_none=True)
    name = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    order = fields.Int(missing=0)
    topics = fields.Nested(TopicSchema, many=True, missing=[])
    
    @post_load
    def make_module(self, data, **kwargs):
        """Convert to Module model"""
        module = Module(
            id=data.get("id") or str(uuid.uuid4()),
            course_id=None,  # Will be set by parent
            name=data.get("name"),
            description=data.get("description"),
            order=data.get("order", 0)
        )
        
        # Link topics to module
        topics = data.get("topics", [])
        for topic in topics:
            topic.module_id = module.id
        module.topics = topics
        
        return module


class CourseSchema(Schema):
    """Schema for Course model with full hierarchy"""
    id = fields.Str(allow_none=True)
    name = fields.Str(required=True)
    code = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    instructor_id = fields.Str(allow_none=True)
    duration_hours = fields.Str(allow_none=True)
    level = fields.Str(allow_none=True)
    modules = fields.Nested(ModuleSchema, many=True, missing=[])
    
    @post_load
    def make_course(self, data, **kwargs):
        """Convert DTO to Course model"""
        course = Course(
            id=data.get("id") or str(uuid.uuid4()),
            name=data.get("name"),
            code=data.get("code"),
            description=data.get("description"),
            instructor_id=data.get("instructor_id"),
            duration_hours=data.get("duration_hours"),
            level=data.get("level")
        )
        
        # Link modules to course
        modules = data.get("modules", [])
        for module in modules:
            module.course_id = course.id
        course.modules = modules
        
        return course


# ============================================
# Mapper Class
# ============================================

class CourseMapperMarshmallow:
    """AutoMapper using Marshmallow schemas"""
    
    # Initialize schemas
    course_schema = CourseSchema()
    module_schema = ModuleSchema()
    topic_schema = TopicSchema()
    detail_schema = TopicDetailSchema()
    
    @classmethod
    def dto_to_model(cls, course_dto: Dict[str, Any]) -> Course:
        """
        Convert DTO dict to Course model with full hierarchy
        
        Usage:
            course = CourseMapperMarshmallow.dto_to_model({
                "name": "Python 101",
                "code": "PY101",
                "modules": [...]
            })
        """
        return cls.course_schema.load(course_dto)
    
    @classmethod
    def model_to_dto(cls, course: Course) -> Dict[str, Any]:
        """Convert Course model back to DTO dict"""
        return cls.course_schema.dump(course)
    
    @classmethod
    def dto_to_module(cls, module_dto: Dict[str, Any]) -> Module:
        """Convert DTO to Module model"""
        return cls.module_schema.load(module_dto)
    
    @classmethod
    def dto_to_topic(cls, topic_dto: Dict[str, Any]) -> Topic:
        """Convert DTO to Topic model"""
        return cls.topic_schema.load(topic_dto)
    
    @classmethod
    def dto_to_detail(cls, detail_dto: Dict[str, Any]) -> TopicDetail:
        """Convert DTO to TopicDetail model"""
        return cls.detail_schema.load(detail_dto)


# ============================================
# Alternative: Using Marshmallow with validation
# ============================================

class CourseSchemaWithValidation(Schema):
    """Course schema with additional validation"""
    id = fields.Str(allow_none=True)
    name = fields.Str(required=True, validate=lambda x: len(x) > 0)
    code = fields.Str(required=True, validate=lambda x: len(x) > 0)
    description = fields.Str(allow_none=True, missing="")
    instructor_id = fields.Str(allow_none=True)
    duration_hours = fields.Str(allow_none=True)
    level = fields.Str(
        allow_none=True,
        validate=lambda x: x in ["beginner", "intermediate", "advanced"] if x else True
    )
    modules = fields.Nested(ModuleSchema, many=True, missing=[])
    
    @post_load
    def make_course(self, data, **kwargs):
        """Convert to Course with validation"""
        course = Course(
            id=data.get("id") or str(uuid.uuid4()),
            name=data.get("name"),
            code=data.get("code"),
            description=data.get("description", ""),
            instructor_id=data.get("instructor_id"),
            duration_hours=data.get("duration_hours"),
            level=data.get("level")
        )
        
        modules = data.get("modules", [])
        for module in modules:
            module.course_id = course.id
        course.modules = modules
        
        return course


class CourseMapperWithValidation:
    """AutoMapper with validation"""
    schema = CourseSchemaWithValidation()
    
    @classmethod
    def dto_to_model(cls, course_dto: Dict[str, Any]) -> Course:
        """Convert DTO to Course with validation"""
        return cls.schema.load(course_dto)
    
    @classmethod
    def validate(cls, course_dto: Dict[str, Any]) -> Dict[str, Any]:
        """Only validate without converting"""
        errors = cls.schema.validate(course_dto)
        if errors:
            raise ValueError(f"Validation errors: {errors}")
        return course_dto
