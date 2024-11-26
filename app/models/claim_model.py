"""
define o modelo orm para a tabela 'claims'

o modelo representa as informações de 'claims' no banco de dados e suas relações com outras tabelas
"""

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean
from .base import Base

class Claim(Base):
    """
    modelo para a tabela 'claims'
    """

    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, index=True, doc="identificador único do claim")
    description = Column(String, nullable=False, index=True, doc="descrição do claim")
    active = Column(Boolean, nullable=False, default=True, doc="indica se o claim está ativo")

    users = relationship(
        "User", 
        secondary="user_claims", 
        back_populates="claims", 
        doc="relação muitos-para-muitos com a tabela 'users' via 'user_claims'"
    )
