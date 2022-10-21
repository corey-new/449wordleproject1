import sqlite3
from databases import Database


dbname = 'wordle.db'
print('setting up db: ', dbname)
con = sqlite3.connect(dbname)
cur = con.cursor()
with open('schema.sql', 'r') as file:
    data = file.read()
    cur.executescript(data)
con.close()
print('successfully setup db: ', dbname)


