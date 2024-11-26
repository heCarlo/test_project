import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.services.role_service import RoleService
from app.repositories.role_repository import RoleRepository

@pytest.fixture
def db_session():
    """Mock da sessão do banco de dados."""
    return MagicMock(spec=Session)

@patch.object(RoleRepository, 'get_role_by_id')
def test_get_role_by_id_success(mock_get_role_by_id, db_session):
    """Teste de sucesso para o método get_role_by_id."""
    mock_role = {"id": 1, "name": "Admin"}
    mock_get_role_by_id.return_value = mock_role

    result = RoleService.get_role_by_id(db_session, 1)

    mock_get_role_by_id.assert_called_once_with(db_session, 1)

    assert result == mock_role

@patch.object(RoleRepository, 'get_role_by_id')
def test_get_role_by_id_not_found(mock_get_role_by_id, db_session):
    """Teste de falha para o método get_role_by_id (papel não encontrado)."""
    mock_get_role_by_id.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        RoleService.get_role_by_id(db_session, 99)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "role not found"

    mock_get_role_by_id.assert_called_once_with(db_session, 99)
