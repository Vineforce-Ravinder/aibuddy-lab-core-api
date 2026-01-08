import uuid
from app.infrastructure.db.base_model import BaseModel
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Text
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class UserRolePermission(BaseModel):
    
    __tablename__ = "user_role_permissions"

    
    # ---------- Primary Key ----------
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # 🔑 FOREIGN KEY
    # FIX 2: Changed to nullable=True to prevent crash if role is missing on create
    role_id = Column(
        Integer,
        ForeignKey("roles.id", ondelete="RESTRICT"),
        nullable=True 
    )

    # Many users -> one role
    role = relationship("Role", back_populates="users")

    
    # 🔑 FOREIGN KEY
    # FIX 2: Changed to nullable=True to prevent crash if role is missing on create
    permission_id = Column(
        Integer,
        ForeignKey("permissions.id", ondelete="RESTRICT"),
        nullable=True 
    )

    # Many users -> one permission
    permission = relationship("Permission", back_populates="users")
