"""
define o modelo orm para a tabela 'roles'

o modelo representa as informações de 'roles' no banco de dados e suas relações com outras tabelas
"""

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from .base import Base

class Role(Base):
    """
    modelo para a tabela 'roles'
    """

    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True, doc="identificador único do role")
    description = Column(String, nullable=False, index=True, doc="descrição do role")

    users = relationship(
        "User", 
        back_populates="role", 
        doc="relação um-para-muitos com a tabela 'users'"
    )
