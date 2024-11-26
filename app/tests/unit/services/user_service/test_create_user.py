import pytest
from sqlalchemy.orm import Session
from unittest.mock import patch, MagicMock
from app.services.user_service import UserService
from app.services.role_service import RoleService
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate
from app.models.user_model import User

@pytest.fixture
def db_session():
    """Mock da sessão do banco de dados."""
    return MagicMock(spec=Session)

@patch.object(RoleService, 'get_role_by_id')
@patch.object(UserRepository, 'create_user')
def test_create_user(mock_create_user, mock_get_role_by_id, db_session):
    user_data = UserCreate(
        name="Carlos Santos",
        email="carlos@example.com",
        password="password123",
        role_id=1
    )

    mock_get_role_by_id.return_value = {"id": 1, "name": "Admin"}

    mock_create_user.return_value = User(
        id=1,
        name=user_data.name,
        email=user_data.email,
        password="hashed_password",
        role_id=user_data.role_id,
        created_at="2024-11-23T00:00:00Z" 
    )

    created_user = UserService.create_user(db_session, user_data)

    mock_get_role_by_id.assert_called_once_with(db_session, user_data.role_id)

    mock_create_user.assert_called_once()

    assert created_user.name == user_data.name
    assert created_user.email == user_data.email
    assert created_user.role_id == user_data.role_id
    assert created_user.password != user_data.password
    assert created_user.created_at == "2024-11-23T00:00:00Z"
