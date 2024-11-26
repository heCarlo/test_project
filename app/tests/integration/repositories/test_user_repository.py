import pytest
from datetime import date
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.models.base import Base
from app.models.user_model import User
from app.models.role_model import Role
from app.models.claim_model import Claim
from app.models.user_claim_model import UserClaim
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

@pytest.fixture
def db_session():
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

@pytest.fixture
def sample_roles(db_session):
    role_admin = Role(description="Administrador")
    role_user = Role(description="Usuário Padrão")
    db_session.add(role_admin)
    db_session.add(role_user)
    db_session.commit()
    db_session.refresh(role_admin)
    db_session.refresh(role_user)
    return role_admin, role_user

@pytest.fixture
def sample_claims(db_session):
    claim_view_reports = Claim(description="Visualizar Relatórios", active=True)
    claim_edit_data = Claim(description="Editar Dados", active=True)
    claim_delete_records = Claim(description="Excluir Registros", active=True)
    db_session.add(claim_view_reports)
    db_session.add(claim_edit_data)
    db_session.add(claim_delete_records)
    db_session.commit()
    db_session.refresh(claim_view_reports)
    db_session.refresh(claim_edit_data)
    db_session.refresh(claim_delete_records)
    return claim_view_reports, claim_edit_data, claim_delete_records

@pytest.fixture
def sample_users(db_session, sample_roles, sample_claims):
    role_admin, role_user = sample_roles
    claim_view_reports, claim_edit_data, claim_delete_records = sample_claims

    user_carlos = User(
        name="Carlos Henrique",
        email="carlos@example.com",
        password="password123",
        role_id=role_admin.id,
        created_at=date.today(),
        updated_at=date.today()
    )
    user_gabrielly = User(
        name="Gabrielly Nunes",
        email="gabrielly@example.com",
        password="password123",
        role_id=role_user.id,
        created_at=date.today(),
        updated_at=date.today()
    )
    db_session.add(user_carlos)
    db_session.add(user_gabrielly)
    db_session.commit()
    db_session.refresh(user_carlos)
    db_session.refresh(user_gabrielly)

    user_claim_carlos_1 = UserClaim(user_id=user_carlos.id, claim_id=claim_view_reports.id)
    user_claim_carlos_2 = UserClaim(user_id=user_carlos.id, claim_id=claim_edit_data.id)
    user_claim_gabrielly_1 = UserClaim(user_id=user_gabrielly.id, claim_id=claim_view_reports.id)

    db_session.add(user_claim_carlos_1)
    db_session.add(user_claim_carlos_2)
    db_session.add(user_claim_gabrielly_1)
    db_session.commit()

    return user_carlos, user_gabrielly

def test_create_user_with_role(db_session, sample_roles):
    role_admin, role_user = sample_roles
    user = User(
        name="Alice Smith",
        email="alice.smith@example.com",
        password="password123",
        role_id=role_admin.id,
        created_at=date.today(),
        updated_at=date.today()
    )
    try:
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
    except SQLAlchemyError as e:
        pytest.fail(f"Error creating user: {e}")

    assert user.name == "Alice Smith"
    assert user.email == "alice.smith@example.com"
    assert user.role_id == role_admin.id

def test_user_role_and_claim(db_session, sample_users, sample_claims):
    user_carlos, user_gabrielly = sample_users
    claim_view_reports, claim_edit_data, claim_delete_records = sample_claims

    assert user_carlos.role.description == "Administrador"
    assert len(user_carlos.claims) == 2
    assert user_carlos.claims[0].description == "Visualizar Relatórios"
    assert user_carlos.claims[1].description == "Editar Dados"

    assert user_gabrielly.role.description == "Usuário Padrão"
    assert len(user_gabrielly.claims) == 1
    assert user_gabrielly.claims[0].description == "Visualizar Relatórios"

def test_create_claim(db_session):
    claim = Claim(description="Editar Dados")
    db_session.add(claim)
    db_session.commit()
    db_session.refresh(claim)

    assert claim.description == "Editar Dados"

def test_create_role(db_session):
    role = Role(description="Usuário Padrão")
    db_session.add(role)
    db_session.commit()
    db_session.refresh(role)

    assert role.description == "Usuário Padrão"

def test_user_claim_association(db_session, sample_users, sample_claims):
    user_carlos, _ = sample_users
    claim_view_reports, claim_edit_data, _ = sample_claims

    user_claim = db_session.query(UserClaim).filter_by(user_id=user_carlos.id, claim_id=claim_view_reports.id).first()
    assert user_claim is not None
    assert user_claim.user_id == user_carlos.id
    assert user_claim.claim_id == claim_view_reports.id

def test_create_user_with_duplicate_email(db_session, sample_roles):
    role_admin, _ = sample_roles
    user1 = User(
        name="Alice Smith",
        email="alice.smith@example.com",
        password="password123",
        role_id=role_admin.id,
        created_at=date.today(),
        updated_at=date.today()
    )
    user2 = User(
        name="Bob Jones",
        email="alice.smith@example.com",
        password="password456",
        role_id=role_admin.id,
        created_at=date.today(),
        updated_at=date.today()
    )

    db_session.add(user1)
    db_session.commit()
    db_session.refresh(user1)

    try:
        db_session.add(user2)
        db_session.commit()
        pytest.fail("Esperado IntegrityError devido ao email duplicado, mas não ocorreu.")
    except IntegrityError:
        pass
    except SQLAlchemyError as e:
        pytest.fail(f"Erro inesperado: {e}")

def test_delete_user_and_related_claims(db_session, sample_users, sample_claims):
    user_carlos, _ = sample_users
    claim_view_reports, _, _ = sample_claims

    user_claim = db_session.query(UserClaim).filter_by(user_id=user_carlos.id, claim_id=claim_view_reports.id).first()
    assert user_claim is not None

    db_session.delete(user_carlos)
    db_session.commit()

    user_claim = db_session.query(UserClaim).filter_by(user_id=user_carlos.id, claim_id=claim_view_reports.id).first()
    assert user_claim is None

def test_delete_role_with_users(db_session, sample_roles, sample_users):
    role_admin, _ = sample_roles
    user_carlos, _ = sample_users

    assert user_carlos.role.description == "Administrador"

    db_session.query(User).filter(User.role_id == role_admin.id).update({User.role_id: 2})
    db_session.commit()

    db_session.delete(role_admin)
    db_session.commit()

    updated_user = db_session.query(User).filter(User.id == user_carlos.id).one()
    assert updated_user.role_id == 2
