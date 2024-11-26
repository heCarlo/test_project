import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.user_service import UserService
from app.services.role_service import RoleService
from app.schemas.user_schema import UserCreate, UserResponse
from app.schemas.role_schema import RoleResponse
from app.database.database import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

def test_create_user(client):
    user_data = {
        "name": "Carlos Santos",
        "email": "carlos.santos@example.com",
        "password": "password123",
        "role_id": 2
    }

    with patch.object(UserService, 'get_user_by_email', return_value=None):
        with patch.object(UserService, 'create_user', return_value={
            "id": 1,
            "name": user_data["name"],
            "email": user_data["email"]
        }):
            response = client.post("/users/", json=user_data)
    
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": user_data["name"],
        "email": user_data["email"]
    }

def test_create_user_with_existing_email(client):
    user_data = {
        "name": "Carlos Santos",
        "email": "carlos.santos@example.com",
        "password": "password123",
        "role_id": 2
    }

    with patch.object(UserService, 'get_user_by_email', return_value={"id": 1, "name": user_data["name"], "email": user_data["email"]}):
        response = client.post("/users/", json=user_data)
    
    assert response.status_code == 400
    assert response.json() == {"detail": "email already registered"}

def test_get_role_by_id(client):
    with patch.object(RoleService, 'get_role_by_id', return_value={
        "id": 2,
        "description": "Administrator role"
    }):
        response = client.get("/role/2")
        assert response.status_code == 200
        assert response.json() == {"id": 2, "description": "Administrator role"}

def test_get_role_by_id_not_found(client):
    with patch.object(RoleService, 'get_role_by_id', return_value=None):
        response = client.get("/role/999")
    
    assert response.status_code == 404
    assert response.json() == {"detail": "role not found"}
