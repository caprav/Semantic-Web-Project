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
            'FILTER( ?releaseDate > ' + self.start_date + '"^^xsd:date '
            '&& ?releaseDate < ' + self.end_date + '"^^xsd:date '
            "(isUri(?external_work_URI) || isIri(?external_work_URI)) "
            "&& STRSTARTS(STR(?external_work_URI), STR(wd:)))"
            "} "
            )

    def return_federated_fuseki_wikidata(self):

        store = SPARQLUpdateStore()
        query_endpoint = "http://localhost:3030/music/query"
        update_endpoint = "http://localhost:3030/music/update"
        store.open((query_endpoint, update_endpoint))

        results_federated_query = (self.prefixes +
            "SELECT DISTINCT ?external_work_URI ?country "
            "WHERE { "
            "?dbpedia_work owl:sameAs ?external_work_URI; "
            "dbo:releaseDate ?releaseDate. "
            "SERVICE <https://query.wikidata.org/sparql> { "
            "?external_work_URI p:P495 ?statement. "
            "?statement ps:P495 ?country. "
            "} "
            'FILTER( ?releaseDate > ' + self.start_date + '"^^xsd:date '
            '&& ?releaseDate < ' + self.end_date + '"^^xsd:date '
            "} "
            )
        print(results_federated_query)

        fuseki_result = store.query(results_federated_query)
        print(fuseki_result)
        return "" #  VC -return an array of key/value pairs "country, count"