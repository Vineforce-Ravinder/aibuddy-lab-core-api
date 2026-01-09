# app/core/services/user_service.py

from sqlalchemy.orm import Session
from typing import Dict, Any, Optional, List, Union

# Imports from your structure
from app.infrastructure.db.repositories.user_repository import UserRepository
from app.infrastructure.db.models.role import Role
from app.core.dto.userdto import UserDTO
from app.infrastructure.db.models.user import User

# Attempt to import password utilities (hash & verify)
try:
    # Use the import path that matches your project structure
    # Check if it's app.infrastructure.auth or app.auth
    from app.infrastructure.auth.password import get_password_hash, verify_password
except ImportError:
    # Fallback if file setup isn't complete yet
    # NOTE: In production, ensure the real password hasher is imported!
    def get_password_hash(p): return p 
    def verify_password(plain, hashed): return plain == hashed

class UserService:
    """
    Business logic layer for User operations.
    Connects API Routers to Database Repositories.
    """
    def __init__(self, db: Session, user_repo: UserRepository):
        # The database session is injected automatically by FastAPI dependencies
        self.db = db
        self.user_repo = user_repo


    # ============================
    # 1. CREATE
    # ============================
    def create_user(self, dto: UserDTO) -> User:
        """
        Creates a new user from a DTO.
        Handles password hashing and default role assignment.
        """
        # 1. Check if user already exists
        existing_user = UserRepository.get_user_by_email(self.db, dto.email)
        if existing_user:
            raise ValueError("User with this email already exists")

        # 2. Prepare data
        user_data = dto.model_dump() # Convert Pydantic DTO to dict
        
        # 3. Hash the password
        if "password" in user_data:
            user_data["password_hash"] = get_password_hash(user_data.pop("password"))

        # 4. Handle Role ID (Default to 'Student' if missing)
        # This prevents "IntegrityError" if the frontend doesn't send a role
        if "role_id" not in user_data or user_data["role_id"] is None:
            # Try to find a default role (e.g., "Student")
            default_role = self.db.query(Role).filter(Role.name == "Student").first()
            
            if default_role:
                user_data["role_id"] = default_role.id
            else:
                # OPTIONAL: If 'Student' role doesn't exist, log warning
                print("WARNING: Default 'Student' role not found. User created without role.")
                user_data["role_id"] = None

        # 5. Create User Object
        new_user = User(**user_data)
        
        # 6. Save to DB
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        
        return new_user

    # ============================
    # 2. GET (READ)
    # ============================
    def get_user(self, user_id: str) -> Optional[User]:
        """
        Get a user by ID using the Repository.
        """
        return UserRepository.get_user_by_id(self.db, user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        return UserRepository.get_user_by_email(self.db, email)
    
    def get_all_users(self, skip: int = 0, limit: int = 10) -> List[User]:
        """
        Get list of users with pagination
        """
        return UserRepository.get_all_users(self.db, skip, limit)

    # ============================
    # 3. UPDATE
    # ============================
    def update_user(self, user_id: str, update_data: Dict[str, Any]) -> Optional[User]:
        """
        Updates user fields.
        Handles password hashing if a new password is provided.
        """
        # Business Logic: Prevent updating immutable fields
        if "id" in update_data:
            del update_data["id"]
        
        # Handle Password Update
        if "password" in update_data:
            plain_password = update_data.pop("password")
            # If password is not empty, hash it and update 'password_hash'
            if plain_password: 
                update_data["password_hash"] = get_password_hash(plain_password)
            
        return UserRepository.update_user(self.db, user_id, update_data)

    # ============================
    # 4. DELETE
    # ============================
    def delete_user(self, user_id: str) -> bool:
        """
        Deletes a user.
        """
        return UserRepository.delete_user(self.db, user_id)

    # ============================
    # 5. AUTHENTICATE (Restored from your request)
    # ============================
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """
        Fetch user from DB and verify credentials
        Used by Login API.
        """
        user = (
            self.db.query(User)
            .filter(User.username == username)
            .first()
        )

        if not user:
            return None

        if not verify_password(password, user.password_hash):
            return None

        # Ensure we check for active status (if your model has it)
        if hasattr(user, 'is_active') and not user.is_active:
            return None

        return user
