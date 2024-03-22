from typing import Optional
from pydantic import BaseModel

class TipoPrestamo(BaseModel):
    tipoprestamoid: Optional[int]
    descripcion: str
