from SPARQLWrapper import SPARQLWrapper, JSON

def get_grammyw_values():
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")
    sparql.setQuery("""
        SELECT ?resource ?value
        WHERE {
            ?resource <http://dbpedia.org/property/grammyw> ?value
        }
        ORDER BY ?resource ?value
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

# Run the query
grammyw_results = get_grammyw_values()

if grammyw_results and grammyw_results["results"]["bindings"]:
    for result in grammyw_results["results"]["bindings"]:
        resource = result["resource"]["value"]
        value = result["value"]["value"]
        print(f"Resource: {resource}, Value: {value}")
else:
    print("No results found for the query.")
