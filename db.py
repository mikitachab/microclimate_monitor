from statistics import mean
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, DateTime, Boolean
from sqlalchemy.sql import select
from config import config
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
    select_list = [getattr(measurements.c, value) for value in config['MONITORED_VALUES']]
    query = select(select_list).order_by(measurements.c.id.desc()).limit(n)
    result = conn.execute(query)
    return result.fetchall()


def mean_of_last_n_measurements(n):
    n_measurements = last_n_measurements(n)
    if not n_measurements:
        return 0
    avg_list = []
    for i in range(len(n_measurements[0])):
        avg_list.append(mean(m[i] for m in n_measurements))
    return avg_list
