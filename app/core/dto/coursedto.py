# app/core/dto/coursedto.py

from app.core.dto.moduledto import ModuleDTO
from app.utility.app_enum import TopicDetailType
from pydantic import BaseModel, Field ,ConfigDict
from typing import Optional, List, Any,TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from app.core.dto.moduledto import ModuleResponseDTO

# ========================================
# COURSE DTOs
# ========================================

class CourseDTO(BaseModel):
    course_id: str = Field(...)
    title: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=2000)
    level: Optional[str] = Field(None)  # beginner, intermediate, advanced
    modules: List[ModuleDTO] = []



class TopicDetailDTO(BaseModel):
    id: int
    type: TopicDetailType
    content: str
    order:int

    class Config:
        from_attributes = True



class CourseDTO(BaseModel):
    id: str
    code:str
    title:str
    description:str
    modules: List[ModuleDTO]

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
