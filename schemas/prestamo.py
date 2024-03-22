from datetime import date
from typing import Optional
from pydantic import BaseModel

class Prestamo(BaseModel):
    prestamoid: Optional[int]
    fechaprestamo: date
    fechaestimadapago: date
    monto: int
    cuotas: int
    valorcuota: int
    clienteid: int
    estadoid: int
    tipoprestamoid: int
