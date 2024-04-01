from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Date

from sqlalchemy.orm import relationship

from .prestamo import prestamos
from config.db import meta, engine

pagos = Table(
    "pagos",
    meta,

    Column("pagoid", Integer, primary_key=True),
    Column("fechapago", Date),
    Column("monto", Integer),
    Column("prestamoid", Integer, ForeignKey(prestamos.c.prestamoid)),
    extend_existing=True
)
meta.create_all(engine)
