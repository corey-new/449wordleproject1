import sqlite3
import argparse

#Sqlite3 Database creation and population script.
#run with argument "-p" to populate database with a few entries.
#view populatedb.sql to see the added user and games.

def setupdb():
    dbname = 'wordle.db'
    print('setting up db: ', dbname)
    con = sqlite3.connect(dbname)
    cur = con.cursor()
    with open('schema.sql', 'r') as file:
        data = file.read()
        cur.executescript(data)
    con.close()
    print('successfully setup db: ', dbname)

def populatedb():
    dbname = 'wordle.db'
    print('populating up db: ', dbname)
    con = sqlite3.connect(dbname)
    cur = con.cursor()
    with open('populatedb.sql', 'r') as file:
        data = file.read()
        cur.executescript(data)
    con.close()
    print('successfully populated db: ', dbname)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', action='store_true')

    parser = parser.parse_args()

    setupdb()

    if parser.p:
        populatedb()