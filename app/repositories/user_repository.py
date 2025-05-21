from typing import Dict, Optional, List
from app.models.user import UserInDB, UserCreate


class UserRepository:
    
    def __init__(self):

        self.users: Dict[str, UserInDB] = {}
        self.counter = 0
    
    def create(self, user_data: UserCreate) -> UserInDB:

        for user in self.users.values():
            if user.email == user_data.email:
                return None
        

        self.counter += 1
        user_id = str(self.counter)
        

        user_in_db = UserInDB(
            id=user_id,
            name=user_data.name,
            email=user_data.email,
            password=user_data.password  # Note: This will be hashed by the service
        )
        

        self.users[user_id] = user_in_db
        return user_in_db
    
    def get_by_email(self, email: str) -> Optional[UserInDB]:
        for user in self.users.values():
            if user.email == email:
                return user
        return None
    
    def get_by_id(self, user_id: str) -> Optional[UserInDB]:
        return self.users.get(user_id)
    
    def get_all(self) -> List[UserInDB]:
        return list(self.users.values())
