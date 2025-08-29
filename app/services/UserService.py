# app/services/user_service.py
from typing import Optional, List, Dict, Any
from datetime import datetime
from passlib.context import CryptContext
from app.repositories.user_repository import user_repository
from app.models.user import User
import logging
from app.schemas.user_schema import UserCreate, UserResponse

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"])

class UserService:    
    def __init__(self):
        self.user_repo = user_repository
    
    def _hash_password(self, password: str) -> str:
        return pwd_context.hash(password)
    
    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    def create_user(self, user_data: UserCreate) -> UserResponse:
        try:
            # Check if user already exists
            existing_user = self.user_repo.get_by_email(user_data.email)
            print(existing_user)
            if existing_user:
                raise ValueError(f"User with email {user_data.email} already exists")
            
            # Check username uniqueness if provided
            if user_data.username:
                existing_username = self.user_repo.get_by_username(user_data.username)
                if existing_username:
                    raise ValueError(f"Username {user_data.username} is already taken")
            
            # Prepare user data
            user_dict = user_data.model_dump()
            user_dict["password"] = self._hash_password(user_data.password)
            user_dict["created_at"] = datetime.utcnow()
            user_dict["is_active"] = True
            
            # Create user
            user = self.user_repo.create(user_dict)
            
            logger.info(f"User created successfully: {user.email}")
            return UserResponse.model_validate(user)
            
        except Exception as e:
            logger.error(f"Failed to create user: {str(e)}")
            raise


# Create a singleton instance
user_service = UserService()