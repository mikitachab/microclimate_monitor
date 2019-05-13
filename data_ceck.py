import sqlite3
from pprint import pprint


with sqlite3.connect('data.db') as conn:
    c = conn.cursor()
    q = 'select * from measurements'
    res = c.execute(q)
    pprint(res.fetchall())
