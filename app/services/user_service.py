from fastapi import HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from typing import Optional
from app.models.user import UserCreate, UserInDB, UserLogin, TokenData
from app.repositories.user_repository import UserRepository

# Security configuration
SECRET_KEY = "a_very_secret_key_that_should_be_in_env_variables"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against a hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """Hash a password"""
        return pwd_context.hash(password)
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def register_user(self, user_data: UserCreate) -> UserInDB:
        """Register a new user"""
        # Check if email already exists
        existing_user = self.repository.get_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash the password
        hashed_password = self.get_password_hash(user_data.password)
        
        # Create user with hashed password
        user_with_hashed_pwd = UserCreate(
            name=user_data.name,
            email=user_data.email,
            password=hashed_password
        )
        
        # Save user to repository
        user = self.repository.create(user_with_hashed_pwd)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user"
            )
            
        return user
    
    def login_user(self, login_data: UserLogin) -> str:
        """Authenticate a user and return an access token"""
        # Get user by email
        user = self.repository.get_by_email(login_data.email)
        
        # Check if user exists and password is correct
        if not user or not self.verify_password(login_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(
            data={"sub": user.email},
            expires_delta=access_token_expires
        )
        
        return access_token
    
    def get_current_user(self, token: str) -> UserInDB:
        """Get the current user from a JWT token"""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            # Decode the JWT token
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            
            if email is None:
                raise credentials_exception
                
            token_data = TokenData(email=email)
        except JWTError:
            raise credentials_exception
            
        # Get the user from the repository
        user = self.repository.get_by_email(token_data.email)
        
        if user is None:
            raise credentials_exception
            
        return user
