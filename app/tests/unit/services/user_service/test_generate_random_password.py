import pytest
from app.services.user_service import UserService

def test_generate_random_password():
    password = UserService.generate_random_password(12)
    assert len(password) == 12
    assert all(c.isalnum() for c in password)