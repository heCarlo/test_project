from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone
from ..models.claim_model import Claim
from ..models.user_model import User
from ..models.role_model import Role
from ..database.database import engine

def insert_test_data(db: Session):
    admin_role = Role(description="Administrador")
    user_role = Role(description="Usuário Padrão")
    db.add_all([admin_role, user_role])
    db.commit()

    claim1 = Claim(description="Visualizar Relatórios")
    claim2 = Claim(description="Editar Dados")
    claim3 = Claim(description="Excluir Registros")
    db.add_all([claim1, claim2, claim3])
    db.commit()

    user1 = User(
        name="Carlos Henrique",
        email="carlos@example.com",
        password="password123",
        role_id=admin_role.id,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    user2 = User(
        name="Gabrielly Nunes",
        email="gabrielly@example.com",
        password="password123",
        role_id=user_role.id,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    db.add_all([user1, user2])
    db.commit()

    user1.claims = [claim1, claim2]
    user2.claims = [claim1]
    db.commit()


def insert_data():
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    insert_test_data(db)

    db.close()