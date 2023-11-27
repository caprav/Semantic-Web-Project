from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore


class grammy_by_city_queries:
    gbc_external_ontology_queries = []
    gbc_return_Fuseki_results_queries = []
    check_for_group_or_solo = ""
    prefixes = ("prefix foaf:   <http://xmlns.com/foaf/0.1/> "
                "prefix schema: <http://schema.org/> "
                "prefix dbo:    <http://dbpedia.org/ontology/> "
                "prefix dbc:    <http://dbpedia.org/resource/Category:> "
                "prefix rdf:    <http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
                )

    query_dbpedia_grammys_by_city_solo = (prefixes +
        "CONSTRUCT { "
        "?artist dbo:wikiPageWikiLink dbc:Grammy_Award_winners;  "
        "rdf:type dbo:Person; "
        "dbo:birthPlace ?hometown_name .  "
        "}"
        "WHERE { "
        "?artist dbo:wikiPageWikiLink dbc:Grammy_Award_winners; "
        "rdf:type dbo:Person; "
        "dbo:birthPlace ?hometown . "
        "?hometown rdf:type schema:City; "
        "rdfs:label ?hometown_name "
        "FILTER (lang(?hometown_name) = 'en') "
        "} "
        )

    query_dbpedia_grammys_by_city_group = (prefixes +
        "CONSTRUCT { "
        "?artist dbo:wikiPageWikiLink dbc:Grammy_Award_winners; "
        "rdf:type dbo:Group; "
        "dbo:hometown ?hometown_name . "
        "} "
        "WHERE { "
        "?artist dbo:wikiPageWikiLink dbc:Grammy_Award_winners; "
        "rdf:type dbo:Group; "
        "dbo:hometown ?hometown . "
        "?hometown rdf:type schema:City; "
        "rdfs:label ?hometown_name "
        "FILTER (lang(?hometown_name) = 'en') "
        "} "
        )

    #  VC - might be able to delete this if I run through a for look in routes.py
    """
    query_dbpedia_grammys_by_city_both = (prefixes +
        "SELECT distinct count(?artist) ?hometown "
        "WHERE { "
        "rdf:type dbo:Person; "
        "dbo:birthPlace ?hometown . "
        "?hometown rdf:type schema:City .} "
        "UNION "
        "{?artist dbo:wikiPageWikiLink dbc:Grammy_Award_winners; "
        "rdf:type dbo:Group; "
        "dbo:hometown ?hometown . "
        "?hometown rdf:type schema:City .} "
        "} "
        )
    """
    def __init__(self, check_for_group_or_solo):
        self.check_for_group_or_solo = check_for_group_or_solo

        self.gbc_external_ontology_queries.clear()
        if self.check_for_group_or_solo == "solo":
            self.gbc_external_ontology_queries.append(self.query_dbpedia_grammys_by_city_solo)
        elif self.check_for_group_or_solo == "group":
            self.gbc_external_ontology_queries.append(self.query_dbpedia_grammys_by_city_group)
        else:
            self.gbc_external_ontology_queries.append(self.query_dbpedia_grammys_by_city_solo)
            self.gbc_external_ontology_queries.append(self.query_dbpedia_grammys_by_city_group)

    def return_fuseki_city_info(self):
        print("inside grammy by city class")
        store = SPARQLUpdateStore()
        query_endpoint = "http://localhost:3030/music/query"
        update_endpoint = "http://localhost:3030/music/update"
        store.open((query_endpoint, update_endpoint))
        print("store is open")

        results_grammy_city_query_solo = (self.prefixes +
            "SELECT ?hometown_name (COUNT(?artist) AS ?total)  "
            "WHERE { "
            "?artist dbo:wikiPageWikiLink dbc:Grammy_Award_winners; "
            "rdf:type dbo:Person; "
            "dbo:birthPlace ?hometown_name. "
            "} "
            "GROUP BY ?hometown_name "
            )
        results_grammy_city_query_group = (self.prefixes +
            "SELECT ?hometown_name (COUNT(?artist) AS ?total) "
            "WHERE { "
            "?artist dbo:wikiPageWikiLink dbc:Grammy_Award_winners; "
            "rdf:type dbo:Group; "
            "dbo:hometown ?hometown_name . "
            "} "
            "GROUP BY ?hometown_name "
            )

        results_grammy_city_query_both = (self.prefixes +
            "SELECT ?hometown_name (COUNT(?artist) AS ?total) "
            "WHERE { "
            "{?artist dbo:wikiPageWikiLink dbc:Grammy_Award_winners;  "
            "rdf:type dbo:Person; "
            "dbo:birthPlace ?hometown_name .}"
            "UNION "
            "{?artist dbo:wikiPageWikiLink dbc:Grammy_Award_winners; "
            "rdf:type dbo:Group; "
            "dbo:hometown ?hometown_name .}"
            "}"
            "GROUP BY ?hometown_name "
            )
        print(results_grammy_city_query_solo)


        if self.check_for_group_or_solo == "solo":
            fuseki_result = store.query(results_grammy_city_query_solo)
        elif self.check_for_group_or_solo == "group":
            fuseki_result = store.query(results_grammy_city_query_group)
        else:
            fuseki_result = store.query(results_grammy_city_query_both)

        #  fuseki_result = store.query(results_grammy_city_query_solo)
        print(fuseki_result)

        return_result_dictionary = {}
        for record in fuseki_result:
            #  print(record) #  VC - for troubleshooting
            temp_city = record.hometown_name.toPython()
            temp_count = record.total
            #  print(temp_city + "\t" + temp_count) #  VC - for troubleshooting
            return_result_dictionary[temp_city] = temp_count

        #  print(return_result_dictionary) #  VC - for troubleshooting
        return return_result_dictionary
