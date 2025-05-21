from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestUserAPI:
    def test_register_valid_user(self):
        """Test that a user with valid data can be registered via API"""
        response = client.post(
            "/api/register",
            json={
                "name": "API Test User",
                "email": "apitest@example.com",
                "password": "securepassword123"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "apitest@example.com"
        assert data["name"] == "API Test User"
        assert "password" in data  # Password should be hashed, not plaintext
    
    def test_register_duplicate_email(self):
        """Test that registering with an existing email returns an error"""
        # Register a user first
        client.post(
            "/api/register",
            json={
                "name": "Duplicate User",
                "email": "duplicate@example.com",
                "password": "securepassword123"
            }
        )
        
        # Try to register again with the same email
        response = client.post(
            "/api/register",
            json={
                "name": "Another User",
                "email": "duplicate@example.com",
                "password": "anotherpassword123"
            }
        )
        
        assert response.status_code == 400
        assert "Email already registered" in response.text
    
    def test_login_valid_credentials(self):
        """Test that login works with valid credentials"""
        # Register a user first
        client.post(
            "/api/register",
            json={
                "name": "Login Test User",
                "email": "logintest@example.com",
                "password": "securepassword123"
            }
        )
        
        # Try to login
        response = client.post(
            "/api/token",
            data={
                "username": "logintest@example.com",
                "password": "securepassword123"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_invalid_credentials(self):
        """Test that login fails with invalid credentials"""
        # Register a user first
        client.post(
            "/api/register",
            json={
                "name": "Invalid Login Test User",
                "email": "invalidlogin@example.com",
                "password": "securepassword123"
            }
        )
        
        # Try to login with wrong password
        response = client.post(
            "/api/token",
            data={
                "username": "invalidlogin@example.com",
                "password": "wrongpassword"
            }
        )
        
        assert response.status_code == 401
        assert "Invalid credentials" in response.text
    
    def test_get_current_user(self):
        """Test that the current user can be retrieved with a valid token"""
        # Register a user first
        client.post(
            "/api/register",
            json={
                "name": "Current User Test",
                "email": "currentuser@example.com",
                "password": "securepassword123"
            }
        )
        
        # Login to get token
        response = client.post(
            "/api/token",
            data={
                "username": "currentuser@example.com",
                "password": "securepassword123"
            }
        )
        
        token = response.json()["access_token"]
        
        # Get current user with token
        response = client.get(
            "/api/users/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "currentuser@example.com"
        assert data["name"] == "Current User Test"
