from datetime import date
import pytest
from sqlalchemy.orm import Session
from unittest.mock import patch, MagicMock
from app.services.user_service import UserService
from app.models.user_model import User
from app.repositories.user_repository import UserRepository

@pytest.fixture
def db_session():
    return MagicMock(spec=Session)

@patch.object(UserRepository, 'get_user_by_email')
def test_get_user_by_email(mock_get_user_by_email, db_session):
    mock_user = User(id=1, name="Carlos Santos", email="carlos@example.com", password="hashed_password", role_id=1, created_at=date.today())
    
    mock_get_user_by_email.return_value = mock_user

    result = UserService.get_user_by_email(db_session, "carlos@example.com")

    mock_get_user_by_email.assert_called_once_with(db_session, "carlos@example.com")

    assert result == mock_user

    mock_get_user_by_email.return_value = None

    result = UserService.get_user_by_email(db_session, "nonexistent@example.com")

    assert result is None
