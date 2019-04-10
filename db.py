from sqlalchemy import create_engine, MetaData, Table, Column, Integer, DateTime, Boolean
meta = MetaData()
engine = create_engine('sqlite:///data.db')


measurements = Table(
    'measurements', meta,
    Column('id', Integer, primary_key=True),
    Column('datetime', DateTime),
    Column('temperature', Integer),
    Column('humidity', Integer),
    Column('is_valid', Boolean)
)

meta.create_all(engine)


def measurements_insert(**kwargs):
    conn = engine.connect()
    ins = measurements.insert().values(**kwargs)
    conn.execute(ins)
