from app.repositories.base_repository import BaseRepository
from app.models.user import User
from app.config.database import get_db_context
from typing import List, Optional
from sqlalchemy import or_

class UserRepository(BaseRepository[User]):
    """Repository for User model with specific user-related database operations."""
    
    def __init__(self):
        super().__init__(User)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email address."""
        return self.get_by_field("email", email)
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        return self.get_by_field("username", username)
    
    def get_active_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all active users."""
        return self.get_all(
            skip=skip, 
            limit=limit, 
            filters={"is_active": True}
        )
    
    def search_users(self, search_term: str, limit: int = 50) -> List[User]:
        """Search users by name, email, or username."""
        with get_db_context() as session:
            search_pattern = f"%{search_term}%"
            return session.query(User).filter(
                or_(
                    User.first_name.ilike(search_pattern),
                    User.last_name.ilike(search_pattern),
                    User.email.ilike(search_pattern),
                    User.username.ilike(search_pattern)
                )
            ).limit(limit).all()
    
    def get_users_by_role(self, role: str) -> List[User]:
        """Get users by their role."""
        return self.get_all(filters={"role": role})
    
    def activate_user(self, user_id: int) -> Optional[User]:
        """Activate a user account."""
        return self.update(user_id, {"is_active": True})
    
    def deactivate_user(self, user_id: int) -> Optional[User]:
        """Deactivate a user account."""
        return self.update(user_id, {"is_active": False})
    
    def update_last_login(self, user_id: int) -> Optional[User]:
        """Update user's last login timestamp."""
        from datetime import datetime
        return self.update(user_id, {"last_login": datetime.utcnow()})


# Create a singleton instance
user_repository = UserRepository()