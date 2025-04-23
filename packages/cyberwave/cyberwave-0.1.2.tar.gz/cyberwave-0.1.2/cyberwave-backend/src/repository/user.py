from src.repository.base import CRUDBase
from src.models.user import User
from src.schemas.user import UserCreate, UserInDB # Placeholder Update schema needed later

class UserRepository(CRUDBase[User, UserCreate, UserInDB]): # Replace UserInDB with UserUpdate later
    pass

user_repo = UserRepository(User) 