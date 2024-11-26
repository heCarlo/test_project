from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session
import logging
from app.database.database import SessionLocal
from app.models.user_model import User
from app.database.insert_test_data import insert_data 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

revision: str = '6b902945ce46'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'claims',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('description', sa.String(), nullable=False, index=True),
        sa.Column('active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
    )

    op.create_table(
        'roles',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('description', sa.String(), nullable=False, index=True),
    )

    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('name', sa.String(), nullable=False, index=True),
        sa.Column('email', sa.String(), nullable=False, unique=True, index=True),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('role_id', sa.Integer(), sa.ForeignKey('roles.id'), nullable=False),
        sa.Column('created_at', sa.Date(), nullable=False),
        sa.Column('updated_at', sa.Date(), nullable=True),
    )

    op.create_table(
        'user_claims',
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), primary_key=True),
        sa.Column('claim_id', sa.Integer(), sa.ForeignKey('claims.id'), primary_key=True),
    )
    
    op.execute('COMMIT')

    initialize_data()


def downgrade() -> None:
    op.drop_table('user_claims')
    op.drop_table('users')
    op.drop_table('roles')
    op.drop_table('claims')


def initialize_data():
    """Insere os dados iniciais no banco, após garantir que as tabelas existem."""
    with SessionLocal() as session:
        try:
            if not session.query(User).first():
                insert_data()
                logger.info("Dados iniciais inseridos com sucesso.")
            else:
                logger.info("Os dados iniciais já estão presentes, nenhum dado foi inserido.")
        except Exception as e:
            logger.error(f"Erro ao inicializar os dados: {e}", exc_info=True)
