import sqlite3
from sqlite3 import Error
import os 

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

def create_query_repository_table(conn):
    """ create the query_repository table """
    sql_create_query_repository_table = """CREATE TABLE IF NOT EXISTS query_repository (
                                            id INTEGER PRIMARY KEY,
                                            query_number INTEGER,
                                            actual_query TEXT,
                                            description TEXT
                                        );"""
    create_table(conn, sql_create_query_repository_table)

def insert_query(conn, query_data):
    """ Insert a new query into the query_repository table """
    sql = ''' INSERT INTO query_repository(query_number, actual_query, description)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, query_data)
    conn.commit()
    return cur.lastrowid

def main():
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    database = os.path.join(basedir, 'db.sqlite3')
    
    # Create a database connection
    conn = create_connection(database)
    if conn is not None:
        with conn:
            # Create table
            create_query_repository_table(conn)

            # Query data to insert
            query_data = (1,
                         
""" PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
    PREFIX ex: <http://example.org/> 
    PREFIX foaf: <http://xmlns.com/foaf/0.1/> 
    SELECT DISTINCT ?artist_name WHERE { 
    ?song ex:isHitSongOf ?artist. 
    ?artist foaf:name ?artist_name 
       }
     """
  
   ,
    """"This SPARQL query finds unique artist names associated with hit songs in an RDF dataset. It uses prefixes to define namespaces for RDF properties and extracts artist names using the "foaf:name" property.""")
            
            # Insert query data
            insert_query(conn, query_data)

if __name__ == '__main__':
    main()
