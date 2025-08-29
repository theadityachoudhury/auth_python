# app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Enum as SQLEnum
from sqlalchemy.sql import func
from datetime import datetime
from enum import Enum
from app.config.database import Base


class UserRole(str, Enum):
    """User roles enumeration."""
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"


class User(Base):
    """User model for storing user account information."""
    
    __tablename__ = "users"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Basic user information
    email = Column(
        String(255), 
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
    
    # Authentication
    password = Column(
        String(255), 
        nullable=False,
        doc="Hashed password"
    )
    
    # User status and role
    is_active = Column(
        Boolean, 
        default=True, 
        nullable=False,
        doc="Whether the user account is active"
    )
    is_verified = Column(
        Boolean, 
        default=False, 
        nullable=False,
        doc="Whether the user's email is verified"
    )
    role = Column(
        SQLEnum(UserRole), 
        default=UserRole.USER, 
        nullable=False,
        doc="User's role in the system"
    )
    
    # Optional profile information
    phone_number = Column(
        String(20), 
        nullable=True,
        doc="User's phone number (optional)"
    )
    bio = Column(
        Text, 
        nullable=True,
        doc="User's biography or description (optional)"
    )
    profile_picture_url = Column(
        String(500), 
        nullable=True,
        doc="URL to user's profile picture (optional)"
    )
    
    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        doc="When the user account was created"
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        doc="When the user account was last updated"
    )
    last_login = Column(
        DateTime(timezone=True),
        nullable=True,
        doc="When the user last logged in"
    )
    
    # Soft delete timestamp
    deleted_at = Column(
        DateTime(timezone=True),
        nullable=True,
        doc="When the user account was soft deleted (if applicable)"
    )
    
    def __repr__(self):
        """String representation of the User object."""
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"
    
    def __str__(self):
        """Human-readable string representation."""
        return f"{self.first_name} {self.last_name} ({self.email})"
    
    @property
    def full_name(self) -> str:
        """Get the user's full name."""
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def is_admin(self) -> bool:
        """Check if the user is an admin."""
        return str(self.role) == UserRole.ADMIN
    
    @property
    def is_moderator(self) -> bool:
        """Check if the user is a moderator."""
        return str(self.role) == UserRole.MODERATOR
    
    def has_permission(self, required_role: UserRole) -> bool:
        """
        Check if the user has the required role or higher permissions.
        
        Permission hierarchy: ADMIN > MODERATOR > USER
        """
        role_hierarchy = {
            UserRole.USER: 1,
            UserRole.MODERATOR: 2,
            UserRole.ADMIN: 3
        }
        
        user_level = role_hierarchy.get(UserRole[str(self.role)], 0)
        required_level = role_hierarchy.get(required_role, 0)
        
        return user_level >= required_level
    
    def to_dict(self, include_sensitive: bool = False) -> dict:
        """
        Convert the user object to a dictionary.
        
        Args:
            include_sensitive: Whether to include sensitive information like password
        """
        user_dict = {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "role": self.role.value if str(self.role) else None,
            "phone_number": self.phone_number,
            "bio": self.bio,
            "profile_picture_url": self.profile_picture_url,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "last_login": self.last_login,
        }
        
        if include_sensitive:
            user_dict["password"] = self.password
            user_dict["deleted_at"] = self.deleted_at
        
        return user_dict