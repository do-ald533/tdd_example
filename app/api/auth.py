from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.models.user import UserCreate, UserInDB, Token
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository

router = APIRouter(tags=["authentication"])

# Dependency
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Create a single instance of the repository to be used across requests
user_repository = UserRepository()
user_service = UserService(user_repository)


@router.post("/register", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate):
    """Register a new user"""
    return user_service.register_user(user_data)


@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login and get access token"""
    # Convert form data to our login model
    from app.models.user import UserLogin
    login_data = UserLogin(email=form_data.username, password=form_data.password)
    
    # Authenticate user
    access_token = user_service.login_user(login_data)
    
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get the current authenticated user"""
    return user_service.get_current_user(token)


@router.get("/users/me", response_model=UserInDB)
def read_users_me(current_user: UserInDB = Depends(get_current_user)):
    """Get current user information"""
    return current_user
