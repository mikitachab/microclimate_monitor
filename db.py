from sqlalchemy import create_engine, MetaData, Table, Column, Integer, DateTime, Boolean
from sqlalchemy.sql import select
from statistics import mean
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


def last_n_measurements(n):
    conn = engine.connect()
    query = select([measurements.c.temperature, measurements.c.humidity]).order_by(measurements.c.id.desc()).limit(n)
    result = conn.execute(query)
    return result.fetchall()


def mean_of_last_n_measurements(n):
    n_measurements = last_n_measurements(n)
    n_temperature = [x[0] for x in n_measurements]
    n_humidity = [x[1] for x in n_measurements]
    return mean(n_temperature), mean(n_humidity)
