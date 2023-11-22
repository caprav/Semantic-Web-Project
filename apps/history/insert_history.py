"""
Author: Sharayu 
use this file to insert history table data
"""


import sqlite3
import os
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
database = os.path.join(basedir, 'db.sqlite3')
conn = create_connection(database)

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def table_exists(conn, table_name):
    c = conn.cursor()
    c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    return c.fetchone() is not None

def create_history_table(conn):
    table_name = 'history'
    if not table_exists(conn, table_name):
        sql_create_history_table = """CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            start_date TEXT,
            end_date TEXT,
            type TEXT,
            artist_name TEXT,
            query_date TEXT,
            parameter_1 TEXT,
            parameter_2 TEXT,
            parameter_3 TEXT,
            parameter_4 TEXT
        );"""
        create_table(conn, sql_create_history_table)

def load_history(history_data):
    conn = None
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    database = os.path.join(basedir, 'db.sqlite3')
    

    try:
        conn = sqlite3.connect(database)
        
    except Error as e:
        print(e)

    sql = '''INSERT INTO history(username, start_date, end_date, type, artist_name, query_date, parameter_1, parameter_2, parameter_3, parameter_4)
             VALUES(?,?,?,?,?,?,?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, history_data)
    conn.commit()
    conn.close()
    


def main():
    try:
        create_history_table(conn)
    except Exception as e:
        print("Table creation failed:", e)

        

    history_data = ('test', '2022-11-01', '2023-11-15', 'Gold', 'Enrique', '2023-11-18', None, None, None, None)
    history_data1 = ('test', '2022-11-01', '2023-11-15', 'Silver', 'Lady Gaga', '2023-11-18', 'Value1', None, None, None)
    history_data2 = ('test', '2022-11-01', '2023-11-15', 'Platinum', 'Shakira', '2023-11-18', 'Value1', 'Value2', None, None)
    load_history(history_data)
    load_history( history_data1)
    load_history( history_data2)

if __name__ == '__main__':
    main()
