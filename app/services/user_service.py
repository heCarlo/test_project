"""
serviço para gerenciar as operações relacionadas aos usuários

este serviço fornece métodos para criar e buscar usuários no sistema,
além de gerar senhas aleatórias e realizar o hash das senhas
"""

import random
import string
from datetime import date
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from ..models.user_model import User
from ..repositories.user_repository import UserRepository
from ..services.role_service import RoleService
from ..schemas.user_schema import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    """
    serviço para gerenciar os usuários do sistema

    classe que oferece métodos para criação de usuários, busca por e-mail
    e geração de senhas aleatórias e seguras
    """

    @staticmethod
    def generate_random_password(length=8) -> str:
        """
        gera uma senha aleatória

        este método cria uma senha aleatória usando letras e números

        :param length: tamanho da senha a ser gerada (padrão é 8)
        :return: a senha gerada como string

        exemplo:
        - length: 12
        - retorna uma senha aleatória de 12 caracteres
        """
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    @staticmethod
    def hash_password(password: str) -> str:
        """
        gera o hash de uma senha

        este método usa o algoritmo bcrypt para gerar o hash de uma senha

        :param password: a senha a ser hashada
        :return: o hash gerado para a senha

        exemplo:
        - password: "password123"
        - retorna o hash bcrypt da senha "password123"
        """
        return pwd_context.hash(password)

    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """
        cria um novo usuário no sistema

        este método verifica se o papel existe, gera uma senha aleatória
        ou usa a fornecida, realiza o hash da senha (se necessário) e cria
        um novo usuário no banco de dados

        :param db: sessão do banco de dados para realizar a operação
        :param user_data: os dados do usuário a ser criado
        :return: o usuário criado

        exemplo:
        - user_data: {
            "name": "Carlos Santos",
            "email": "carlos@example.com",
            "password": "password123",
            "role_id": 1
        }
        - retorna o novo usuário criado com os dados fornecidos
        """
        RoleService.get_role_by_id(db, user_data.role_id)
        
        password = user_data.password or UserService.generate_random_password()

        if user_data.password:
            password = UserService.hash_password(password)

        new_user = User(
            name=user_data.name,
            email=user_data.email,
            password=password,
            role_id=user_data.role_id,
            created_at=date.today()
        )

        return UserRepository(db).create_user(db, new_user)

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User | None:
        """
        busca um usuário pelo e-mail

        este método consulta o banco de dados para buscar um usuário com o e-mail fornecido

        :param db: sessão do banco de dados para realizar a consulta
        :param email: o e-mail do usuário a ser buscado
        :return: o usuário encontrado ou None se não encontrado

        exemplo:
        - email: "carlos@example.com"
        - retorna o usuário com o e-mail "carlos@example.com", caso exista
        """
        return UserRepository(db).get_user_by_email(db, email)
