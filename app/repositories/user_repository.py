from typing import Dict, Optional, List
from app.models.user import UserInDB, UserCreate


class UserRepository:
    """
    Mock repository for user data.
    In a real application, this would interact with a database.
    """
    
    def __init__(self):
        # In-memory storage for users
        self.users: Dict[str, UserInDB] = {}
        self.counter = 0
    
    def create(self, user_data: UserCreate) -> UserInDB:
        """Create a new user in the repository"""
        # Check if email already exists
        for user in self.users.values():
            if user.email == user_data.email:
                return None
        
        # Generate a simple ID
        self.counter += 1
        user_id = str(self.counter)
        
        # Create user in DB format
        user_in_db = UserInDB(
            id=user_id,
            name=user_data.name,
            email=user_data.email,
            password=user_data.password  # Note: This will be hashed by the service
        )
        
        # Store user
        self.users[user_id] = user_in_db
        return user_in_db
    
    def get_by_email(self, email: str) -> Optional[UserInDB]:
        """Get a user by email"""
        for user in self.users.values():
            if user.email == email:
                return user
        return None
    
    def get_by_id(self, user_id: str) -> Optional[UserInDB]:
        """Get a user by ID"""
        return self.users.get(user_id)
    
    def get_all(self) -> List[UserInDB]:
        """Get all users"""
        return list(self.users.values())
