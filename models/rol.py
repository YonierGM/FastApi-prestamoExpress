from sqlalchemy import Table, Column, Integer, String, Date, ForeignKey
#from sqlalchemy.sql.sqltypes import Integer, String, Date

from config.db import meta, engine

roles = Table(

    "roles",
    meta,

    Column("rolid", Integer, primary_key=True),
    Column("descripcion", String(255)),
)

meta.create_all(engine)