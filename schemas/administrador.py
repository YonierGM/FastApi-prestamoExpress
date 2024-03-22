from typing import Optional
from pydantic import BaseModel

class Administrador(BaseModel):

    administradorid: Optional[int]
    nombre: str
    apellido: str
    documento: int
    email: str
    celular: str
    rolid: int
