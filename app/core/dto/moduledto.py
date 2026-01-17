# app/core/dto/moduledto.py

from pydantic import BaseModel, Field
from typing import Optional, Any, List
from datetime import datetime

# ========================================
# MODULE DTOs
# ========================================

class ModuleBaseDTO(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    order: Optional[int] = Field(None)

class ModuleDTO(ModuleBaseDTO):
    """DTO for creating a module"""
    course_id: str = Field(...)

class ModuleUpdateDTO(BaseModel):
    """DTO for updating a module"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    order: Optional[int] = Field(None)
    is_active: Optional[bool] = Field(None)

class ModuleResponseDTO(ModuleBaseDTO):
    """DTO for module API response"""
    id: str
    course_id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    topics: Optional[List['TopicResponseDTOWithoutModule']] = None
    
    class Config:
        from_attributes = True

from app.core.dto.topicdto import TopicResponseDTOWithoutModule
ModuleResponseDTO.model_rebuild()

# ========================================
# API Response Wrapper
# ========================================

class ApiResponseDTO(BaseModel):
    """Generic API Response wrapper"""
    status: str = Field(..., pattern="^(success|error)$")
    message: str
    data: Optional[Any] = None
