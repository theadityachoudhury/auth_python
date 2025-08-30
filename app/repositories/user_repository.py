from app.repositories.base_repository import BaseRepository
from app.models.user import User, UserStatus
from app.config.database import get_db_context
from typing import List, Optional
from sqlalchemy import or_

class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)
    
    def get_by_email(self, email: str) -> Optional[User]:
        return self.get_by_field("email", email)
    
    def get_by_username(self, username: str) -> Optional[User]:
        return self.get_by_field("username", username)
    
    def get_active_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        return self.get_all(
            skip=skip, 
            limit=limit, 
            filters={"status": UserStatus.ACTIVE}
        )
    
    def search_users(self, search_term: str, limit: int = 50) -> List[User]:
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



# Create a singleton instance
user_repository = UserRepository()