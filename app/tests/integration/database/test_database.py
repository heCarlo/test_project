import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.database.database import get_db
from dotenv import load_dotenv
import os
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope='function')
def db_session():
    """Fixture para criar e fechar a sessão de banco de dados"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_get_db(db_session):
    """Teste para garantir que a função get_db() cria e fecha a sessão corretamente"""

    db_generator = get_db()
    db = next(db_generator)

    assert db is not None
    assert hasattr(db, 'execute')

    result = db.execute(text('SELECT 1'))     
    assert result.fetchone() is not None      

    db_generator.close()

    with pytest.raises(StopIteration):
        next(db_generator)
