from typing import Optional
from pydantic import BaseModel

class EstadoPrestamo(BaseModel):
    estadoid: Optional[int]
    descripcion: str
