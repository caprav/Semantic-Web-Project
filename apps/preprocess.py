"""
 Sharayu :Script to  initialize  all database tables
 Table Names
 1) Reviews
 2) Artist
 3) History

 """
 

import sqlite3
import os
from sqlite3 import Error
import os, random, string

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None

def table_exists(conn, table_name):
    c = conn.cursor()
    c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    return c.fetchone() is not None    

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

def create_artist_table(conn):
    """ create the artist table if does not exists """
    sql_create_artist_table = """CREATE TABLE IF NOT EXISTS artist (
                                   id INTEGER PRIMARY KEY,
                                    artist_name TEXT
                                );"""
    create_table(conn, sql_create_artist_table)

def insert_artist(conn, qid, artist_name):
    """ Insert a new artist into the artist table with qid and artist_name """
    sql = ''' INSERT INTO artist(artist_name)
              VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, (artist_name))
    conn.commit()

def create_history_table(conn):
    
    
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




artists = [
    "Beyonce", "George Solti", "Quincy Jones", "Chick Corea", "Alison Krauss", "Stevie Wonder", 
    "John Williams", "Vladimir Horowitz", "Jay-Z", "Kanye West", "Vince Gill", "Henry Mancini", 
    "Bruce Springsteen", "Pat Metheny", "Al Schmitt", "Tony Bennett", "Yo-Yo Ma", "Aretha Franklin", 
    "Jimmy Sturr", "Kendrick Lamar", "Ray Charles", "Leonard Bernstein", "James Mallinson", 
    "Robert Shaw", "Paul Simon", "Steven Epstein", "Kirk Franklin", "David Frost", "Eminem", 
    "Bruno Mars", "Foo Fighters", "CeCe Winans", "Alicia Keys", "Adele", "Bela Fleck", "Jerry Douglas", 
    "Phil Ramone", "Alison Krauss and Union Station", "Jay David Saks", "Emmylou Harris", "Michael Jackson", 
    "Pharrell Williams", "Lady Gaga", "Johnny Cash", "Bonnie Raitt", "Robert Woods", "Taylor Hawkins", 
    "Leontyne Price", "Ella Fitzgerald", "T Bone Burnett", "Thomas Z Shepard", "John Legend", "The Chicks", 
    "Jay Newland", "Babyface", "Taylor Swift", "Michael Tilson Thomas", "Shirley Caesar", "Al Green", 
    "Arif Mardin", "Roger Miller", "Andre Previn", "Justin Timberlake", "Bob Dylan", "James Levine", 
    "Linda Ronstadt", "Chaka Khan", "Bobby McFerrin", "Carlos Santana", "Pat Metheny Group", "Willie Nelson", 
    "Mary J. Blige", "Rihanna", "Frank Sinatra", "Sheryl Crow", "James Blackwood Sr.", "Brandi Carlile", 
    "Natalie Cole", "Count Basie", "Joni Mitchell", "Norah Jones", "Hillary Scott", "Emerson String Quartet", 
    "Dolly Parton", "Barbra Streisand", "Luther Vandross", "Asleep At The Wheel", "Tina Turner", "Usher", 
    "Fergie", "Take 6", "Lauryn Hill", "Blackwood Brothers", "Anita Baker", "Metallica", "Rick Rubin", 
    "James Blackwood Jr.", "Chris Stapleton", "Carrie Underwood", "Ziggy Marley", "Eddie Palmieri", 
    "The Manhattan Transfer", "Art Garfunkel", "Anderson .Paak", "Skrillex", "Santana", "Stephen Marley", 
    "Finneas O'Connell", "Prince", "Madonna", "will.i.am", "Dr. Dre", "André 3000", "Gladys Knight", 
    "Thomas Frost", "John Mayer", "Billie Eilish", "Los Tigres del Norte", "Toni Braxton", "Simon & Garfunkel", 
    "Ricky Skaggs and Kentucky Thunder", "Leslie Ann Jones", "Whitney Houston", "Robert M. Jones", "Amy Grant", 
    "James Taylor", "Eagles", "Big Boi", "Jack Antonoff", "Questlove", "Israel Houghton", "OutKast", 
    "Black Eyed Peas", "Dr. John", "Tito Puente", "Tim Martyn", "Kacey Musgraves", "Mariah Carey", "Lil Wayne", 
    "Janet Jackson", "H.E.R.", "Billy Joel", "Christina Aguilera", "Donna Summer", "Cee Lo Green", 
    "Mary Chapin Carpenter", "Peter, Paul & Mary", "Dionne Warwick", "Michael McDonald", "Sandi Patty", 
    "Kuk Harrell", "Maria Schneider", "Childish Gambino", "Robert Glasper", "Jon Batiste", "Lady A", 
    "Christopher Cross", "Missy Elliott", "David Russell", "Flaco Jimenez", "Ward Swingle", "India.arie", 
    "Timbaland", "Erykah Badu", "Keith Urban", "PJ Morton", "Lyle Lovett", "Lizzo", "Yolanda Adams", 
    "Tracy Chapman", "The Weeknd", "Marvin Hamlisch", "Lisa Lopes", "Lenny Kravitz", "Carole King", "Sade", 
    "Robert Spano", "Will Smith", "Pepe Aguilar", "Silk Sonic", "R. Kelly", "Pink", "Ludacris", "T.I", 
    "Gwen Stefani", "Loretta Lynn", "Etta James", "Bill Holman", "Reba McEntire", "Kelly Clarkson", "Elvis Presley", 
    "Harry Connick Jr.", "Destiny's Child", "The Roots", "Clare Fischer", "Puff Daddy", "Maroon 5", "Maxwell", 
    "Diplo", "Gloria Estefan", "Red Hot Chili Peppers", "Los Lobos", "Vikki Carr", "Fiona Apple", "Lori McKenna", 
    "Rob Thomas", "Shawn Colvin", "Taj Mahal", "Steely Dan", "Harry Styles", "James Brown", "Chance the Rapper", 
    "Ross Bagdasarian Sr.", "The Carpenters", "Olivia Rodrigo", "The Flaming Lips", "Megan Thee Stallion", 
    "Lin-Manuel Miranda", "Bob Newhart", "Esperanza Spalding", "Toto", "St. Vincent", "Tool", "Lenny White", 
    "Dan + Shay", "Pentatonix", "Jazmine Sullivan", "Cyndi Lauper", "Melissa Etheridge", "Ariana Grande", 
    "Peter Kater", "Patti LaBelle", "T-Pain", "Marvin Gaye", "Kenny Loggins", "Barry White", "Yehudi Menuhin", 
    "Intocable", "No Doubt", "Jimmy Carter", "Brian Wilson", "Marc Anthony", "Peter Nero", "Nate Ruess", 
    "Bon Iver", "Soundgarden", "La Mafia", "LeAnn Rimes", "Brave Combo", "Fleetwood Mac", "Frank Ocean", 
    "Jennifer Hudson", "Linkin Park", "Andrew Dost", "Evanescence", "Bad Bunny", "Natalie Hemby", "Nate Hills", 
    "Otis Redding", "Bobby Darin", "Tyler, the Creator", "Vernon Reid", "Colbie Caillat", "Lorde", "Aaron Dessner", 
    "Ted Nash", "The Wreckers", "Lauren Daigle", "Kaytranada", "Jason Mraz", "Nipsey Hussle", "Little Joe y La Familia", 
    "Lisa Fischer", "Tori Kelly", "Rufus", "Thundercat", "David Robertson", "Selena", 
    "Judy Garland", "Samara Joy", "Chris Brown", "Kenny G", "Doja Cat", "Nas", "SZA", 
    "50 Cent", "Elvis Costello", "Ledisi", "Ray Barretto", "Miguel", "Pearl Jam", 
    "Carter Beauford", "Brandy Norwood", "Fantasia", "Dave Matthews Band", "Eddie Blazonczyk", 
    "Jon Bon Jovi", "J. Cole", "Lucky Daye", "DJ Khaled", "Q-Tip", "Chicago", "David Crosby", 
    "Cardi B", "The Neptunes", "Bon Jovi", "Arcade Fire", "Roddy Ricch", "Ashanti", "Al Hirt", 
    "Britney Spears", "Mariachi Divas", "John McLaughlin Williams", "Stephen Stills", "Sara Bareilles", 
    "Faith Evans", "Lil Baby", "Cher", "Queen Latifah", "Mongo Santamaria", "Paula Cole", "Nat King Cole", 
    "Rhonda Vincent", "Steve Lacy", "Stargate", "Bobby Bare", "Crosby, Stills & Nash", "Nirvana", 
    "Twenty One Pilots", "Kylie Minogue", "Gloria Gaynor", "Emilio Navaira", "Ciara", "Fun", 
    "Richard Marx", "Enrique Iglesias", "The Chainsmokers", "Steve Jordan", "Pink Floyd", "Michelle Branch", 
    "Frank Yankovic", "Kentucky Headhunters", "Imagine Dragons", "Alfred Newman", "Julieta Venegas", "Monica", 
    "21 Savage", "Hykeem Carter", "Leon Bridges", "Ella Mai", "Muni Long", "Weezer", "Cal Tjader", 
    "Mariachi los Camperos", "Texas Tornados", "Los Palominos", "Rüfüs Du Sol", "Meghan Trainor", "La Santa Cecilia", 
    "Lila Downs", "The Band Perry", "Lupillo Rivera", "Nadia Shpachenko", "Andra Day", "Harry Styles", "Creed", 
    "Gloria Cheng", "Bacilos", "Los Super Seven", "The Legends", "Paula Abdul", "Bobby Brown", "Bo Burnham", 
    "Otha Nash", "America", "Lisa Loeb & Nine Stories", "Jesse Harris", "Sirah", "Solange", "Chris Perez", 
    "Stephen McLaughlin", "Chente Barrera", "Los Texmaniacs", "Jessica Rivera", "Puff Daddy & The Family", 
    "The Product G&B", "Timothy Fallon", "Freddie Nartinez Jr.", "Daya"]          

 


 
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
database = os.path.join(basedir, 'db.sqlite3')
    
    # Create a database connection
conn = create_connection(database)
if conn is not None:
        with conn:

            if not table_exists(conn, 'reviews'):
                create_reviews_table(conn)
                review_data = ('test', 'Pop', 'Imagine Dragon Concert live on 20th Nov', 'http://example.com', 'Lets go', None,'2023-11-19')
                insert_review(conn, review_data)
                ReviewStatus ="Review Table Created"
            else:
                ReviewStatus ="Review Table Loaded"


            if not table_exists(conn, 'artist'):
                create_artist_table(conn)
                for artist in artists:
                    query = "INSERT INTO artist (name) VALUES (%s);"
                    insert_artist(conn, query, (artist,))
                ArtistStatus ="Artist Table Created" 
            else:
                ArtistStatus ="Artist Table Loaded"   
            
            if not table_exists(conn, 'history'):
                create_history_table(conn)
                history_data = ('test', '2022-11-01', '2023-11-15', 'Gold', 'Enrique', '2023-11-18', None, None, None, None)
                load_history(history_data)
                HistoryStatus ="History Table Created" 
            else:
                HistoryStatus ="History Table Loaded"              
         
            db_dict = {
                    'ReviewStatus': ReviewStatus,
                    'ArtistStatus'     : ArtistStatus ,
                    'HistoryStatus' :  HistoryStatus
            }
 