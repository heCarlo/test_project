"""
define o modelo orm para a tabela 'users'

o modelo representa os usuários do sistema com suas informações básicas, relação com roles e claims
"""

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from .base import Base

class User(Base):
    """
    modelo para a tabela 'users'
    """

    __tablename__ = "users"

    id = Column(
        Integer, 
        primary_key=True, 
        index=True, 
        doc="identificador único do usuário"
    )
    name = Column(
        String, 
        nullable=False, 
        index=True, 
        doc="nome completo do usuário"
    )
    email = Column(
        String, 
        nullable=False, 
        unique=True, 
        index=True, 
        doc="endereço de email único do usuário"
    )
    password = Column(
        String, 
        nullable=False, 
        doc="hash da senha do usuário"
    )
    role_id = Column(
        Integer, 
        ForeignKey("roles.id"), 
        nullable=False, 
        doc="identificador da role associada ao usuário"
    )
    created_at = Column(
        Date, 
        nullable=False, 
        doc="data de criação do registro"
    )
    updated_at = Column(
        Date, 
        nullable=True, 
        doc="data de atualização do registro, se aplicável"
    )

    role = relationship(
        "Role", 
        back_populates="users", 
        doc="relação com o papel (role) do usuário"
    )
    claims = relationship(
        "Claim", 
        secondary="user_claims", 
        back_populates="users", 
        doc="relação com as claims associadas ao usuário"
    )
