from rdflib import Graph, Namespace
from rdflib.graph import DATASET_DEFAULT_GRAPH_ID as default
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore
from SPARQLWrapper import SPARQLWrapper, JSON, N3
from pprint import pprint


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

prefixes = "prefix ex: <http://example.org/>"
ns = Namespace("http://example.org/")

query1 = ('SELECT distinct ?works ?artist WHERE {?works a dbo:Song; dbp:award "Platinum"@en; dbo:artist ?artist; '
          'dbo:releaseDate ?releaseDate. FILTER( ?releaseDate > "2007-01-01"^^xsd:date && ?releaseDate < '
          '"2007-02-01"^^xsd:date)}')
query2 = ('CONSTRUCT {?works <http://example.org/isHitSongOf> ?artist} WHERE {?works a dbo:Song; dbp:award '
          '"Platinum"@en; dbo:artist ?artist; dbo:releaseDate ?releaseDate. FILTER( ?releaseDate > '
          '"2007-01-01"^^xsd:date && ?releaseDate < "2007-02-01"^^xsd:date)}')

sparql = SPARQLWrapper("https://dbpedia.org/sparql")
sparql.setQuery(query2)
sparql.setReturnFormat(N3)
qres = sparql.query().convert()

# url = "https://dbpedia.org/resource/"
g = Graph(store, identifier=default)
#g = Graph()
# g.parse(url)
g.parse(qres)
print(len(g))

for stmt in g:
    pprint(stmt)

store.add_graph(g)


# for result in qres['results']['bindings']:
#    print(result['object'])

# lang, value = result['object']['xml:lang'], result['object']['value']
# print(f'Lang: {lang}\tValue: {value}')
# if lang == 'en':
# print(value)
