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
        "SELECT distinct count(?artist) ?hometown "
        "WHERE { "
        "?artist dbo:wikiPageWikiLink dbc:Grammy_Award_winners; "
        "rdf:type dbo:Person; "
        "dbo:birthPlace ?hometown . "
        "?hometown rdf:type schema:City .} "
        )

    query_dbpedia_grammys_by_city_group = (prefixes +
        "?artist dbo:wikiPageWikiLink dbc:Grammy_Award_winners; "
        "rdf:type dbo:Group; "
        "dbo:hometown ?hometown . "
        "?hometown rdf:type schema:City .} "
        )

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
    def __init__(self, check_for_group_or_solo):
        self.check_for_group_or_solo = check_for_group_or_solo

        self.gbc_external_ontology_queries.clear()
        if self.check_for_group_or_solo == "solo":
            self.gbc_external_ontology_queries.append(self.query_dbpedia_grammys_by_city_solo)
        elif self.check_for_group_or_solo == "group":
            self.gbc_external_ontology_queries.append(self.query_dbpedia_grammys_by_city_group)
        else:
            self.gbc_external_ontology_queries.append(self.query_dbpedia_grammys_by_city_both)
