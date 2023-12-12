from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore

class hits_by_country_queries:
    countries_external_ontology_queries = []
    start_date = ""
    end_date = ""

    prefixes = (
        "PREFIX rdf:    <http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
        "PREFIX rdfs:   <http://www.w3.org/2000/01/rdf-schema#> "
        "prefix owl:    <http://www.w3.org/2002/07/owl#> "
        "prefix dbo:    <http://dbpedia.org/ontology/> "
        "prefix dbp:    <http://dbpedia.org/property/> "
        "PREFIX dbr:    <http://dbpedia.org/resource/> "
        "PREFIX mo:     <http://purl.org/ontology/mo/> "
        "PREFIX p:      <http://www.wikidata.org/prop/> "
        "PREFIX ps:     <http://www.wikidata.org/prop/statement/> "
        "PREFIX wd:     <http://www.wikidata.org/entity/> "
        "PREFIX wds:    <http://www.wikidata.org/entity/statement/> "
        "PREFIX xsd:    <http://www.w3.org/2001/XMLSchema#> "
        )

    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

        query_dbpedia_get_sameAs = (self.prefixes +
            "CONSTRUCT {"
            "?dbpedia_works owl:sameAs ?external_work_URI. "
            "?dbpedia_works dbo:releaseDate ?releaseDate. "
            "} "
            "WHERE { "
            "?dbpedia_works owl:sameAs ?external_work_URI; "
            'rdf:type dbo:Song; '
            'dbp:award "Platinum"@en; '  # user defines "hits" as either gold or platinum
            'dbo:artist ?artist; '
            'dbo:releaseDate ?releaseDate. '
            '?artist a owl:Thing. '
            'FILTER( ?releaseDate > "' + str(self.start_date) + '"^^xsd:date '
            '&& ?releaseDate < "' + str(self.end_date) + '"^^xsd:date '
            '&& (isURI(?external_work_URI) || isIRI(?external_work_URI)) '
            '&& STRSTARTS(STR(?external_work_URI), STR(wd:)))'
            "} "
        )
        self.countries_external_ontology_queries.clear()
        if query_dbpedia_get_sameAs not in self.countries_external_ontology_queries:
            self.countries_external_ontology_queries.append(query_dbpedia_get_sameAs)

    def return_federated_fuseki_wikidata(self):
        print("inside hits by country wiki class")
        store = SPARQLUpdateStore()
        query_endpoint = "http://localhost:3030/music/query"
        update_endpoint = "http://localhost:3030/music/update"
        store.open((query_endpoint, update_endpoint))
        print("store is open")
        results_federated_query = (self.prefixes +
            "SELECT DISTINCT ?external_work_URI ?label "
            "WHERE { "
            "?dbpedia_work owl:sameAs ?external_work_URI; "
            "dbo:releaseDate ?releaseDate. "
            "SERVICE <https://query.wikidata.org/sparql> { "
            "?external_work_URI p:P495 ?statement. "
            "?statement ps:P495 ?country. "
            "?country rdfs:label ?label "
            "FILTER(lang(?label) = 'en') "
            "} "
            'FILTER( ?releaseDate > "' + str(self.start_date) +
            '"^^xsd:date && ?releaseDate < "' + str(self.end_date) + '"^^xsd:date )'
            "} "
        )
        print(results_federated_query)

        fuseki_result = store.query(results_federated_query)
        print(1)
        for row in fuseki_result.bindings:
            print(row)
        print(2)
        return_result_dictionary = {}
        print(3)
        for record in fuseki_result:
            #  VC - this should get the portion returned by the SELECT ?country in results_federated_query above
            temp_country = record.label.toPython()
            print(4)
            print(temp_country)
            #  VC - https://www.geeksforgeeks.org/python-increment-value-in-dictionary/
            return_result_dictionary[temp_country] = return_result_dictionary.get(temp_country, 0) + 1
        print(5)
        #  VC -return an array of key/value pairs "country, count"
        print(return_result_dictionary)
        return return_result_dictionary
