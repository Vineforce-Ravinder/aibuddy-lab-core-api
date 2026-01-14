# app/api/routes/module_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.middleware.dependencies import get_db
from app.core.dto.moduledto import ApiResponseDTO, ModuleDTO, ModuleResponseDTO, ModuleUpdateDTO
from app.core.services.module_service import ModuleService
from app.infrastructure.db.repositories.module_repository import ModuleRepository


class ModuleRouter:
    """API Router for Module operations"""
    
    def __init__(self):
        self.router = APIRouter(prefix="/modules", tags=["Modules"])

        @self.router.post(
            "/create",
            response_model=ApiResponseDTO,
            status_code=status.HTTP_201_CREATED,
            summary="Create a new module"
        )
        def create_module(
            dto: ModuleDTO,
            db: Session = Depends(get_db)
        ):
            """Create a new module"""
            try:
                module_repo = ModuleRepository()
                module_service = ModuleService(db, module_repo)
                module = module_service.create_module(dto)
                
                return ApiResponseDTO(
                    status="success",
                    message="Module created successfully",
                    data=ModuleResponseDTO.model_validate(module).model_dump()
                )
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(e)
                )

        @self.router.get(
            "/course/{course_id}",
            response_model=ApiResponseDTO,
            status_code=status.HTTP_200_OK,
            summary="Get modules for course"
        )
        def get_course_modules(
            course_id: str,
            db: Session = Depends(get_db)
        ):
            """Get all modules for a course"""
            try:
                module_repo = ModuleRepository()
                module_service = ModuleService(db, module_repo)
                modules = module_service.get_course_modules(course_id)
                
                return ApiResponseDTO(
                    status="success",
                    message="Modules retrieved successfully",
                    data=[ModuleResponseDTO.model_validate(m).model_dump() for m in modules]
                )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to retrieve modules"
                )

        @self.router.get(
            "/course/{course_id}/active",
            response_model=ApiResponseDTO,
            status_code=status.HTTP_200_OK,
            summary="Get active modules for course"
        )
        def get_active_course_modules(
            course_id: str,
            db: Session = Depends(get_db)
        ):
            """Get all active modules for a course"""
            try:
                module_repo = ModuleRepository()
                module_service = ModuleService(db, module_repo)
                modules = module_service.get_active_course_modules(course_id)
                
                return ApiResponseDTO(
                    status="success",
                    message="Active modules retrieved successfully",
                    data=[ModuleResponseDTO.model_validate(m).model_dump() for m in modules]
                )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to retrieve modules"
                )

        @self.router.get(
            "/{module_id}",
            response_model=ApiResponseDTO,
            status_code=status.HTTP_200_OK,
            summary="Get module by ID"
        )
        def get_module(
            module_id: str,
            db: Session = Depends(get_db)
        ):
            """Get a specific module"""
            try:
                module_repo = ModuleRepository()
                module_service = ModuleService(db, module_repo)
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
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to retrieve module"
                )

        @self.router.put(
            "/{module_id}",
            response_model=ApiResponseDTO,
            status_code=status.HTTP_200_OK,
            summary="Update module"
        )
        def update_module(
            module_id: str,
            dto: ModuleUpdateDTO,
            db: Session = Depends(get_db)
        ):
            """Update a module"""
            try:
                module_repo = ModuleRepository()
                module_service = ModuleService(db, module_repo)
                module = module_service.update_module(module_id, dto)
                
                return ApiResponseDTO(
                    status="success",
                    message="Module updated successfully",
                    data=ModuleResponseDTO.model_validate(module)
                )
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=str(e)
                )

        @self.router.delete(
            "/{module_id}",
            response_model=ApiResponseDTO,
            status_code=status.HTTP_200_OK,
            summary="Delete module"
        )
        def delete_module(
            module_id: str,
            db: Session = Depends(get_db)
        ):
            """Delete a module"""
            try:
                module_repo = ModuleRepository()
                module_service = ModuleService(db, module_repo)
                success = module_service.delete_module(module_id)
                
                if not success:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Module not found"
                    )
                
                return ApiResponseDTO(
                    status="success",
                    message="Module deleted successfully",
                    data=None
                )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to delete module"
                )
