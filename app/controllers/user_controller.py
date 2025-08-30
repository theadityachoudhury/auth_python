from app.services.UserService import user_service
from app.schemas.users import UserCreate, UserResponse
from app.config.database import logger
from fastapi import HTTPException, status

class UserController:    
    def __init__(self):
        self.user_service = user_service
    
    async def create_user(self, user_data: UserCreate) -> UserResponse:
        try:
            return self.user_service.create_user(user_data)
            
        except ValueError as e:
            logger.warning(f"User creation validation error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            logger.error(f"Unexpected error during user creation: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user"
            )
            
user_controller = UserController()