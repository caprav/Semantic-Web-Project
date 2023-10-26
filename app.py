from flask import Flask, render_template, request
from rdflib import Graph, Namespace, URIRef
from rdflib.graph import DATASET_DEFAULT_GRAPH_ID as default
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore
from SPARQLWrapper import SPARQLWrapper, JSON, N3, TURTLE, RDF
from pprint import pprint
from pyfuseki import AsyncFuseki, FusekiUpdate, register
from pyfuseki.utils import RdfUtils
from pyfuseki.rdf import rdf_prefix, NameSpace as name_space, rdf_property

app = Flask(__name__, static_folder='static')

# Load the ontology graph globally
graph = Graph()
#graph.parse('/Users/gaurav/Programming/ontology/PizzaTutorial.owl', format='xml')

# Get the namespace of the graph
ns = Namespace("http://example.org/")
#graph.bind('ns', ns)

# VPC: You will need to install apache-jena-fuseki-4.9.0 (https://jena.apache.org/download/) on 
#   your PC. Then you need to create dataDir folder in the install directory. 
#   Then run the persistent cmd: 'fuseki-server --update --loc=dataDir /music.ttl' to launch the server
async_fuseki_server = AsyncFuseki('http://localhost:3030/#/dataset/', 'music.ttl') 
async_fuseki_update = FusekiUpdate('http://localhost:3030/#/dataset/', 'music.ttl')

#custom_property_isHitSongOf = 'http://example.org/isHitSongOf'
#instead of the preceding line, trying this:
""" @rdf_property('http://example.org/')
class ObjectProperty():
    isHitSongOf: uri
op = ObjectProperty() """

@rdf_prefix('http://example.org/')
class RDFPrefix():
    Artist: name_space
    Song: name_space
rp = RDFPrefix()

artist_1  = URIRef('Vincent', ns)
song_1 = URIRef('MySong', ns)
graph_1 = Graph(store, identifier=default)

graph_1.add((song_1, URIRef('isHitSongOf',ns), artist_1))
async_fuseki_update.insert_graph(graph_1)
#print(async_fuseki_update.fuseki_url)

def execute_query_and_format_result(sparql_query: str) -> str:
    result = graph.query(sparql_query)

    if result:
        result_list = [str(row) for row in result]
        return "\n".join(result_list)

    else:
        return "No result found or error in query."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query.html')
def query():
    return render_template('query.html')



@app.route('/execute-query', methods=['POST'])
def execute_query():
    query = request.form['query']
    sparql = SPARQLWrapper('https://dbpedia.org/sparql')
    sparql.setQuery(query)
    sparql.setReturnFormat(RDF)
    qres = sparql.query().convert()



    print(qres)
    # Prepend PREFIX declarations to the query
    #query = 'PREFIX ns: <http://www.semanticweb.org/gaurav/ontologies/2023/1/PizzaTutorial#> ' + query
    #query_result = execute_query_and_format_result(query)
    return render_template('query.html', query_result=qres)

if __name__ == '__main__':
    app.run(debug=True, port=3003)
