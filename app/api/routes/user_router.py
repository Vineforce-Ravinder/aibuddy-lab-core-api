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
        # 2. GET USER
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
        # 3. UPDATE USER
        # -----------------------------
        @self.router.put(
            "/{user_id}",
            response_model=ApiResponseDTO,
            status_code=status.HTTP_200_OK
        )
        def update_user(
            user_id: str,
            dto: UserUpdateDTO, # FIX: Use specific DTO so Swagger works
            user_service: UserService = Depends(get_user_service)
        ):
            """
            Update user details.
            """
            try:
                # exclude_unset=True ensures we don't erase fields we didn't send
                update_data = dto.model_dump(exclude_unset=True)
                
                updated_user = user_service.update_user(user_id, update_data)
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
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(e)
                )

        # -----------------------------
        # 4. DELETE USER
        # -----------------------------
        @self.router.get(
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

        
        # -----------------------------
        # 5. GET ALL USERS
        # -----------------------------
        @self.router.get(
            "/get-all-users",
            response_model=ApiResponseDTO,
            status_code=status.HTTP_200_OK
        )
        def get_all_users(
            user_service: UserService = Depends(get_user_service)
        ):
            success = user_service.get_all_users()
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Some thing went wrong while fetching users"
                )

            return ApiResponseDTO(
                status="success",
                message="Users fetched successfully",
                data=success
            )
