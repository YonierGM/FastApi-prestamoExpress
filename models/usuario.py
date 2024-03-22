from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Date

from sqlalchemy.orm import relationship

from .rol import roles
from config.db import meta, engine

usuarios = Table(
    "usuarios",
    meta,

    Column("usuarioid", Integer, primary_key=True),
    Column("username", String(255)),
    Column("passw", String(255)),
    Column("rolid", Integer, ForeignKey(roles.c.rolid)),
    extend_existing=True
)
meta.create_all(engine)

