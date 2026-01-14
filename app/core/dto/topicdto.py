# app/core/dto/topicdto.py

from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime

# ========================================
# TOPIC DTOs
# ========================================

class TopicBaseDTO(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    content: Optional[str] = Field(None)
    order: Optional[int] = Field(None)
    learning_objectives: Optional[str] = Field(None)
    estimated_duration: Optional[int] = Field(None)

class TopicDTO(TopicBaseDTO):
    """DTO for creating a topic"""
    module_id: str = Field(...)

class TopicUpdateDTO(BaseModel):
    """DTO for updating a topic"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    content: Optional[str] = Field(None)
    order: Optional[int] = Field(None)
    learning_objectives: Optional[str] = Field(None)
    estimated_duration: Optional[int] = Field(None)
    is_active: Optional[bool] = Field(None)
    is_published: Optional[bool] = Field(None)

class TopicResponseDTO(TopicBaseDTO):
    """DTO for topic API response"""
    id: str
    module_id: str
    is_active: bool
    is_published: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# ========================================
# API Response Wrapper
# ========================================

class ApiResponseDTO(BaseModel):
    """Generic API Response wrapper"""
    status: str = Field(..., pattern="^(success|error)$")
    message: str
    data: Optional[Any] = None
