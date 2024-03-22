from datetime import date
from typing import Optional
from pydantic import BaseModel

class Pago(BaseModel):
    pagoid: Optional[int]
    fechapago: date
    monto: int
    prestamoid: int
