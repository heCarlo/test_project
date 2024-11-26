"""
repositório para acessar os dados de 'role' no banco de dados

esta classe abstrai as operações de consulta e manipulação de dados 
da tabela 'roles' no banco de dados. ela utiliza o sqlalchemy para 
interagir com o banco de dados relacional
"""

from ..models.role_model import Role
from sqlalchemy.orm import Session

class RoleRepository:
    """
    repositório para a tabela 'roles'

    classe que oferece métodos para consultar e manipular dados da tabela 'roles'
    """
    @staticmethod
    def get_role_by_id(db: Session, role_id: int):
        """
        recupera um 'role' específico pelo id

        :param db: sessão ativa do banco de dados
        :param role_id: id do role a ser recuperado
        :return: objeto Role ou None se não encontrado
        """
        return db.query(Role).filter(Role.id == role_id).first()
