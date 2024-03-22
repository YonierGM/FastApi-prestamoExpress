from sqlalchemy import Table, Column, ForeignKey, ForeignKeyConstraint
from sqlalchemy.sql.sqltypes import Integer, String, Date

from sqlalchemy.orm import relationship

from .rol import roles
from config.db import meta, engine

clientes = Table(

    "clientes",
    meta,

    Column("clienteid", Integer, primary_key=True),
    Column("nombre", String(255)),
    Column("apellido", String(255)),
    Column("documento", Integer),
    Column("fecha_nac", Date),
    Column("direccion", String(255)),
    Column("celular", String(255)),
    Column("email", String(255)),
    Column("rolid", Integer),
    ForeignKeyConstraint(["rolid"], ["roles.rolid"], ondelete="CASCADE"),
    extend_existing=True
)
meta.create_all(engine)