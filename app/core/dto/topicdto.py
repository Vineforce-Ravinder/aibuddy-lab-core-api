# app/core/dto/topicdto.py

from pydantic import BaseModel, Field
from typing import List, Optional, Any
from datetime import datetime

from app.core.dto.coursedto import TopicDetailDTO

# ========================================
# TOPIC DTOs
# ========================================

class TopicDTO(BaseModel):
    id: int
    title: str
    description:str
    order:int
    details: List[TopicDetailDTO]

    class Config:
        from_attributes = True
