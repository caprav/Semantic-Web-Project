from flask import Flask, render_template, request
from rdflib import Graph, Namespace
from rdflib import Graph
from SPARQLWrapper import SPARQLWrapper, JSON, N3
from pprint import pprint

app = Flask(__name__, static_folder='static')

# Load the ontology graph globally
graph = Graph()
graph.parse('/Users/gaurav/Programming/ontology/PizzaTutorial.owl', format='xml')

# Get the namespace of the graph
ns = Namespace("http://www.semanticweb.org/gaurav/ontologies/2023/1/PizzaTutorial#")
graph.bind('ns', ns)

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
    sparql.setReturnFormat(JSON)
    qres = sparql.query().convert()
    print(qres)
    # Prepend PREFIX declarations to the query
    #query = 'PREFIX ns: <http://www.semanticweb.org/gaurav/ontologies/2023/1/PizzaTutorial#> ' + query
    #query_result = execute_query_and_format_result(query)
    return render_template('query.html', query_result=qres)

if __name__ == '__main__':
    app.run(debug=True, port=3003)
    

