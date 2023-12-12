from SPARQLWrapper import SPARQLWrapper, JSON
import urllib.parse

def get_artist_suggestions(pattern):
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")
    sparql.setQuery("""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        SELECT DISTINCT ?artist ?artist_name WHERE {{
            ?artist a dbo:MusicalArtist ;
                    foaf:name ?artist_name .
            FILTER(CONTAINS(LCASE(str(?artist_name)), LCASE("{pattern}")))
        }}
       
    """.format(pattern=pattern.lower()))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

def get_artist_sales(artist_name):
    # Extracting the artist name from the URI
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")
    sparql.setQuery("""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dbp: <http://dbpedia.org/property/>
        PREFIX dbr: <http://dbpedia.org/resource/>
        SELECT DISTINCT ?work ?sales WHERE {{
            ?work dbo:artist dbr:{artist_name} ;
                  a dbo:Song ;
                  dbp:salesamount ?sales.
        }}
    """.format(artist_name=artist_name))  # Use artist_name=artist_name here
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results



# Example usage
pattern = input("Enter artist name pattern: ")  # User inputs pattern
suggestions = get_artist_suggestions(pattern)

if suggestions and suggestions["results"]["bindings"]:
    for suggestion in suggestions["results"]["bindings"]:
        artist_uri = suggestion['artist']['value']
        print(f"\nArtist URI: {artist_uri}")
        artist_name = artist_uri.split('/')[-1]
        print(artist_name)

        sales_info = get_artist_sales(artist_name)
        total_sales = 0
        if sales_info and sales_info["results"]["bindings"]:
            print("Sales Information:")
            for sale in sales_info["results"]["bindings"]:
                work = sale['work']['value']
                sales = float(sale['sales']['value']) if 'sales' in sale and sale['sales']['value'].isdigit() else 0
                total_sales += sales
                print(f"Work: {work}, Sales: {sales}")
            print(f"Total Sales for {artist_uri}: {total_sales}")
        else:
            print("No sales information found for", artist_uri)
else:
    print("No artist suggestions found for pattern:", pattern)
