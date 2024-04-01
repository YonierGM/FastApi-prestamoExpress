from sqlalchemy import create_engine, MetaData

engine = create_engine('postgresql://postgres:0000@localhost:5432/prestamoexpressdb')
meta = MetaData()
conn = engine.connect()

