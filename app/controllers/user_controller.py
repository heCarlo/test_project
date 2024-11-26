"""
este módulo contém os endpoints relacionados a usuários e roles (papeis) do sistema

endpoints:
- obter role por id
- criar um novo usuário
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..services.user_service import UserService
from ..services.role_service import RoleService
from ..database.database import get_db
from ..schemas.user_schema import UserCreate, UserResponse
from ..schemas.role_schema import RoleResponse

router = APIRouter()

@router.get(
    "/role/{role_id}",
    response_model=RoleResponse,
    summary="obter role por id",
    description="obtém um papel (role) específico a partir do id fornecido"
)
def get_role_by_id(role_id: int, db: Session = Depends(get_db)):
    """
    endpoint para obter um papel (role) por id

    args:
        role_id (int): id do papel a ser buscado
        db (Session): sessão de banco de dados injetada automaticamente

    returns:
        RoleResponse: dados do papel correspondente

    raises:
        HTTPException: retorna 404 se o papel não for encontrado
    """
    role = RoleService.get_role_by_id(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="role not found")
    return role

@router.post(
    "/users/",
    response_model=UserResponse,
    summary="criar usuário",
    description="cria um novo usuário no sistema"
)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    endpoint para criar um novo usuário no sistema

    args:
        user (UserCreate): dados do usuário a ser criado
        db (Session): sessão de banco de dados injetada automaticamente

    returns:
        UserResponse: dados do usuário criado

    raises:
        HTTPException:
            - 400 se o e-mail já estiver registrado
    """
    existing_user = UserService.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="email already registered")
    
    return UserService.create_user(db, user)