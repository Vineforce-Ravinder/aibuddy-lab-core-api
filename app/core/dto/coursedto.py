# app/core/dto/coursedto.py

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Any, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from app.core.dto.moduledto import ModuleResponseDTO

# ========================================
# COURSE DTOs
# ========================================

class CourseBaseDTO(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=2000)
    instructor_id: Optional[str] = Field(None)
    duration_hours: Optional[str] = Field(None)
    level: Optional[str] = Field(None)  # beginner, intermediate, advanced

class CourseDTO(CourseBaseDTO):
    """DTO for creating a course"""
    pass

class CourseUpdateDTO(BaseModel):
    """DTO for updating a course"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=2000)
    instructor_id: Optional[str] = Field(None)
    duration_hours: Optional[str] = Field(None)
    level: Optional[str] = Field(None)
    is_active: Optional[bool] = Field(None)
    is_published: Optional[bool] = Field(None)

class CourseResponseDTO(CourseBaseDTO):
    """DTO for course API response with nested modules and topics"""
    id: str
    is_active: bool
    is_published: bool
    created_at: datetime
    updated_at: datetime
    modules: Optional[List['ModuleResponseDTO']] = None
    
    class Config:
        from_attributes = True

# Import and rebuild after ModuleResponseDTO is defined
from app.core.dto.moduledto import ModuleResponseDTO
CourseResponseDTO.model_rebuild()

# ========================================
# API Response Wrapper
# ========================================

class ApiResponseDTO(BaseModel):
    """Generic API Response wrapper"""
    status: str = Field(..., pattern="^(success|error)$")
    message: str
    data: Optional[Any] = None
