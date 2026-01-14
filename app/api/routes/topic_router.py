# app/api/routes/topic_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.middleware.dependencies import get_db
from app.core.dto.topicdto import ApiResponseDTO, TopicDTO, TopicResponseDTO, TopicUpdateDTO
from app.core.services.topic_service import TopicService
from app.infrastructure.db.repositories.topic_repository import TopicRepository


class TopicRouter:
    """API Router for Topic operations"""
    
    def __init__(self):
        self.router = APIRouter(prefix="/topics", tags=["Topics"])

        @self.router.post(
            "/create",
            response_model=ApiResponseDTO,
            status_code=status.HTTP_201_CREATED,
            summary="Create a new topic"
        )
        def create_topic(
            dto: TopicDTO,
            db: Session = Depends(get_db)
        ):
            """Create a new topic"""
            try:
                topic_repo = TopicRepository()
                topic_service = TopicService(db, topic_repo)
                topic = topic_service.create_topic(dto)
                
                return ApiResponseDTO(
                    status="success",
                    message="Topic created successfully",
                    data=TopicResponseDTO.model_validate(topic).model_dump()
                )
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(e)
                )

        @self.router.get(
            "/module/{module_id}",
            response_model=ApiResponseDTO,
            status_code=status.HTTP_200_OK,
            summary="Get topics for module"
        )
        def get_module_topics(
            module_id: str,
            db: Session = Depends(get_db)
        ):
            """Get all topics for a module"""
            try:
                topic_repo = TopicRepository()
                topic_service = TopicService(db, topic_repo)
                topics = topic_service.get_module_topics(module_id)
                
                return ApiResponseDTO(
                    status="success",
                    message="Topics retrieved successfully",
                    data=[TopicResponseDTO.model_validate(t).model_dump() for t in topics]
                )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to retrieve topics"
                )

        @self.router.get(
            "/module/{module_id}/active",
            response_model=ApiResponseDTO,
            status_code=status.HTTP_200_OK,
            summary="Get active topics for module"
        )
        def get_active_module_topics(
            module_id: str,
            db: Session = Depends(get_db)
        ):
            """Get all active topics for a module"""
            try:
                topic_repo = TopicRepository()
                topic_service = TopicService(db, topic_repo)
                topics = topic_service.get_active_module_topics(module_id)
                
                return ApiResponseDTO(
                    status="success",
                    message="Active topics retrieved successfully",
                    data=[TopicResponseDTO.model_validate(t).model_dump() for t in topics]
                )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to retrieve topics"
                )

        @self.router.get(
            "/module/{module_id}/published",
            response_model=ApiResponseDTO,
            status_code=status.HTTP_200_OK,
            summary="Get published topics for module"
        )
        def get_published_module_topics(
            module_id: str,
            db: Session = Depends(get_db)
        ):
            """Get all published topics for a module"""
            try:
                topic_repo = TopicRepository()
                topic_service = TopicService(db, topic_repo)
                topics = topic_service.get_published_module_topics(module_id)
                
                return ApiResponseDTO(
                    status="success",
                    message="Published topics retrieved successfully",
                    data=[TopicResponseDTO.model_validate(t) for t in topics]
                )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to retrieve topics"
                )

        @self.router.get(
            "/{topic_id}",
            response_model=ApiResponseDTO,
            status_code=status.HTTP_200_OK,
            summary="Get topic by ID"
        )
        def get_topic(
            topic_id: str,
            db: Session = Depends(get_db)
        ):
            """Get a specific topic"""
            try:
                topic_repo = TopicRepository()
                topic_service = TopicService(db, topic_repo)
                topic = topic_service.get_topic(topic_id)
                
                if not topic:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Topic not found"
                    )
                
                return ApiResponseDTO(
                    status="success",
                    message="Topic retrieved successfully",
                    data=TopicResponseDTO.model_validate(topic)
                )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to retrieve topic"
                )

        @self.router.put(
            "/{topic_id}",
            response_model=ApiResponseDTO,
            status_code=status.HTTP_200_OK,
            summary="Update topic"
        )
        def update_topic(
            topic_id: str,
            dto: TopicUpdateDTO,
            db: Session = Depends(get_db)
        ):
            """Update a topic"""
            try:
                topic_repo = TopicRepository()
                topic_service = TopicService(db, topic_repo)
                topic = topic_service.update_topic(topic_id, dto)
                
                return ApiResponseDTO(
                    status="success",
                    message="Topic updated successfully",
                    data=TopicResponseDTO.model_validate(topic)
                )
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=str(e)
                )

        @self.router.delete(
            "/{topic_id}",
            response_model=ApiResponseDTO,
            status_code=status.HTTP_200_OK,
            summary="Delete topic"
        )
        def delete_topic(
            topic_id: str,
            db: Session = Depends(get_db)
        ):
            """Delete a topic"""
            try:
                topic_repo = TopicRepository()
                topic_service = TopicService(db, topic_repo)
                success = topic_service.delete_topic(topic_id)
                
                if not success:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Topic not found"
                    )
                
                return ApiResponseDTO(
                    status="success",
                    message="Topic deleted successfully",
                    data=None
                )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to delete topic"
                )
