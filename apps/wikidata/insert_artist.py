# Preprocess Artist info for faster  wikidata retrival 
#
#

import sqlite3
from sqlite3 import Error
import os 

 

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
database = os.path.join(basedir, 'db.sqlite3')

def select_all_artists(conn,user_input):
    cur = conn.cursor()
    """ Query all rows in the artist table """
    query = "SELECT artist_name FROM artist WHERE artist_name LIKE ?"
    cur.execute(query, ('%' + user_input + '%',))
    
    rows = cur.fetchall()
    return rows



def create_connection():
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    database = os.path.join(basedir, 'db.sqlite3')
    conn = None
    try:
        conn = sqlite3.connect(database)
    except Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_artist_table(conn):
    """ create the artist table """
    sql_create_artist_table = """CREATE TABLE IF NOT EXISTS artist (
                                   id INTEGER PRIMARY KEY,
                                    artist_name TEXT
                                );"""
    create_table(conn, sql_create_artist_table)

# Call this function to create the "artist" table in your database.
# Replace 'conn' with your database connection object.



def insert_artist(conn, qid, artist_name):
    """ Insert a new artist into the artist table with qid and artist_name """
    sql = ''' INSERT INTO artist(artist_name)
              VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, (artist_name))
    conn.commit()


def main():
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    database = os.path.join(basedir, 'db.sqlite3')
    
    # Create a database connection
    conn = create_connection()
    if conn is not None:
        with conn:
            # Create table
            create_artist_table(conn)
 
 
            #######
            #  Enable below for loop to insert the data in artists table 
            ######### 
            
            for artist in artists:
                query = "INSERT INTO artists (name) VALUES (%s);"
                insert_artist(conn, query, (artist,))
           

            """ Use below to view the data in artits table
              

            all_artists = select_all_artists(conn)
            for artist in all_artists:
                print(artist)    
                 """ 








# Generating the SQL INSERT statements for the provided list of artists
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




if __name__ == '__main__':
    main()   
