# app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
from enum import Enum
from .validators import UserValidators


class UserRole(str, Enum):
    """User roles enumeration."""

    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"


# Base schema with common fields
class UserBase(BaseModel):
    """Base user schema with common fields."""

    email: EmailStr = Field(..., description="User's email address")
    username: Optional[str] = Field(
        None,
        min_length=3,
        max_length=50,
        pattern="^[a-zA-Z0-9_]+$",
        description="Username (alphanumeric and underscore only)",
    )
    first_name: str = Field(..., min_length=1, max_length=100, description="First name")
    last_name: str = Field(..., min_length=1, max_length=100, description="Last name")
    phone_number: Optional[str] = Field(
        None,
        pattern=r"^[\+]?[1-9][\d]{0,15}$",
        description="Phone number in international format",
    )
    bio: Optional[str] = Field(None, max_length=1000, description="User biography")
    profile_picture_url: Optional[str] = Field(
        None, max_length=500, description="URL to profile picture"
    )

    @validator("email")
    def validate_email(cls, v):
        """Validate email format."""
        return UserValidators.validate_email(v)

    @validator("first_name", "last_name")
    def validate_names(cls, v):
        """Validate and clean name fields."""
        return UserValidators.validate_name(v)

    @validator("username")
    def validate_username(cls, v):
        """Validate username format."""
        return UserValidators.validate_username(v)

    @validator("profile_picture_url")
    def validate_profile_picture_url(cls, v):
        """Validate profile picture URL."""
        return UserValidators.validate_url(v, max_length=500)

    @validator("phone_number")
    def validate_phone_number(cls, v):
        """Validate phone number format."""
        return UserValidators.validate_phone_number(v)


# Schema for creating a new user
class UserCreate(UserBase):
    """Schema for creating a new user."""

    password: str = Field(
        ..., min_length=8, max_length=128, description="Password (minimum 8 characters)"
    )
    role: UserRole = Field(default=UserRole.USER, description="User role")

    @validator("password")
    def validate_password(cls, v):
        """Validate password strength."""
        return UserValidators.validate_password(v, require_special_char=True)


# Schema for updating user information
class UserUpdate(BaseModel):
    """Schema for updating user information."""

    email: Optional[EmailStr] = Field(None, description="New email address")
    username: Optional[str] = Field(
        None,
        min_length=3,
        max_length=50,
        pattern="^[a-zA-Z0-9_]+$",
        description="New username",
    )
    first_name: Optional[str] = Field(
        None, min_length=1, max_length=100, description="New first name"
    )
    last_name: Optional[str] = Field(
        None, min_length=1, max_length=100, description="New last name"
    )
    password: Optional[str] = Field(
        None, min_length=8, max_length=128, description="New password"
    )
    phone_number: Optional[str] = Field(
        None, pattern=r"^[\+]?[1-9][\d]{0,15}$", description="New phone number"
    )
    bio: Optional[str] = Field(None, max_length=1000, description="New biography")
    profile_picture_url: Optional[str] = Field(
        None, max_length=500, description="New profile picture URL"
    )
    is_active: Optional[bool] = Field(None, description="Account active status")
    is_verified: Optional[bool] = Field(None, description="Email verification status")
    role: Optional[UserRole] = Field(None, description="User role")

    @validator("email")
    def validate_email(cls, v):
        """Validate email format."""
        return UserValidators.validate_email(v)

    @validator("first_name", "last_name")
    def validate_names(cls, v):
        """Validate and clean name fields."""
        return UserValidators.validate_name(v)

    @validator("username")
    def validate_username(cls, v):
        """Validate username format."""
        return UserValidators.validate_username(v)

    @validator("password")
    def validate_password(cls, v):
        """Validate password strength."""
        return UserValidators.validate_password(v, require_special_char=False)

    @validator("profile_picture_url")
    def validate_profile_picture_url(cls, v):
        """Validate profile picture URL."""
        return UserValidators.validate_url(v, max_length=500)

    @validator("phone_number")
    def validate_phone_number(cls, v):
        """Validate phone number format."""
        return UserValidators.validate_phone_number(v)


# Schema for user login
class UserLogin(BaseModel):
    """Schema for user authentication."""

    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=1, description="User's password")

    @validator("email")
    def validate_email(cls, v):
        """Validate email format."""
        return UserValidators.validate_email(v)


# Schema for user response (what gets returned to the client)
class UserResponse(BaseModel):
    """Schema for user response data."""

    id: int = Field(..., description="User ID")
    email: str = Field(..., description="User's email address")
    username: Optional[str] = Field(None, description="Username")
    first_name: str = Field(..., description="First name")
    last_name: str = Field(..., description="Last name")
    full_name: Optional[str] = Field(None, description="Full name")
    phone_number: Optional[str] = Field(None, description="Phone number")
    bio: Optional[str] = Field(None, description="User biography")
    profile_picture_url: Optional[str] = Field(None, description="Profile picture URL")
    is_active: bool = Field(..., description="Whether the account is active")
    is_verified: bool = Field(..., description="Whether the email is verified")
    role: UserRole = Field(..., description="User role")
    created_at: datetime = Field(..., description="Account creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    last_login: Optional[datetime] = Field(None, description="Last login timestamp")

    class Config:
        """Pydantic configuration."""

        from_attributes = True  # Enable ORM mode for SQLAlchemy models
        json_encoders = {datetime: lambda v: v.isoformat() if v else None}

        # Example schema for API documentation
        schema_extra = {
            "example": {
                "id": 1,
                "email": "john.doe@example.com",
                "username": "johndoe",
                "first_name": "John",
                "last_name": "Doe",
                "full_name": "John Doe",
                "phone_number": "+1234567890",
                "bio": "Software developer with 5 years of experience",
                "profile_picture_url": "https://example.com/profile.jpg",
                "is_active": True,
                "is_verified": True,
                "role": "user",
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-20T14:45:00Z",
                "last_login": "2024-01-25T09:15:00Z",
            }
        }


# Schema for user summary (minimal user information)
class UserSummary(BaseModel):
    """Schema for minimal user information."""

    id: int = Field(..., description="User ID")
    email: str = Field(..., description="User's email address")
    username: Optional[str] = Field(None, description="Username")
    full_name: str = Field(..., description="Full name")
    role: UserRole = Field(..., description="User role")
    is_active: bool = Field(..., description="Whether the account is active")

    class Config:
        """Pydantic configuration."""

        from_attributes = True


# Schema for password reset request
class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""

    email: EmailStr = Field(..., description="User's email address")

    @validator("email")
    def validate_email(cls, v):
        """Validate email format."""
        return UserValidators.validate_email(v)


# Schema for password reset confirmation
class PasswordResetConfirm(BaseModel):
    """Schema for password reset confirmation."""

    token: str = Field(..., description="Reset token")
    new_password: str = Field(
        ..., min_length=8, max_length=128, description="New password"
    )

    @validator("new_password")
    def validate_password(cls, v):
        """Validate password strength."""
        return UserValidators.validate_password(v, require_special_char=False)
