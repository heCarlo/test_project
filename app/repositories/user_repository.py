"""
repositório para acessar os dados de 'user' no banco de dados

esta classe abstrai as operações de consulta e manipulação de dados 
da tabela 'users' no banco de dados. ela utiliza o sqlalchemy para 
interagir com o banco de dados relacional e realizar operações de 
leitura e escrita no banco
"""

from sqlalchemy.orm import Session
from ..models.user_model import User
from ..models.claim_model import Claim
from ..models.role_model import Role

class UserRepository:
    """
    repositório para a tabela 'users'

    classe que oferece métodos para consultar e manipular dados da tabela 'users',
    incluindo a criação de usuários, recuperação por email, e inclusão de roles e claims.
    """

    def __init__(self, db: Session):
        """
        inicializa o repositório com a sessão ativa do banco de dados

        :param db: sessão ativa do banco de dados
        """
        self.db = db

    def create_user(self, db: Session, user: User):
        """
        cria um novo usuário no banco de dados

        :param db: sessão ativa do banco de dados
        :param user: objeto User a ser criado
        :return: o usuário criado após o commit no banco de dados
        """
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def get_all_users(self):
        """
        recupera todos os usuários cadastrados

        :return: lista de objetos User
        """
        return self.db.query(User).all()
    
    def get_user_by_email(self, db: Session, email: str) -> User:
        """
        recupera um usuário específico pelo email

        :param db: sessão ativa do banco de dados
        :param email: email do usuário a ser recuperado
        :return: usuário encontrado ou None se não encontrado
        """
        return db.query(User).filter(User.email == email).first()

    def get_users_with_role_and_claims(self):
        """
        recupera todos os usuários com seus respectivos roles e claims

        :return: lista de tuplas contendo dados dos usuários, roles e claims
        """
        return (
            self.db.query(User, Role, Claim)
            .join(Role, User.role_id == Role.id)
            .join(User.claims)
            .join(Claim)
            .all()
        )
