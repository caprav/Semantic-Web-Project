from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore


class TourAttendance_queries:
    gbc_external_ontology_queries = []
    start_date = ""
    end_date = ""
    prefixes = ("prefix foaf:   <http://xmlns.com/foaf/0.1/> "
                "prefix schema: <http://schema.org/> "
                "prefix dbo:    <http://dbpedia.org/ontology/> "
                "prefix dbc:    <http://dbpedia.org/resource/Category:> "
                "prefix dbp:    <http://dbpedia.org/property/>"  
                "prefix rdf:    <http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
                "prefix rdfs:   <http://www.w3.org/2000/01/rdf-schema#> "
                )

    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

        query_dbpedia_tour_attendance = (self.prefixes +
            "CONSTRUCT { "
            "?tour_name rdfs:label ?tour_label;"
            "dbp:artist ?artist_uri ; "
            "dbp:startDate ?tour_start_date; "
            "dbp:attendance ?tour_attendance. "
            "?artist_uri foaf:name ?artist_name. "
            "} "
            "WHERE { "
            "?tour_name dbp:artist ?artist_uri ; "
            "rdfs:label ?tour_label; "
            "dbp:attendance ?tour_attendance; "
            "dbp:startDate ?tour_start_date.  "
            "?artist_uri foaf:name ?artist_name. "
            "FILTER(contains(lcase(?tour_label), 'tour' ) "
            f"&& (?tour_start_date > '{self.start_date}'^^xsd:date) "
            f"&& (?tour_start_date < '{self.end_date}'^^xsd:date) "
            "&& (lang(?tour_label) = 'en')) "
            "}"
        )
        
        
        self.gbc_external_ontology_queries.clear()
        if query_dbpedia_tour_attendance not in self.gbc_external_ontology_queries:
            self.gbc_external_ontology_queries.append(query_dbpedia_tour_attendance)
            
    def return_fuseki_tour_info(self):
        print("inside grammy by city class")
        store = SPARQLUpdateStore()
        query_endpoint = "http://localhost:3030/music/query"
        update_endpoint = "http://localhost:3030/music/update"
        store.open((query_endpoint, update_endpoint))
        print("store is open")

        results_tour_attendance = (self.prefixes +
            "SELECT ?artist_name ?tour_label ?tour_attendance "
            "WHERE {"
            "?tour_name rdfs:label ?tour_label; "
            "dbp:artist ?artist_uri; "
            "dbp:startDate ?tour_start_date; "
            "dbp:attendance ?tour_attendance. "
            "?artist_uri foaf:name ?artist_name. "
            "FILTER((?tour_start_date > '" + self.start_date + "'^^xsd:date ) "
            "&& (?tour_start_date < '" + self.end_date + "'^^xsd:date))" 
            "} "
            )
        print(results_tour_attendance)
        fuseki_result = store.query(results_tour_attendance)
        return_result_dictionary = {}

        for record in fuseki_result:
            temp_tour_name = record.tour_label.toPython()
            temp_artist = record.artist_name.toPython()
            temp_attendance = record.tour_attendance
            return_result_dictionary[temp_tour_name] = [temp_artist, temp_attendance]

        print(return_result_dictionary)
        return return_result_dictionary