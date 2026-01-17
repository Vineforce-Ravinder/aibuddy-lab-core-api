"""
course_mapper_pydantic.py

AutoMapper using Pydantic models for DTO validation and conversion
No additional packages needed - uses existing Pydantic dependency
"""

from pydantic import BaseModel, field_validator, model_validator, Field
from typing import Dict, Any, List, Optional
from app.infrastructure.db.models.course import Course
from app.infrastructure.db.models.module import Module
from app.infrastructure.db.models.topic import Topic
from app.infrastructure.db.models.topicdetail import TopicDetail
import uuid


# ============================================
# Pydantic DTO Models (with validation)
# ============================================

class TopicDetailDTO(BaseModel):
    """DTO for TopicDetail with validation"""
    id: Optional[str] = None
    detail_type: str
    content: str
    order: int = 0
    
    @field_validator("detail_type")
    @classmethod
    def validate_detail_type(cls, v):
        """Validate detail type"""
        valid_types = ["video", "reading", "quiz", "assignment", "exercise"]
        if v not in valid_types:
            raise ValueError(f"Detail type must be one of {valid_types}")
        return v
    
    def to_model(self, topic_id: str) -> TopicDetail:
        """Convert DTO to TopicDetail model"""
        return TopicDetail(
            id=self.id or str(uuid.uuid4()),
            topic_id=topic_id,
            detail_type=self.detail_type,
            content=self.content,
            order=self.order
        )
    
    model_config = {"from_attributes": True}


class TopicDTO(BaseModel):
    """DTO for Topic with validation"""
    id: Optional[str] = None
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    order: int = 0
    details: List[TopicDetailDTO] = []
    
    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        """Ensure name is not empty"""
        if not v or not v.strip():
            raise ValueError("Topic name cannot be empty")
        return v.strip()
    
    def to_model(self, module_id: str) -> Topic:
        """Convert DTO to Topic model"""
        topic = Topic(
            id=self.id or str(uuid.uuid4()),
            module_id=module_id,
            name=self.name,
            description=self.description,
            order=self.order
        )
        
        # Convert nested details
        topic.details = [detail.to_model(topic.id) for detail in self.details]
        
        return topic
    
    model_config = {"from_attributes": True}


class ModuleDTO(BaseModel):
    """DTO for Module with validation"""
    id: Optional[str] = None
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    order: int = 0
    topics: List[TopicDTO] = []
    
    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        """Ensure name is not empty"""
        if not v or not v.strip():
            raise ValueError("Module name cannot be empty")
        return v.strip()
    
    def to_model(self, course_id: str) -> Module:
        """Convert DTO to Module model"""
        module = Module(
            id=self.id or str(uuid.uuid4()),
            course_id=course_id,
            name=self.name,
            description=self.description,
            order=self.order
        )
        
        # Convert nested topics
        module.topics = [topic.to_model(module.id) for topic in self.topics]
        
        return module
    
    model_config = {"from_attributes": True}


class CourseDTO(BaseModel):
    """DTO for Course with full validation"""
    id: Optional[str] = None
    name: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=2000)
    instructor_id: Optional[str] = None
    duration_hours: Optional[str] = None
    level: Optional[str] = None
    modules: List[ModuleDTO] = []
    
    @field_validator("name", "code")
    @classmethod
    def validate_required_fields(cls, v):
        """Ensure required fields are not empty"""
        if not v or not v.strip():
            raise ValueError("Field cannot be empty")
        return v.strip()
    
    @field_validator("level")
    @classmethod
    def validate_level(cls, v):
        """Validate course level"""
        if v is None:
            return v
        valid_levels = ["beginner", "intermediate", "advanced"]
        if v not in valid_levels:
            raise ValueError(f"Level must be one of {valid_levels}")
        return v
    
    @model_validator(mode="after")
    def validate_code_format(self):
        """Validate code format (alphanumeric)"""
        if not self.code.replace("-", "").replace("_", "").isalnum():
            raise ValueError("Code must be alphanumeric (with optional - or _)")
        return self
    
    def to_model(self) -> Course:
        """Convert DTO to Course model"""
        course = Course(
            id=self.id or str(uuid.uuid4()),
            name=self.name,
            code=self.code,
            description=self.description,
            instructor_id=self.instructor_id,
            duration_hours=self.duration_hours,
            level=self.level
        )
        
        # Convert nested modules
        course.modules = [module.to_model(course.id) for module in self.modules]
        
        return course
    
    model_config = {"from_attributes": True}


# ============================================
# Mapper Class
# ============================================

class CourseMapperPydantic:
    """AutoMapper using Pydantic models"""
    
    @staticmethod
    def dto_to_model(course_data: Dict[str, Any]) -> Course:
        """
        Convert DTO dict to Course model with validation
        
        Raises ValidationError if validation fails
        
        Usage:
            try:
                course = CourseMapperPydantic.dto_to_model({
                    "name": "Python 101",
                    "code": "PY101",
                    "level": "beginner",
                    "modules": [...]
                })
            except ValueError as e:
                print(f"Validation error: {e}")
        """
        # Validate using Pydantic
        course_dto = CourseDTO(**course_data)
        
        # Convert to model
        return course_dto.to_model()
    
    @staticmethod
    def validate_only(course_data: Dict[str, Any]) -> CourseDTO:
        """Validate DTO without converting to model"""
        return CourseDTO(**course_data)
    
    @staticmethod
    def dto_to_module(module_data: Dict[str, Any], course_id: str) -> Module:
        """Convert module DTO to model"""
        module_dto = ModuleDTO(**module_data)
        return module_dto.to_model(course_id)
    
    @staticmethod
    def dto_to_topic(topic_data: Dict[str, Any], module_id: str) -> Topic:
        """Convert topic DTO to model"""
        topic_dto = TopicDTO(**topic_data)
        return topic_dto.to_model(module_id)
    
    @staticmethod
    def model_to_dto(course: Course) -> Dict[str, Any]:
        """Convert Course model to DTO dict"""
        return CourseDTO.model_validate(course).model_dump()


    @staticmethod
    def batch_validate(courses_data: List[Dict[str, Any]]) -> List[CourseDTO]:
        """Validate multiple courses at once"""
        validated = []
        errors = []
        
        for idx, course_data in enumerate(courses_data):
            try:
                validated.append(CourseDTO(**course_data))
            except ValueError as e:
                errors.append({"index": idx, "error": str(e)})
        
        if errors:
            raise ValueError(f"Batch validation failed: {errors}")
        
        return validated
