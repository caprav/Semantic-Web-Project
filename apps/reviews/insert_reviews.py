"""
Author: Sharayu 
use this file to insert reviews table data

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

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_reviews_table(conn):
    """ create the reviews table if it does not exist """
    sql_create_reviews_table = """ CREATE TABLE IF NOT EXISTS reviews (
                                        id INTEGER PRIMARY KEY,
                                        username TEXT NOT NULL,
                                        category TEXT,
                                        description TEXT,
                                        url TEXT,
                                        details TEXT,
                                        buffer TEXT,
                                        date TEXT

                                    ); """
    create_table(conn, sql_create_reviews_table)

def insert_review(conn, review_data):
    """ Insert a new review into the reviews table """
    sql = ''' INSERT INTO reviews(username, category, description, url, details, buffer,date )
              VALUES(?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, review_data)
    conn.commit()
    return cur.lastrowid






def main():
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    database = os.path.join(basedir, 'db.sqlite3')
    
    # Create a database connection
    conn = create_connection(database)
    if conn is not None:
        with conn:
            # Create reviews table if not exists
            create_reviews_table(conn)

            # Insert review data as needed
            # Example review data to insert
            review_data = ('test', 'Pop', 'Imagine Dragon Concert live on 20th Nov', 'http://example.com', 'Lets go', None,'2023-11-19')
            inserted_id = insert_review(conn, review_data)

            # Delete a review by ID as needed
            # delete_review(conn, inserted_id)

if __name__ == '__main__':
    main()
