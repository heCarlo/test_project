import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base 
from app.models.role_model import Role
from app.repositories.role_repository import RoleRepository

@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def sample_role(db_session):
    role = Role(description="Test Role")
    db_session.add(role)
    db_session.commit()
    db_session.refresh(role)
    return role

def test_get_role_by_id(db_session, sample_role):
    role = RoleRepository.get_role_by_id(db_session, sample_role.id)
    
    assert role is not None
    assert role.id == sample_role.id
    assert role.description == "Test Role"
