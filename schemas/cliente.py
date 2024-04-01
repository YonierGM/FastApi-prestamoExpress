from datetime import date
from typing import Optional
from pydantic import BaseModel

class Cliente(BaseModel):
    clienteid: Optional[int]
    nombre: str
    apellido: str
    documento: int
    fecha_nac: date
    direccion: str
    celular: int
    email: str
    username: str
    passw: str
    rolid: int
