"""
repositório para interagir com a tabela 'claims'

este repositório contém métodos para acessar e manipular os dados relacionados às claims no banco de dados
"""

from sqlalchemy.orm import Session
from ..models.claim_model import Claim

class ClaimRepository:
    """
    repositório para a tabela 'claims'

    classe que oferece métodos para consultar as claims no banco de dados
    """
    def __init__(self, db: Session):
        """
        inicializa o repositório com uma sessão de banco de dados

        :param db: sessão ativa do banco de dados
        """
        self.db = db

    def get_all_claims(self):
        """
        retorna todas as claims armazenadas no banco de dados

        :return: lista de objetos 'Claim'
        """
        return self.db.query(Claim).all()
