# sk-Import necessary libraries and modules
import os
import urllib
from flask_migrate import Migrate
from flask_minify import Minify
from sys import exit
from rdflib import Graph, Namespace, Literal
from rdflib.graph import DATASET_DEFAULT_GRAPH_ID as default
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore
from SPARQLWrapper import SPARQLWrapper, JSON, N3
from pprint import pprint
from two_hit_wonders import (
    external_ontology_queries, return_all_isHitSongOf_artists
)
from hits_by_song_duration import duration_external_ontology_queries
from flask import Flask, render_template, request
from apps.config import config_dict
from apps import create_app, db
import jsonify

# WARNING: Don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False") == "True"

# The configuration
get_config_mode = "Debug" if DEBUG else "Production"

try:
    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit("Error: Invalid <config_mode>. Expected values [Debug, Production] ")

app = create_app(app_config)
Migrate(app, db)

if not DEBUG:
    Minify(app=app, html=True, js=False, cssless=False)


if DEBUG:
    app.logger.info("DEBUG            = " + str(DEBUG))
    app.logger.info("Page Compression = " + "FALSE" if DEBUG else "TRUE")
    app.logger.info("DBMS             = " + app_config.SQLALCHEMY_DATABASE_URI)
    app.logger.info("ASSETS_ROOT      = " + app_config.ASSETS_ROOT)


# Sharayu: Define a route to interact with Fuseki and DBpedia
@app.route("/get_fuseki", methods=["POST"])
def fuseki():
    global tempResult
    print("inside fuseki")

    store = SPARQLUpdateStore()
    query_endpoint = "http://localhost:3030/music/query"
    update_endpoint = "http://localhost:3030/music/update"
    store.open((query_endpoint, update_endpoint))

    querysite = 'dbpedia' # wikidata or dbpedia
    duration_hit_threshold = '"Platinum"@en'
    duration_start_date = "2007-01-01"
    duration_end_date = "2007-03-01"
    prefixes = ("prefix foaf:   <http://xmlns.com/foaf/0.1/> "
                "prefix owl:    <http://www.w3.org/2002/07/owl#> "
                "prefix dbo:    <http://dbpedia.org/ontology/> "
                "prefix dbp:    <http://dbpedia.org/property/> "
                "PREFIX mo:     <http://purl.org/ontology/mo/> "
                "PREFIX p:      <http://www.wikidata.org/prop/> "
                "PREFIX ps:     <http://www.wikidata.org/prop/statement/> "
                "PREFIX wd:     <http://www.wikidata.org/entity/> "
                "PREFIX wds:    <http://www.wikidata.org/entity/statement/> "
                )

    g = Graph(store, identifier=default)
    match querysite:
        case'wikidata':
            print('Querying wikiData')
            sparql = SPARQLWrapper("https://query.wikidata.org/")
            #"https://query.wikidata.org/")  # "https://dbpedia.org/sparql"

            wikidataEndPointUrl = 'https://query.wikidata.org/sparql'


            tempQuery1 = (prefixes + "CONSTRUCT {"
                     "<http://dbpedia.org/resource/Rehab_(Amy_Winehouse_song)> owl:sameAs ?external_work_URI. } "
                     "WHERE { "
                     "<http://dbpedia.org/resource/Rehab_(Amy_Winehouse_song)> owl:sameAs ?external_work_URI. "
                     "FILTER ((isUri(?external_work_URI) || isIri(?external_work_URI)) "
                     "&& STRSTARTS(STR(?external_work_URI), STR(wd:)))"
                     "} "
                     )


            """
             'CONSTRUCT {?external_work <http://example.org/isAHitSongFrom> ?country} '
             # VC - p:P495 = country of origin https://www.wikidata.org/wiki/Property:P495
             'WHERE {?external_work p:P495 ?statement. '
             '?statement ps:P495 ?country '  # :P361 - PartOf                  
             '} LIMIT 100')
             """

            tempQuery2 = (prefixes +
                         'CONSTRUCT {?external_work_URI <http://example.org/isAHitSongFrom> ?country} '
                         # VC - p:P495 = country of origin https://www.wikidata.org/wiki/Property:P495
                         'WHERE {?external_work_URI p:P495 ?statement. '
                         '?statement ps:P495 ?country '
                         '{SERVICE <https://dbpedia.org/sparql> { '
                         'SELECT ?external_work_URI WHERE{'
                         '?works a dbo:Song; '
                         'dbp:award ' + duration_hit_threshold + '; ' +
                         'dbo:releaseDate ?releaseDate; '
                         'owl:sameAs ?external_work_URI. '
                         'FILTER( ?releaseDate > "' + duration_start_date + '"^^xsd:date '
                                '&& ?releaseDate < "' + duration_end_date + '"^^xsd:date '
                                '&& (isUri(?external_work_URI) || isIri(?external_work_URI)) '
                                '&& STRSTARTS(STR(?external_work_URI), STR(wd:))) '                                       
                         '}}}}'
                         )
            print(tempQuery1)
            resultURL = wikidataEndPointUrl + '?query=' + urllib.parse.quote(tempQuery1)
            print(resultURL)
            tempResult = g.parse(location=resultURL)

        case _:
            print('Querying DBPedia')
            sparql = SPARQLWrapper("https://dbpedia.org/sparql")

            tempQuery3 = (prefixes + "CONSTRUCT {"
                                     "<http://dbpedia.org/resource/Rehab_(Amy_Winehouse_song)> owl:sameAs ?external_work_URI. } "
                                     "WHERE { "
                                     "<http://dbpedia.org/resource/Rehab_(Amy_Winehouse_song)> owl:sameAs ?external_work_URI. "
                                     "FILTER ((isUri(?external_work_URI) || isIri(?external_work_URI)) "
                                     "&& STRSTARTS(STR(?external_work_URI), STR(wd:)))"
                                     "} "
                          )
            dbpediaquery= (prefixes +
                          'SELECT ?external_work_URI '
                          # VC - p:P495 = country of origin https://www.wikidata.org/wiki/Property:P495
                          'WHERE {'
                          '?works a dbo:Song; '
                          'dbp:award ' + duration_hit_threshold + '; ' +
                          'dbo:releaseDate ?releaseDate; '
                          'owl:sameAs ?external_work_URI. ' 
                          'FILTER( ?releaseDate > "' + duration_start_date + '"^^xsd:date '
                          '&& ?releaseDate < "' + duration_end_date + '"^^xsd:date '
                          '&& (isUri(?external_work_URI)) && STRSTARTS(STR(?external_work_URI), STR(wd:))) }')
            print(tempQuery3)
            sparql.setQuery(tempQuery3)
            sparql.setReturnFormat(N3)
            query_result = sparql.query().convert()
            print(query_result)

            """
            for query in duration_external_ontology_queries:
                # duration_external_ontology_queries: # external_ontology_queries:
                sparql.setQuery(query)
                sparql.setReturnFormat(N3)
                print('first')
                query_result = sparql.query().convert()
                print('second')
                print(query_result)
                print('third')
                # g.parse(query_result)
            """
            tempResult = g.parse(query_result)

    print(tempResult)

    #  VC - This line actually puts the info into Fuseki
    store.add_graph(tempResult)        #g)

    #  VC - can't use sparql below, need to use the store (pointing to Fuseki), sparql is pointing to dbpedia
    fuseki_result = store.query(return_all_isHitSongOf_artists)

    # sharayu - Process and print the results
    res = """"""

    for record in fuseki_result:
        res += record.artist_name.toPython()

    print(res)

    return render_template("fedrated.html", query_result=res)

if __name__ == "__main__":
    # Change the port to the desired value (e.g., 8080)
    app.run()
