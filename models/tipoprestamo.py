from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Date

from sqlalchemy.orm import relationship

from config.db import meta, engine

tipoprestamos = Table(
    "tipoprestamos",
    meta,

    Column("tipoprestamoid", Integer, primary_key=True),
    Column("descripcion", String(255)),
)
meta.create_all(engine)

