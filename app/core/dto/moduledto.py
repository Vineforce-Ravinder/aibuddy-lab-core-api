# app/core/dto/moduledto.py

from pydantic import BaseModel, Field
from typing import Optional, Any, List
from datetime import datetime

from app.infrastructure.mappers.course_mapper_pydantic import TopicDTO

# ========================================
# MODULE DTOs
# ========================================

class ModuleDTO(BaseModel):
    id: str
    title: str
    description:str
    order:int
    topics: List[TopicDTO]

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
