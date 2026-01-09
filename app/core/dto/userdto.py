# app/core/dto/userdto.py

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Any
from datetime import date

# --------------------------------------------------------
# 1. Base DTO (Shared Fields)
# --------------------------------------------------------
class UserBaseDTO(BaseModel):
    # Authentication
    email: EmailStr
    phone_number: Optional[str] = Field(None, pattern=r'^\+?[1-9]\d{1,14}$')
    
    # Profile Information
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    username: Optional[str] = Field(None, min_length=1, max_length=100)
    gender: Optional[str] = Field(None, max_length=20)
    date_of_birth: Optional[date] = None
    profile_image: Optional[str] = None
    
    # Address
    address: Optional[str] = None
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    pincode: Optional[str] = Field(None, max_length=20)

# --------------------------------------------------------
# 2. Input DTOs
# --------------------------------------------------------

# For CREATING a user (Password is required)
class UserDTO(UserBaseDTO):
    password: str = Field(..., min_length=8)
    role_id: Optional[int] = None 

# For UPDATING a user (Everything is optional)
class UserUpdateDTO(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = Field(None, pattern=r'^\+?[1-9]\d{1,14}$')
    password: Optional[str] = Field(None, min_length=8)  # New password (optional)
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "phone_number": "+14155552671",
                "password": None
            }
        }

# DTO for Login (Added from upstream)
class LoginRequest(BaseModel):
    username: str
    password: str

# --------------------------------------------------------
# 3. Output DTOs (Response)
# --------------------------------------------------------

class UserResponseDTO(UserBaseDTO):
    id: str  # FIX: UUID string, NOT int
    is_active: bool = True
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "41a1c6e4-8676-46cb-975f-1fbe2cf3dad0",
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "phone_number": "+14155552671",
                "is_active": True
            }
        }

# --------------------------------------------------------
# 4. API Wrapper
# --------------------------------------------------------

class ApiResponseDTO(BaseModel):
    # status_code: int # Removed status_code (usually redundant in body if HTTP header is 200)
    status: str
    message: str
    data: Optional[Any] = None  # Corrected to uppercase Any
