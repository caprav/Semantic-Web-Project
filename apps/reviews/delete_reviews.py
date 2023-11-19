"""
Author: Sharayu 
use this file to delete reviews table data
"""


import sqlite3
import os
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None

def delete_reviews_table(conn):
    """ Delete the reviews table """
    sql = 'DROP TABLE IF EXISTS reviews'
    try:
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
    except Error as e:
        print(e)

 


def main():
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    database = os.path.join(basedir, 'db.sqlite3')
    
    # Create a database connection
    conn = create_connection(database)
    if conn is not None:
        with conn:
            # Create reviews table if not exists
            delete_reviews_table(conn)


if __name__ == '__main__':
    main()
