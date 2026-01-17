# app/api/routes/course_management_router.py

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.middleware.dependencies import (
    get_course_service,
    get_module_service,
    get_topic_service
)
from app.core.dto.coursedto import ApiResponseDTO, CourseDTO, CourseResponseDTO, CourseUpdateDTO
from app.core.dto.moduledto import ModuleDTO, ModuleResponseDTO, ModuleUpdateDTO
from app.core.dto.topicdto import TopicDTO, TopicResponseDTO, TopicResponseDTOWithoutModule, TopicUpdateDTO
from app.core.services.course_service import CourseService
from app.core.services.module_service import ModuleService
from app.core.services.topic_service import TopicService


class CourseManagementRouter:
    """Unified API Router for Course Management (Courses, Modules, Topics)"""
    
    def __init__(self):
        self.router = APIRouter(prefix="/courses", tags=["Course Management"])

        # =============================
        # COURSE ENDPOINTS
        # =============================
        
        @self.router.post(
            "",
            response_model=ApiResponseDTO,
            status_code=status.HTTP_201_CREATED,
            summary="Create a new course"
        )
        def create_course(
            dto: CourseDTO,
            course_service: CourseService = Depends(get_course_service)
        ):
            """Create a new course"""
            try:
                course = course_service.create_course(dto)
                return ApiResponseDTO(
                    status="success",
                    message="Course created successfully",
                    data=CourseResponseDTO.model_validate(course)
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
            course_service: CourseService = Depends(get_course_service)
        ):
            """Get all courses with pagination (includes nested modules and topics)"""
            try:
                courses = course_service.get_all_courses(skip, limit)
                courses_data = []
                for c in courses:
                    course_dto = CourseResponseDTO.model_validate(c)
                    # Load nested modules with topics
                    if c.modules:
                        modules_data = []
                        for m in c.modules:
                            module_dto = ModuleResponseDTO.model_validate(m)
                            # Load nested topics
                            if m.topics:
                                module_dto.topics = [TopicResponseDTOWithoutModule.model_validate(t) for t in m.topics]
                            modules_data.append(module_dto)
                        course_dto.modules = modules_data
                    courses_data.append(course_dto)
                return ApiResponseDTO(
                    status="success",
                    message="Courses retrieved successfully",
                    data=courses_data
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
            course_service: CourseService = Depends(get_course_service)
        ):
            """Get all active courses (includes nested modules and topics)"""
            try:
                courses = course_service.get_active_courses()
                courses_data = []
                for c in courses:
                    course_dto = CourseResponseDTO.model_validate(c)
                    # Load nested modules with topics
                    if c.modules:
                        modules_data = []
                        for m in c.modules:
                            module_dto = ModuleResponseDTO.model_validate(m)
                            # Load nested topics
                            if m.topics:
                                module_dto.topics = [TopicResponseDTOWithoutModule.model_validate(t) for t in m.topics]
                            modules_data.append(module_dto)
                        course_dto.modules = modules_data
                    courses_data.append(course_dto)
                return ApiResponseDTO(
                    status="success",
                    message="Active courses retrieved successfully",
                    data=courses_data
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
            summary="Get a specific course"
        )
        def get_course(
            course_id: str,
            course_service: CourseService = Depends(get_course_service)
        ):
            """Get a specific course by ID (includes nested modules and topics)"""
            course = course_service.get_course(course_id)
            if not course:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Course not found"
                )
            course_dto = CourseResponseDTO.model_validate(course)
            # Load nested modules with topics
            if course.modules:
                modules_data = []
                for m in course.modules:
                    module_dto = ModuleResponseDTO.model_validate(m)
                    # Load nested topics
                    if m.topics:
                        module_dto.topics = [TopicResponseDTOWithoutModule.model_validate(t) for t in m.topics]
                    modules_data.append(module_dto)
                course_dto.modules = modules_data
            return ApiResponseDTO(
                status="success",
                message="Course retrieved successfully",
                data=course_dto
            )

        @self.router.put(
            "/{course_id}",
            response_model=ApiResponseDTO,
            status_code=status.HTTP_200_OK,
            summary="Update a course"
        )
        def update_course(
            course_id: str,
            dto: CourseUpdateDTO,
            course_service: CourseService = Depends(get_course_service)
        ):
            """Update a course"""
            try:
                course = course_service.update_course(course_id, dto)
                if not course:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Course not found"
                    )
                return ApiResponseDTO(
                    status="success",
                    message="Course updated successfully",
                    data=CourseResponseDTO.model_validate(course)
                )
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(e)
                )

        @self.router.delete(
            "/{course_id}",
            response_model=ApiResponseDTO,
            status_code=status.HTTP_200_OK,
            summary="Delete a course"
        )
        def delete_course(
            course_id: str,
            course_service: CourseService = Depends(get_course_service)
        ):
            """Delete a course"""
            success = course_service.delete_course(course_id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Course not found or could not be deleted"
                )
            return ApiResponseDTO(
                status="success",
                message="Course deleted successfully",
                data=None
            )

        # =============================
        # MODULE ENDPOINTS
        # =============================
        
        @self.router.post(
            "/modules",
            response_model=ApiResponseDTO,
            status_code=status.HTTP_201_CREATED,
            summary="Create a new module"
        )
        def create_module(
            dto: ModuleDTO,
            module_service: ModuleService = Depends(get_module_service)
        ):
            """Create a new module"""
            try:
                module = module_service.create_module(dto)
                return ApiResponseDTO(
                    status="success",
                    message="Module created successfully",
                    data=ModuleResponseDTO.model_validate(module)
                )
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(e)
                )

        @self.router.get(
            "/{course_id}/modules",
            response_model=ApiResponseDTO,
            status_code=status.HTTP_200_OK,
            summary="Get modules for a course"
        )
        def get_course_modules(
            course_id: str,
            module_service: ModuleService = Depends(get_module_service)
        ):
            """Get all modules for a specific course"""
            try:
                modules = module_service.get_course_modules(course_id)
                return ApiResponseDTO(
                    status="success",
                    message="Modules retrieved successfully",
                    data=[ModuleResponseDTO.model_validate(m) for m in modules]
                )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to retrieve modules"
                )

        @self.router.get(
            "/{course_id}/modules/active",
            response_model=ApiResponseDTO,
            status_code=status.HTTP_200_OK,
            summary="Get active modules for a course"
        )
        def get_active_course_modules(
            course_id: str,
            module_service: ModuleService = Depends(get_module_service)
        ):
            """Get all active modules for a specific course"""
            try:
                modules = module_service.get_active_course_modules(course_id)
                return ApiResponseDTO(
                    status="success",
                    message="Active modules retrieved successfully",
                    data=[ModuleResponseDTO.model_validate(m) for m in modules]
                )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to retrieve modules"
                )

        @self.router.get(
            "/modules/{module_id}",
            response_model=ApiResponseDTO,
            status_code=status.HTTP_200_OK,
            summary="Get a specific module"
        )
        def get_module(
            module_id: str,
            module_service: ModuleService = Depends(get_module_service)
        ):
            """Get a specific module by ID"""
            module = module_service.get_module(module_id)
            if not module:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Module not found"
                )
            return ApiResponseDTO(
                status="success",
                message="Module retrieved successfully",
                data=ModuleResponseDTO.model_validate(module)
            )

        @self.router.put(
            "/modules/{module_id}",
            response_model=ApiResponseDTO,
            status_code=status.HTTP_200_OK,
            summary="Update a module"
        )
        def update_module(
            module_id: str,
            dto: ModuleUpdateDTO,
            module_service: ModuleService = Depends(get_module_service)
        ):
            """Update a module"""
            try:
                module = module_service.update_module(module_id, dto)
                if not module:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Module not found"
                    )
                return ApiResponseDTO(
                    status="success",
                    message="Module updated successfully",
                    data=ModuleResponseDTO.model_validate(module)
                )
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(e)
                )

        @self.router.delete(
            "/modules/{module_id}",
            response_model=ApiResponseDTO,
            status_code=status.HTTP_200_OK,
            summary="Delete a module"
        )
        def delete_module(
            module_id: str,
            module_service: ModuleService = Depends(get_module_service)
        ):
            """Delete a module"""
            success = module_service.delete_module(module_id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Module not found or could not be deleted"
                )
            return ApiResponseDTO(
                status="success",
                message="Module deleted successfully",
                data=None
            )

        # =============================
        # TOPIC ENDPOINTS
        # =============================
        
        @self.router.post(
            "/topics",
            response_model=ApiResponseDTO,
            status_code=status.HTTP_201_CREATED,
            summary="Create a new topic"
        )
        def create_topic(
            dto: TopicDTO,
            topic_service: TopicService = Depends(get_topic_service)
        ):
            """Create a new topic"""
            try:
                topic = topic_service.create_topic(dto)
                return ApiResponseDTO(
                    status="success",
                    message="Topic created successfully",
                    data=TopicResponseDTO.model_validate(topic)
                )
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(e)
                )

        @self.router.get(
            "/modules/{module_id}/topics",
            response_model=ApiResponseDTO,
            status_code=status.HTTP_200_OK,
            summary="Get topics for a module"
        )
        def get_module_topics(
            module_id: str,
            topic_service: TopicService = Depends(get_topic_service)
        ):
            """Get all topics for a specific module"""
            try:
                topics = topic_service.get_module_topics(module_id)
                return ApiResponseDTO(
                    status="success",
                    message="Topics retrieved successfully",
                    data=[TopicResponseDTO.model_validate(t) for t in topics]
                )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to retrieve topics"
                )

        @self.router.get(
            "/modules/{module_id}/topics/active",
            response_model=ApiResponseDTO,
            status_code=status.HTTP_200_OK,
            summary="Get active topics for a module"
        )
        def get_active_module_topics(
            module_id: str,
            topic_service: TopicService = Depends(get_topic_service)
        ):
            """Get all active topics for a specific module"""
            try:
                topics = topic_service.get_active_module_topics(module_id)
                return ApiResponseDTO(
                    status="success",
                    message="Active topics retrieved successfully",
                    data=[TopicResponseDTO.model_validate(t) for t in topics]
                )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to retrieve topics"
                )

        @self.router.get(
            "/modules/{module_id}/topics/published",
            response_model=ApiResponseDTO,
            status_code=status.HTTP_200_OK,
            summary="Get published topics for a module"
        )
        def get_published_module_topics(
            module_id: str,
            topic_service: TopicService = Depends(get_topic_service)
        ):
            """Get all published topics for a specific module"""
            try:
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
            "/topics/{topic_id}",
            response_model=ApiResponseDTO,
            status_code=status.HTTP_200_OK,
            summary="Get a specific topic"
        )
        def get_topic(
            topic_id: str,
            topic_service: TopicService = Depends(get_topic_service)
        ):
            """Get a specific topic by ID"""
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

        @self.router.put(
            "/topics/{topic_id}",
            response_model=ApiResponseDTO,
            status_code=status.HTTP_200_OK,
            summary="Update a topic"
        )
        def update_topic(
            topic_id: str,
            dto: TopicUpdateDTO,
            topic_service: TopicService = Depends(get_topic_service)
        ):
            """Update a topic"""
            try:
                topic = topic_service.update_topic(topic_id, dto)
                if not topic:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Topic not found"
                    )
                return ApiResponseDTO(
                    status="success",
                    message="Topic updated successfully",
                    data=TopicResponseDTO.model_validate(topic)
                )
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(e)
                )

        @self.router.delete(
            "/topics/{topic_id}",
            response_model=ApiResponseDTO,
            status_code=status.HTTP_200_OK,
            summary="Delete a topic"
        )
        def delete_topic(
            topic_id: str,
            topic_service: TopicService = Depends(get_topic_service)
        ):
            """Delete a topic"""
            success = topic_service.delete_topic(topic_id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Topic not found or could not be deleted"
                )
            return ApiResponseDTO(
                status="success",
                message="Topic deleted successfully",
                data=None
            )
