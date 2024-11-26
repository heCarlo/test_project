from pydantic import BaseModel, Field
from typing import Optional
from pydantic import ConfigDict

class RoleResponse(BaseModel):
    id: int = Field(..., json_schema_extra={"title": "ID do Papel", "example": 1})
    description: str = Field(..., json_schema_extra={"title": "Nome do Papel", "example": "Administrador"})

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "description": "Administrador"
            }
        }
    )
