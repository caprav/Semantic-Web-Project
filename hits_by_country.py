class hits_by_country_queries:
    countries_external_ontology_queries = []
    start_date = ""
    end_date = ""

    prefixes = (
        "prefix owl:    <http://www.w3.org/2002/07/owl#> "
        "prefix dbo:    <http://dbpedia.org/ontology/> "
        "prefix dbp:    <http://dbpedia.org/property/> "
        "PREFIX mo:     <http://purl.org/ontology/mo/> "
        "PREFIX p:      <http://www.wikidata.org/prop/> "
        "PREFIX ps:     <http://www.wikidata.org/prop/statement/> "
        "PREFIX wd:     <http://www.wikidata.org/entity/> "
        "PREFIX wds:    <http://www.wikidata.org/entity/statement/> "
        )

    def __init__(self, start_date, end_date, hit_threshold, check_for_group_or_solo):
        query_dbpedia_get_sameAs = (self.prefixes +
            "CONSTRUCT {"
            "?dbpedia_works owl:sameAs ?external_work_URI. } "
            "WHERE { "
            "?dbpedia_works owl:sameAs ?external_work_URI. "
            '?works a dbo:Song; '
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