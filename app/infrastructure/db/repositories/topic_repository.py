"""
topic_repository.py

Repository for Topic model database operations.
"""

import uuid
from app.infrastructure.db.models.topic import Topic
from app.infrastructure.db.repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session
from typing import Optional, List


class TopicRepository(BaseRepository[Topic]):
    """Repository for Topic CRUD operations"""
    
    def __init__(self):
        super().__init__(Topic)

    @staticmethod
    def get_topic_by_id(db: Session, topic_id: str) -> Optional[Topic]:
        """Get topic by ID"""
        return db.query(Topic).filter(Topic.id == topic_id).first()

    @staticmethod
    def get_topics_by_module(db: Session, module_id: str) -> List[Topic]:
        """Get all topics for a module"""
        return db.query(Topic).filter(Topic.module_id == module_id).order_by(Topic.order).all()

    @staticmethod
    def get_active_topics_by_module(db: Session, module_id: str) -> List[Topic]:
        """Get active topics for a module"""
        return db.query(Topic).filter(
            Topic.module_id == module_id,
            Topic.is_active == True
        ).order_by(Topic.order).all()

    @staticmethod
    def get_published_topics_by_module(db: Session, module_id: str) -> List[Topic]:
        """Get published topics for a module"""
        return db.query(Topic).filter(
            Topic.module_id == module_id,
            Topic.is_published == True
        ).order_by(Topic.order).all()

    @staticmethod
    def create_topic(db: Session, topic_data: dict) -> Topic:
        """Create new topic"""
        topic = Topic(
            id=str(uuid.uuid4()),
            **topic_data
        )
        try:
            db.add(topic)
            db.commit()
            db.refresh(topic)
        except Exception as e:
            db.rollback()
            raise e
        return topic

    @staticmethod
    def update_topic(db: Session, topic_id: str, update_data: dict) -> Optional[Topic]:
        """Update topic"""
        topic = db.query(Topic).filter(Topic.id == topic_id).first()
        if not topic:
            return None
        
        for key, value in update_data.items():
            if hasattr(topic, key) and value is not None:
                setattr(topic, key, value)
        
        try:
            db.commit()
            db.refresh(topic)
        except Exception as e:
            db.rollback()
            raise e
        return topic

    @staticmethod
    def delete_topic(db: Session, topic_id: str) -> bool:
        """Delete topic"""
        topic = db.query(Topic).filter(Topic.id == topic_id).first()
        if not topic:
            return False
        try:
            db.delete(topic)
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        return True
