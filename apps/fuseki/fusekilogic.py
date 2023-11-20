from rdflib import Graph, Namespace
from rdflib.graph import DATASET_DEFAULT_GRAPH_ID as default
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore
from SPARQLWrapper import SPARQLWrapper, JSON, N3
from apps.fuseki.two_hit_wonders import external_ontology_queries


def fueski_query_execution(on_demand_query):
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")
    sparql.setQuery("""
        SELECT ?artist ?birthplace
        WHERE {
        ?artist a dbo:MusicalArtist ;
                dbo:birthPlace ?birthplace .
        }
        LIMIT 10
    """)
    sparql.setReturnFormat(JSON)
    qres = sparql.query().convert()

    Fuseki_database = SPARQLUpdateStore()
    query_endpoint = "http://localhost:3030/music/query"
    update_endpoint = "http://localhost:3030/music/update"
    Fuseki_database.open((query_endpoint, update_endpoint))

 

    sparql = SPARQLWrapper("https://dbpedia.org/sparql")

    g = Graph(Fuseki_database, identifier=default)

    for query in external_ontology_queries:
        sparql.setQuery(query)
        sparql.setReturnFormat(N3)
        query_result = sparql.query().convert()
        g.parse(query_result)

    Fuseki_database.add_graph(g)
    quoted_query = (on_demand_query) 
    

    


    print("Query Here",quoted_query)


    



    fuseki_result = Fuseki_database.query(quoted_query)

    result = ""  # Initialize result as an empty string

    for record in fuseki_result:
        result += (record.artist_name.toPython())


    return result;     
