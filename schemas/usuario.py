from typing import Optional
from pydantic import BaseModel

class Usuario(BaseModel):
    usuarioid: Optional[int]
    username: str
    passw: str
    rolid: int