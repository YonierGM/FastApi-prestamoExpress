from typing import Optional
from pydantic import BaseModel


class Rol(BaseModel):
    rolid: Optional[int]
    descripcion: str