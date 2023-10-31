from rdflib import Graph, Namespace, Literal
from rdflib.graph import DATASET_DEFAULT_GRAPH_ID as default
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore
from SPARQLWrapper import SPARQLWrapper, JSON, N3
from pprint import pprint
from two_hit_wonders import external_ontology_queries  #  query_dbpedia_isHitSongOf, query_foaf_artist_name

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

# pprint(qres)

""" 
Following code is to connect to Fuseki, references:
https://stackoverflow.com/questions/50228032/how-to-store-rdf-data-to-a-triplestore-in-fuseki-sparql-endpoint-using-rdflib-in 
https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.plugins.stores.html#rdflib.plugins.stores.sparqlstore.SPARQLStore 
 """
store = SPARQLUpdateStore()
query_endpoint = "http://localhost:3030/music.ttl/query"
update_endpoint = "http://localhost:3030/music.ttl/update"
store.open((query_endpoint, update_endpoint))

#  VC - probably can delete these 10/31/2023 after some test that they do nothing
#  prefixes = "prefix ex: <http://example.org/>"
#  ns = Namespace("http://example.org/")

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

print(len(g))

for triple in g:
    pprint(triple)

#  VC - This line actually puts the info into Fuseki
store.add_graph(g)

#  VC - can't use sparql below, need to use the store (pointing to Fuseki), sparql is pointing to dbpedia
fuseki_result = store.query(query3)

#  VC - to print in a readable way, this thread helped a lot:
#  https://stackoverflow.com/questions/31629462/how-do-i-print-term-literal-from-rdflib-in-a-readble-way
for record in fuseki_result:
    print(record.artist_name.toPython())


# for result in qres['results']['bindings']:
#    print(result['object'])

# lang, value = result['object']['xml:lang'], result['object']['value']
# print(f'Lang: {lang}\tValue: {value}')
# if lang == 'en':
# print(value)
