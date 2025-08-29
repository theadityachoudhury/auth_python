from enum import Enum
from pydantic import EmailStr, Field, BaseModel, field_validator, model_validator
from typing import Optional
from datetime import datetime
from app.schemas.validators import UserValidators


class UserRole(str, Enum):
    ADMIN = "admin",
    MODERATOR = "moderator",
    USER = "user"

class Gender(str, Enum):
    MALE = "male",
    FEMALE = "female",
    OTHER = "other",
    PREFER_NOT_TO_SAY = "prefer_not_to_say"

class UserStatus(str, Enum):
    ACTIVE = "active",
    INACTIVE = "inactive",
    SUSPENDED = "suspended",
    PENDING_VERIFICATION = "pending_verification"


class UserBase(BaseModel):
    user_id: Optional[str] = Field(
        None,
        description="Unique identifier for a user"
    )
    email: EmailStr = Field(
        ..., 
        description="User's email address"
    )
    username: Optional[str] = Field(
        None,
        min_length=3,
        max_length=50,
        pattern="^[a-zA-Z0-9_]+$",
        description="Username (alphanumeric and underscore only)",
    )
    password: str = Field(
        ...,
        min_length = 8,
        max_length = 32,
        description="User's password"
    )
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="First Name"
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Last Name"
    )
    display_name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Last Name"
    )
    avatar_url: Optional[str] = Field(
        None,
        max_length=500,
        description="URL to profile picture"
    )
    phone_number: Optional[str] = Field(
        None,
        pattern=r"^[\+]?[1-9][\d]{0,15}$",
        description="Phone number in international format"
    )
    date_of_birth: Optional[datetime] = Field(
        None,
        description="Date of birth in YYYY-MM-DD format"
    )
    gender: Optional[Gender] = Field(
        None,
        description="Gender of the user"
    )
    timezone: Optional[str] = Field(
        None,
        description="Timezone of the user, e.g., 'America/New_York'"
    )
    locale: Optional[str] = Field(
        None,
        description="Locale of the user, e.g., 'en_US'"
    )
    status: UserStatus = Field(
        UserStatus.PENDING_VERIFICATION,
        description="Account status"
    )
    
    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        return UserValidators.validate_email(v)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        return UserValidators.validate_password(v, require_special_char=True)
    
    @field_validator("first_name", "last_name", "display_name")
    @classmethod
    def validate_names(cls, v):
        return UserValidators.validate_name(v)
    
    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        return UserValidators.validate_username(v)
    
    @field_validator("avatar_url")
    @classmethod
    def validate_avatar_url(cls, v):
        return UserValidators.validate_url(v, max_length=500)
    
    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, v):
        return UserValidators.validate_phone_number(v)

class UserCreate(UserBase):
    role: UserRole = Field(
        default=UserRole.USER,
        description="Role of the user"
    )

class UserLogin(BaseModel):
    email: Optional[EmailStr] = Field(
        None,
        description="Email address of the user"
    )
    username: Optional[str] = Field(
        None,
        min_length=3,
        max_length=50,
        description="Username (alphanumeric and underscore only)",
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=32,
        description="Password for the user"
    )

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        return UserValidators.validate_email(v)

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        return UserValidators.validate_username(v)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        return UserValidators.validate_password(v, require_special_char=True)

    # Checking for whether both username or password is empty. If empty then send error response
    @model_validator(mode='before')
    @classmethod
    def check_username_or_email(cls,data):
        if isinstance(data,dict):
            email = data.get('email')
            username = data.get('username')

            #check if both username and email are empty/None
            if not email or not username:
                raise ValueError('Either email or username must be provided')

        return data

class UserResponse(BaseModel):
    user_id: str = Field(
        ...,
        description="Unique identifier for a user"
    )
    email: EmailStr = Field(
        ...,
        description="User's email address"
    )
    username: str = Field(
        ...,
        description="User's username"
    )
    first_name: str = Field(
        ...,
        description="User's first name"
    )
    last_name: str = Field(
        ...,
        description="User's last name"
    )