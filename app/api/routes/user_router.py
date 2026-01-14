# app/api/routes/user_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any

from app.api.middleware.dependencies import get_user_service

# NOTE: Comment this out if you haven't set up your security/RBAC system yet
# from app.api.security.decorators import authorize 

# FIX: Import UserUpdateDTO here
from app.core.dto.userdto import ApiResponseDTO, UserDTO, UserResponseDTO, UserUpdateDTO
from app.core.services.user_service import UserService

class UserRouter:
    
    def __init__(self):
        self.router = APIRouter(prefix="/users", tags=["Users"])

        # -----------------------------
        # 1. CREATE USER
        # -----------------------------
        @self.router.post(
            "/create-user",
            response_model=ApiResponseDTO,
            status_code=status.HTTP_201_CREATED
        )
        # @authorize(roles=["ADMIN"], permissions=["user:create"]) # Uncomment when ready
        def create_user(
            dto: UserDTO,
            user_service: UserService = Depends(get_user_service)
        ):
            try:
                user = user_service.create_user(dto)
                # FIX: Use model_validate to safely convert DB model to Pydantic
                return ApiResponseDTO(
                    status="success",
                    message="User created successfully",
                    data=UserResponseDTO.model_validate(user)
                )
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(e)
                )

        # -----------------------------
        # 2. GET ALL USERS (MOVED HERE - SPECIFIC ROUTES FIRST!)
        # -----------------------------
        @self.router.get(
            "/get-all-users",
            response_model=ApiResponseDTO,
            status_code=status.HTTP_200_OK
        )
        def get_all_users(
            user_service: UserService = Depends(get_user_service)
        ):
            users = user_service.get_all_users()
            if users is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Something went wrong while fetching users"
                )

            # Serialize SQLAlchemy User objects to UserResponseDTOs
            user_dtos = [UserResponseDTO.model_validate(user) for user in users]

            return ApiResponseDTO(
                status="success",
                message="Users fetched successfully",
                data=user_dtos
            )

        # -----------------------------
        # 3. GET USER
        # -----------------------------
        @self.router.get(
            "/{user_id}",
            response_model=ApiResponseDTO,
            status_code=status.HTTP_200_OK
        )
        def get_user(
            user_id: str,
            user_service: UserService = Depends(get_user_service)
        ):
            user = user_service.get_user(user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            return ApiResponseDTO(
                    status="success",
                    message="User retrieved successfully",
                    data=UserResponseDTO.model_validate(user)
                )

        # -----------------------------
        # 4. PERFORM UPDATE (UPDATE)
        # When user hits this API, response shows REAL current user data
        # User can change only the fields they want
        # Only changed fields update in database, others remain unchanged
        # ----------------------------- 
        @self.router.put(
            "/{user_id}",
            response_model=ApiResponseDTO,
            status_code=status.HTTP_200_OK
        )
        def update_user(
            user_id: str,
            dto: UserUpdateDTO, 
            user_service: UserService = Depends(get_user_service)
        ):
          
            try:
                # Only fields provided in the request will be updated
                updated_user = user_service.update_user_from_dto(user_id, dto)
                
                if not updated_user:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="User not found"
                    )

                return ApiResponseDTO(
                    status="success",
                    message="User updated successfully",
                    data=UserResponseDTO.model_validate(updated_user)
                )
            except ValueError as e:
                # Catch business logic errors (e.g., duplicate email)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(e)
                )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(e)
                )

        # -----------------------------
        # 5. DELETE USER
        # -----------------------------
        @self.router.delete(
            "/{user_id}",
            response_model=ApiResponseDTO,
            status_code=status.HTTP_200_OK
        )
        def delete_user(
            user_id: str,
            user_service: UserService = Depends(get_user_service)
        ):
            success = user_service.delete_user(user_id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found or could not be deleted"
                )

            return ApiResponseDTO(
                status="success",
                message="User deleted successfully",
                data=None
            )
