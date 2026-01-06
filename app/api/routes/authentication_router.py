from starlette import status
from fastapi import APIRouter, Depends
import psutil
from datetime import datetime

from app.api.middleware.dependencies import get_user_service
from app.api.security.jwt_bearer import generate_token
from app.config.authconfig import ADMIN_USER, NORMAL_USER
from app.core.dto.userdto import LoginRequest
from app.core.services.user_service import UserService


class AuthRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/connect", tags=["Authentication"])

        @self.router.post("/connect")
        def connect_admin():
            try:
                user = {
                    "sub": ADMIN_USER['id'],
                    "username": ADMIN_USER['username'],
                    "role": ADMIN_USER["role"],
                    "permissions": [
                        "user:create",
                        "user:update",
                        "user:delete",
                        "user:read",
                        "status:read"
                    ]
                }
                
                token = generate_token(user)

                return {
                    "statusCode": status.HTTP_200_OK,
                    "message": "Admin token generated successfully",
                    "response": {
                        "accessToken": f"Bearer {token}"
                    }
                }

            except Exception as ex:
                return {
                    "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": "Failed to generate admin token",
                    "response": str(ex)
                }

        
        @self.router.post("/connect-2")
            
        def connect2(
            login: LoginRequest,
            user_service: UserService = Depends(get_user_service)
        ):
            user = user_service.authenticate_user(login.username, login.password)