# sk-Import necessary libraries and modules
import os
from   flask_migrate import Migrate
from   flask_minify  import Minify
from   sys import exit
from rdflib import Graph, Namespace, Literal
from rdflib.graph import DATASET_DEFAULT_GRAPH_ID as default
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore
from SPARQLWrapper import SPARQLWrapper, JSON, N3
from pprint import pprint
from two_hit_wonders import external_ontology_queries  #  query_dbpedia_isHitSongOf, query_foaf_artist_name
from flask import Flask, render_template, request
from apps.config import config_dict
from apps import create_app, db
import jsonify 


 


# WARNING: Don't run with debug turned on in production!
DEBUG = (os.getenv('DEBUG', 'False') == 'True')

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:

    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app(app_config)
Migrate(app, db)

if not DEBUG:
    Minify(app=app, html=True, js=False, cssless=False)

    
 
if DEBUG:
    app.logger.info('DEBUG            = ' + str(DEBUG)             )
    app.logger.info('Page Compression = ' + 'FALSE' if DEBUG else 'TRUE' )
    app.logger.info('DBMS             = ' + app_config.SQLALCHEMY_DATABASE_URI)
    app.logger.info('ASSETS_ROOT      = ' + app_config.ASSETS_ROOT )




# Sharayu: Define a route to interact with Fuseki and DBpedia
@app.route('/get_fuseki',methods =['POST'])

def fuseki():
    print("inside fuseki")

    #query1= request.form['query']

    

# Sharayu: Define SPARQL query to retrieve data from DBpedia


    sparql = SPARQLWrapper("https://dbpedia.org/sparql")
    sparql.setQuery(
        """
        SELECT ?artist ?birthplace
    WHERE {
    ?artist a dbo:MusicalArtist ;
            dbo:birthPlace ?birthplace .
    }
    LIMIT 10
    """
    )
    sparql.setReturnFormat(JSON)
    qres = sparql.query().convert()

    store = SPARQLUpdateStore()
    query_endpoint = "http://localhost:3030/music/query"
    update_endpoint = "http://localhost:3030/music/update"
    store.open((query_endpoint, update_endpoint))

    query1 = ('SELECT distinct ?works ?artist WHERE {?works a dbo:Song; dbp:award "Platinum"@en; dbo:artist ?artist; '
          'dbo:releaseDate ?releaseDate. FILTER( ?releaseDate > "2007-01-01"^^xsd:date && ?releaseDate < '
          '"2007-02-01"^^xsd:date)}')
    query2 = ('CONSTRUCT {?works <http://example.org/isHitSongOf> ?artist} WHERE {?works a dbo:Song; dbp:award '
          '"Platinum"@en; dbo:artist ?artist; dbo:releaseDate ?releaseDate. FILTER( ?releaseDate > '
          '"2007-01-01"^^xsd:date && ?releaseDate < "2007-02-01"^^xsd:date)}')
    query3 = ('PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> '
          'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> '
          'PREFIX ex: <http://example.org/> '
          'PREFIX foaf: <http://xmlns.com/foaf/0.1/> '
          'SELECT DISTINCT ?artist_name WHERE { '
          '?song ex:isHitSongOf ?artist. '
          '?artist foaf:name ?artist_name '
          '}')


    sparql = SPARQLWrapper("https://dbpedia.org/sparql")

    g = Graph(store, identifier=default)

    for query in external_ontology_queries:
        sparql.setQuery(query)
        sparql.setReturnFormat(N3)
        query_result = sparql.query().convert()
        g.parse(query_result)

     

    

    #  VC - This line actually puts the info into Fuseki
    store.add_graph(g)

    

    #  VC - can't use sparql below, need to use the store (pointing to Fuseki), sparql is pointing to dbpedia
    fuseki_result = store.query(query3)

# sharayu - Process and print the results
    res=""""""

    for record in fuseki_result:
        res+= (record.artist_name.toPython())


    print(res)    


    

     


    return render_template('fedrated.html', query_result=qres)

  
if __name__ == "__main__":
    # Change the port to the desired value (e.g., 8080)
    app.run()

