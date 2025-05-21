from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.models.user import UserCreate, UserInDB, Token
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository

router = APIRouter(tags=["authentication"])


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


user_repository = UserRepository()
user_service = UserService(user_repository)


@router.post("/register", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate):
    return user_service.register_user(user_data)


@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):

    from app.models.user import UserLogin
    login_data = UserLogin(email=form_data.username, password=form_data.password)
    

    access_token = user_service.login_user(login_data)
    
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme)):
    return user_service.get_current_user(token)


@router.get("/users/me", response_model=UserInDB)
def read_users_me(current_user: UserInDB = Depends(get_current_user)):
    return current_user
