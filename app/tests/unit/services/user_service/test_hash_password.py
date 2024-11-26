from app.services.user_service import UserService

def test_hash_password():
    password = "password123"
    hashed_password = UserService.hash_password(password)
    assert hashed_password != password
    assert isinstance(hashed_password, str)
