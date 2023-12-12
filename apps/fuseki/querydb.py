import sqlite3
from sqlite3 import Error
import os

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
database = os.path.join(basedir, 'db.sqlite3')

def create_connection():
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    database = os.path.join(basedir, 'db.sqlite3')
    conn = None
    try:
        conn = sqlite3.connect(database)
    except Error as e:
        print(e)
    return conn

def select_all_users(conn,user_input):
    
    cur = conn.cursor()
    query = "SELECT description FROM query_repository WHERE description LIKE ?"
    cur.execute(query, ('%' + user_input + '%',))
    rows = cur.fetchall()
    return rows

def extract_query(conn,user_input):
    
    cur = conn.cursor()
    
    
    query = "SELECT actual_query FROM query_repository WHERE description LIKE ?"
    cur.execute(query, ('%' + user_input + '%',))
    rows = cur.fetchone()
    
    return rows[0]

def main():
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    database = os.path.join(basedir, 'db.sqlite3')
    

    # create a database connection
    conn = create_connection()
    with conn:
        print("1. Query all users")
        select_all_users(conn)

if __name__ == '__main__':
    main()
