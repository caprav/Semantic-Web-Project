"""
Author: Sharayu 
use this file to view history table data
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


def show_history(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT username, start_date, end_date, type, artist_name, query_date, parameter_1    FROM history")
        rows = cursor.fetchall()
        return rows
    except Error as e:
        print("Error querying history table:", e)
        return []

def show_user_history(conn,user_name):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT username, start_date, end_date, type, artist_name, query_date, parameter_1 FROM history WHERE username = ?", (user_name,))
        rows = cursor.fetchall()
        
        return rows
    except Error as e:
        print("Error querying history table:", e)
        return []        

# Example usage:
if __name__ == '__main__':
    conn = create_connection(database)
    if conn is not None:
        history_data = show_history(conn)
        for row in history_data:
            print(row)
        conn.close()
