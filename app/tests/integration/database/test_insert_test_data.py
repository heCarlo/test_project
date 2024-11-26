import pytest
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from app.models.claim_model import Claim
from app.models.user_model import User
from app.models.role_model import Role
from app.database.database import engine, SessionLocal
from sqlalchemy import create_engine
from app.models.base import Base 

TEST_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(TEST_DATABASE_URL, echo=True)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture(scope='module')
def setup_database():
    """Cria e limpa o banco de dados para os testes"""
    Base.metadata.create_all(test_engine)
    yield
    Base.metadata.drop_all(test_engine)

@pytest.fixture(scope='function')
def db_session(setup_database):
    """Fixture para criar e fechar a sessão de banco de dados de teste"""
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()  # Garante que a sessão seja fechada após o teste

def test_insert_test_data(db_session):
    """Teste para garantir que a função insert_test_data insira os dados corretamente"""        

    from app.database.insert_test_data import insert_test_data
    insert_test_data(db_session)

    admin_role = db_session.query(Role).filter_by(description="Administrador").first()
    user_role = db_session.query(Role).filter_by(description="Usuário Padrão").first()
    assert admin_role is not None
    assert user_role is not None

    claim1 = db_session.query(Claim).filter_by(description="Visualizar Relatórios").first()     
    claim2 = db_session.query(Claim).filter_by(description="Editar Dados").first()
    claim3 = db_session.query(Claim).filter_by(description="Excluir Registros").first()
    assert claim1 is not None
    assert claim2 is not None
    assert claim3 is not None

    user1 = db_session.query(User).filter_by(email="carlos@example.com").first()
    user2 = db_session.query(User).filter_by(email="gabrielly@example.com").first()
    assert user1 is not None
    assert user2 is not None

    assert claim1 in user1.claims
    assert claim2 in user1.claims
    assert claim1 in user2.claims
    assert claim2 not in user2.claims

    assert user1.created_at is not None       
    assert user1.updated_at is not None       
    assert user2.created_at is not None       
    assert user2.updated_at is not None
