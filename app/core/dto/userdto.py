from pydantic import BaseModel, EmailStr
from typing import Optional

# Input DTO
class UserDTO(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    email: EmailStr
    password: str  # You can hash this in the service

# Response DTO
class UserResponseDTO(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str]
    email: EmailStr

# Generic API Response DTO
class ApiResponseDTO(BaseModel):
    status_code: int
    status: str  # "success" / "error"
    message: str
    data: Optional[any] = None

class LoginRequest(BaseModel):
    username: str
    password: str
    