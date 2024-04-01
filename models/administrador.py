from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Date

from sqlalchemy.orm import relationship

from .rol import roles
from config.db import meta, engine

administradores = Table(
    "administradores",
    meta,

    Column("administradorid", Integer, primary_key=True),
    Column("nombre", String(255)),
    Column("apellido", String(255)),
    Column("documento", Integer),
    Column("email", String(255)),
    Column("celular", String(255)),
    Column("username", String(255)),
    Column("passw", String(255)),
    Column("rolid", Integer, ForeignKey(roles.c.rolid)),
    extend_existing=True
)
meta.create_all(engine)
