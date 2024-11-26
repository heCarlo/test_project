from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UserCreate(BaseModel):
    name: str = Field(..., title="Nome do Usuário", max_length=100)
    email: EmailStr = Field(..., title="E-mail do Usuário")
    password: Optional[str] = Field(None, title="Senha do Usuário", min_length=6)
    role_id: int = Field(..., title="ID do Papel (Role) do Usuário")

    model_config: ConfigDict = {
        "json_schema_extra": {
            "example": {
                "name": "Carlos Santos",
                "email": "carlos.santos@example.com",
                "password": "password123",
                "role_id": 2
            }
        }
    }

class UserResponse(BaseModel):
    id: int = Field(..., title="ID do Usuário")
    name: str = Field(..., title="Nome do Usuário")
    email: EmailStr = Field(..., title="E-mail do Usuário")

    model_config: ConfigDict = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Carlos Santos",
                "email": "carlos.santos@example.com"
            }
        }
    }
