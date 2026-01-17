# app/core/services/topic_service.py

from sqlalchemy.orm import Session
from typing import List, Optional
from app.infrastructure.db.repositories.topic_repository import TopicRepository
from app.infrastructure.db.repositories.module_repository import ModuleRepository
from app.infrastructure.db.models.topic import Topic
from app.core.dto.topicdto import TopicDTO


class TopicService:
    """Business logic for Topic operations"""
    
    def __init__(self, db: Session, topic_repo: TopicRepository):
        self.db = db
        self.topic_repo = topic_repo

    def create_topic(self, dto: TopicDTO) -> Topic:
        """Create new topic"""
        # Verify module exists
        module = ModuleRepository.get_module_by_id(self.db, dto.module_id)
        if not module:
            raise ValueError("Module not found")
        
        topic_data = dto.model_dump(exclude_none=True)
        return TopicRepository.create_topic(self.db, topic_data)

    def get_topic(self, topic_id: str) -> Optional[Topic]:
        """Get topic by ID"""
        return TopicRepository.get_topic_by_id(self.db, topic_id)

    def get_module_topics(self, module_id: str) -> List[Topic]:
        """Get all topics for module"""
        return TopicRepository.get_topics_by_module(self.db, module_id)

    def get_active_module_topics(self, module_id: str) -> List[Topic]:
        """Get active topics for module"""
        return TopicRepository.get_active_topics_by_module(self.db, module_id)

    def get_published_module_topics(self, module_id: str) -> List[Topic]:
        """Get published topics for module"""
        return TopicRepository.get_published_topics_by_module(self.db, module_id)

    def update_topic(self, topic_id: str, dto: TopicDTO) -> Topic:
        """Update topic"""
        topic = TopicRepository.get_topic_by_id(self.db, topic_id)
        if not topic:
            raise ValueError("Topic not found")
        
        update_data = dto.model_dump(exclude_none=True)
        return TopicRepository.update_topic(self.db, topic_id, update_data)

    def delete_topic(self, topic_id: str) -> bool:
        """Delete topic"""
        return TopicRepository.delete_topic(self.db, topic_id)
