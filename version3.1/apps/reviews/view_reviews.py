"""
Author: Sharayu 
use this file to view reviews table data

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

def select_all_reviews(conn):
    """
    Query all rows in the reviews table
    """
    cur = conn.cursor()
    cur.execute("SELECT username, category, description, url, details, buffer,date  FROM reviews")

    rows = cur.fetchall()

    for row in rows:
        print(row)

    return rows    




def main():
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    database = os.path.join(basedir, 'db.sqlite3')
    
    # Create a database connection
    conn = create_connection(database)
    if conn is not None:
        with conn:
            # Create reviews table if not exists
            select_all_reviews(conn)


if __name__ == '__main__':
    main()
