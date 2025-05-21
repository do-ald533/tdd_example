import pytest
from fastapi import HTTPException
from app.models.user import UserCreate, UserLogin
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository


class TestUserAuthentication:
    @pytest.fixture
    def user_repository(self):
        return UserRepository()
    
    @pytest.fixture
    def user_service(self, user_repository):
        return UserService(user_repository)
    
    @pytest.fixture
    def sample_user(self):
        return UserCreate(
            name="Test User",
            email="test@example.com",
            password="securepassword123"
        )
    
    def test_register_valid_user(self, user_service, sample_user):
        user = user_service.register_user(sample_user)
        assert user.email == sample_user.email
        assert user.name == sample_user.name
        assert user.password != sample_user.password
    
    def test_register_duplicate_email(self, user_service, sample_user):

        user_service.register_user(sample_user)
        

        with pytest.raises(HTTPException) as exc_info:
            user_service.register_user(sample_user)
        
        assert exc_info.value.status_code == 400
        assert "Email already registered" in str(exc_info.value.detail)
    
    def test_login_valid_credentials(self, user_service, sample_user):

        user_service.register_user(sample_user)
        
        # Try to login
        login_data = UserLogin(email=sample_user.email, password=sample_user.password)
        token = user_service.login_user(login_data)
        
        assert token is not None
        assert len(token) > 0
    
    def test_login_invalid_email(self, user_service, sample_user):

        user_service.register_user(sample_user)
        
        # Try to login with wrong email
        login_data = UserLogin(email="wrong@example.com", password=sample_user.password)
        
        with pytest.raises(HTTPException) as exc_info:
            user_service.login_user(login_data)
        
        assert exc_info.value.status_code == 401
        assert "Invalid credentials" in str(exc_info.value.detail)
    
    def test_login_invalid_password(self, user_service, sample_user):

        user_service.register_user(sample_user)
        
        # Try to login with wrong password
        login_data = UserLogin(email=sample_user.email, password="wrongpassword")
        
        with pytest.raises(HTTPException) as exc_info:
            user_service.login_user(login_data)
        
        assert exc_info.value.status_code == 401
        assert "Invalid credentials" in str(exc_info.value.detail)
    
    def test_required_fields_validation(self, user_service):
        # Missing name
        with pytest.raises(ValueError):
            user = UserCreate(email="test@example.com", password="password123")
            user_service.register_user(user)
        
        # Missing email
        with pytest.raises(ValueError):
            user = UserCreate(name="Test User", password="password123")
            user_service.register_user(user)
        
        # Missing password
        with pytest.raises(ValueError):
            user = UserCreate(name="Test User", email="test@example.com")
            user_service.register_user(user)
