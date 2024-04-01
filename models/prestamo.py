from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Date

from sqlalchemy.orm import relationship

from .estadoprestamo import estadoprestamos
from .tipoprestamo import tipoprestamos
from .cliente import clientes

from config.db import meta, engine

prestamos = Table(
    "prestamos",
    meta,

    Column("prestamoid", Integer, primary_key=True),
    Column("fechaprestamo", Date),
    Column("fechaestimadapago", Date),
    Column("monto", Integer),
    Column("cuotas", Integer),
    Column("valorcuota", Integer),
    Column("clienteid", Integer, ForeignKey(clientes.c.clienteid)),
    Column("estadoid", Integer, ForeignKey(estadoprestamos.c.estadoid)),
    Column("tipoprestamoid", Integer, ForeignKey(tipoprestamos.c.tipoprestamoid)),
    extend_existing=True
)
meta.create_all(engine)
