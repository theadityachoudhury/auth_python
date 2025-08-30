# app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Enum as SQLEnum
from sqlalchemy.sql import func
from datetime import datetime
from enum import Enum
from app.config.database import Base
import uuid


class UserRole(str, Enum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"
    
class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING_VERIFICATION = "pending_verification"

class User(Base):    
    __tablename__ = "users"
    
    id = Column(
        String(36), 
        primary_key=True, 
        index=True,
        default=lambda: str(uuid.uuid4())
    )
    email = Column(
        String(50), 
        unique=True, 
        index=True, 
        nullable=False,
        doc="User's email address (unique)"
    )
    username = Column(
        String(50), 
        unique=True, 
        index=True, 
        nullable=True,
        doc="User's username (optional, unique)"
    )
    password = Column(
        String(255), 
        nullable=False,
        doc="Hashed password"
    )
    first_name = Column(
        String(100), 
        nullable=False,
        doc="User's first name"
    )
    last_name = Column(
        String(100), 
        nullable=False,
        doc="User's last name"
    )
    display_name = Column(
        String(100), 
        nullable=True,
        doc="User's display name (optional)"
    )
    avatar_url = Column(
        String(500), 
        nullable=True,
        doc="URL to user's avatar image (optional)"
    )
    phone_number = Column(
        String(15),
        unique=False,
        index=True,
        nullable=True,
        doc="User's phone number (optional, unique)"
    )
    date_of_birth = Column(
        DateTime, 
        nullable=True,
        doc="User's date of birth (optional)"
    )
    gender = Column(
        SQLEnum(Gender),
        nullable=True,
        doc="Gender of the user (optional)"
    )
    timezone = Column(
        String(50),
        nullable=True,
        doc="User's timezone (optional)"
    )
    locale = Column(
        String(10),
        nullable=True,
        doc="User's locale/language preference (optional)"
    )
    status = Column(
        SQLEnum(UserStatus), 
        default=UserStatus.PENDING_VERIFICATION,
        nullable=False,
        doc="Current status of the user account"
    )    
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        doc="When the user account was created",
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        doc="When the user account was last updated"
    )
    deleted_at = Column(
        DateTime(timezone=True),
        nullable=True,
        doc="When the user account was soft deleted (if applicable)"
    )
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()
    
    def to_dict(self, include_sensitive: bool = False) -> dict:
        user_dict = {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "display_name": self.display_name,
            "avatar_url": self.avatar_url,
            "phone_number": self.phone_number,
            "date_of_birth": self.date_of_birth.isoformat() if self.date_of_birth is not None else None,
            "gender": self.gender.value if self.gender is not None else None,
            "timezone": self.timezone,
            "locale": self.locale,
            "status": self.status.value if self.status is not None else None,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
        
        if include_sensitive:
            user_dict["password"] = self.password
            user_dict["deleted_at"] = self.deleted_at
        
        return user_dict
    
    def to_response(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": f"{self.first_name} {self.last_name}".strip(),
            "display_name": self.display_name,
            "avatar_url": self.avatar_url,
            "phone_number": self.phone_number,
            "date_of_birth": self.date_of_birth,
            "gender": self.gender,
            "timezone": self.timezone,
            "locale": self.locale,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }