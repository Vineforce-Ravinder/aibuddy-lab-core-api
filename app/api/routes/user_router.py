
# Create a router for user endpoints
from http.client import HTTPException
from fastapi import APIRouter, Depends
from starlette import status 
from app.api.middleware.dependencies import get_user_service
from app.api.security.decorators import authorize
from app.core.dto.userdto import ApiResponseDTO, UserDTO, UserResponseDTO
from app.core.services.user_service import UserService


class UserRouter:
    
    def __init__(self):
        self.router = APIRouter(prefix="/users", tags=["Users"])


        # -----------------------------
        # CREATE USER ENDPOINT
        # -----------------------------
        @self.router.post(
            "/create-user",
            response_model=ApiResponseDTO,
            status_code=201
        )
        @authorize(
          roles=["ADMIN"],
           permissions=["user:create"]
        )
        def create_user(
            dto: UserDTO,
            user_service: UserService = Depends(get_user_service)
        ):
            """
            Create a new user.
            Input: UserDTO
            Output: ApiResponseDTO(UserResponseDTO)
            """
            try:
                user = user_service.create_user(dto)
                return ApiResponseDTO(
                    status="success",
                    message="User created successfully",
                    data=UserResponseDTO(
                        id=user.id,
                        first_name=user.first_name,
                        last_name=user.last_name,
                        email=user.email
                    )
                )
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(e)
                )