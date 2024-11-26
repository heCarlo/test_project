"""
define o modelo orm para a tabela 'user_claims'

o modelo representa a relação muitos-para-muitos entre usuários e claims no banco de dados
"""

from sqlalchemy import Column, Integer, ForeignKey
from .base import Base

class UserClaim(Base):
    """
    modelo para a tabela 'user_claims'
    """

    __tablename__ = "user_claims"

    user_id = Column(
        Integer, 
        ForeignKey("users.id"), 
        primary_key=True, 
        doc="identificador do usuário associado"
    )
    claim_id = Column(
        Integer, 
        ForeignKey("claims.id"), 
        primary_key=True, 
        doc="identificador do claim associado"
    )
