"""
serviço para gerenciar as operações relacionadas aos papéis (roles) no sistema

este serviço fornece métodos para interagir com os papéis do sistema,
como buscar um papel por seu id
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..repositories.role_repository import RoleRepository

class RoleService:
    """
    serviço para gerenciar os papéis (roles) no sistema

    classe que oferece métodos para realizar operações relacionadas aos papéis
    no sistema, como busca de um papel por id.
    """
    
    @staticmethod
    def get_role_by_id(db: Session, role_id: int):
        """
        obtém um papel (role) pelo id fornecido

        este método busca um papel no banco de dados usando o repositório de papéis
        se o papel não for encontrado, uma exceção http 404 é levantada

        :param db: sessão do banco de dados para realizar a consulta
        :param role_id: o id do papel a ser buscado
        :return: o papel encontrado, caso exista
        :raises HTTPException: levanta um erro 404 caso o papel não seja encontrado
        
        exemplo:
        - role_id: 1
        - retorna o papel com id 1, caso exista no banco de dados
        """
        role = RoleRepository.get_role_by_id(db, role_id)
        if not role:
            raise HTTPException(status_code=404, detail="role not found")
        return role
