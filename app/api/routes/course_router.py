# app/api/routes/course_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.middleware.dependencies import get_db
from app.core.dto.coursedto import ApiResponseDTO, CourseDTO, CourseResponseDTO, CourseUpdateDTO
from app.core.services.course_service import CourseService
from app.infrastructure.db.repositories.course_repository import CourseRepository


class CourseRouter:
    """API Router for Course operations"""
    
    def __init__(self):
        self.router = APIRouter(prefix="/courses", tags=["Courses"])

        @self.router.post(
            "/create",
            response_model=ApiResponseDTO,
            status_code=status.HTTP_201_CREATED,
            summary="Create a new course"
        )
        def create_course(
            dto: CourseDTO,
            db: Session = Depends(get_db)
        ):
            """Create a new course"""
            try:
                course_repo = CourseRepository()
                course_service = CourseService(db, course_repo)
                course = course_service.create_course(dto)
                
                return ApiResponseDTO(
                    status="success",
                    message="Course created successfully",
                    data=CourseResponseDTO.model_validate(course).model_dump()
                )
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(e)
                )

        @self.router.get(
            "",
            response_model=ApiResponseDTO,
            status_code=status.HTTP_200_OK,
            summary="Get all courses"
        )
        def get_all_courses(
            skip: int = 0,
            limit: int = 100,
            db: Session = Depends(get_db)
        ):
            """Get all courses with pagination"""
            try:
                course_repo = CourseRepository()
                course_service = CourseService(db, course_repo)
                courses = course_service.get_all_courses(skip, limit)
                
                return ApiResponseDTO(
                    status="success",
                    message="Courses retrieved successfully",
                    data=[CourseResponseDTO.model_validate(c) for c in courses]
                )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to retrieve courses"
                )

        @self.router.get(
            "/active",
            response_model=ApiResponseDTO,
            status_code=status.HTTP_200_OK,
            summary="Get active courses"
        )
        def get_active_courses(
            db: Session = Depends(get_db)
        ):
            """Get all active courses"""
            try:
                course_repo = CourseRepository()
                course_service = CourseService(db, course_repo)
                courses = course_service.get_active_courses()
                
                return ApiResponseDTO(
                    status="success",
                    message="Active courses retrieved successfully",
                    data=[CourseResponseDTO.model_validate(c) for c in courses]
                )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to retrieve courses"
                )

        @self.router.get(
            "/{course_id}",
            response_model=ApiResponseDTO,
            status_code=status.HTTP_200_OK,
            summary="Get course by ID"
        )
        def get_course(
            course_id: str,
            db: Session = Depends(get_db)
        ):
            """Get a specific course"""
            try:
                course_repo = CourseRepository()
                course_service = CourseService(db, course_repo)
                course = course_service.get_course(course_id)
                
                if not course:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Course not found"
                    )
                
                return ApiResponseDTO(
                    status="success",
                    message="Course retrieved successfully",
                    data=CourseResponseDTO.model_validate(course)
                )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to retrieve course"
                )

        @self.router.put(
            "/{course_id}",
            response_model=ApiResponseDTO,
            status_code=status.HTTP_200_OK,
            summary="Update course"
        )
        def update_course(
            course_id: str,
            dto: CourseUpdateDTO,
            db: Session = Depends(get_db)
        ):
            """Update a course"""
            try:
                course_repo = CourseRepository()
                course_service = CourseService(db, course_repo)
                course = course_service.update_course(course_id, dto)
                
                return ApiResponseDTO(
                    status="success",
                    message="Course updated successfully",
                    data=CourseResponseDTO.model_validate(course)
                )
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=str(e)
                )

        @self.router.delete(
            "/{course_id}",
            response_model=ApiResponseDTO,
            status_code=status.HTTP_200_OK,
            summary="Delete course"
        )
        def delete_course(
            course_id: str,
            db: Session = Depends(get_db)
        ):
            """Delete a course"""
            try:
                course_repo = CourseRepository()
                course_service = CourseService(db, course_repo)
                success = course_service.delete_course(course_id)
                
                if not success:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Course not found"
                    )
                
                return ApiResponseDTO(
                    status="success",
                    message="Course deleted successfully",
                    data=None
                )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to delete course"
                )
