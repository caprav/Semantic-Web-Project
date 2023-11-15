from two_hit_wonders import query_dbpedia_isHitSongOf

# VC - a list of queries to execute external ontologies
duration_external_ontology_queries = []
duration_return_Fuseki_results_queries = []

prefixes = ("prefix foaf:   <http://xmlns.com/foaf/0.1/> "
            "prefix owl:    <http://www.w3.org/2002/07/owl#> "
            "PREFIX mo:     <http://purl.org/ontology/mo/> "
            "PREFIX p:      <http://www.wikidata.org/prop/> "
            "PREFIX wd:     <http://www.wikidata.org/entity/> "
            "PREFIX wds:    <http://www.wikidata.org/entity/statement/> "
            )

duration_start_date = "2007-01-01"  # need to get as input from webpage, might need to cast to a string
duration_end_date = "2007-03-01"  # need to get as input from webpage, might need to cast to a string
duration_hit_threshold = '"Platinum"@en'

query_dbpedia_sameAs_song = ('CONSTRUCT {?works owl:sameAs ?external_work} '
                             'WHERE {?works a dbo:Song; '
                             'dbp:award ' + duration_hit_threshold + '; ' +  # user defines "hits" as either gold or platinum
                             #'dbo:artist ?artist; '
                             'dbo:releaseDate ?releaseDate; '
                             'owl:sameAs ?external_work. ' 
                             # group_or_solo_query_string +
                             'FILTER( ?releaseDate > "' + duration_start_date + '"^^xsd:date '
                             '&& ?releaseDate < "' + duration_end_date + '"^^xsd:date)}')

query_wikidata_country_of_origin = (prefixes +
                          'CONSTRUCT {?external_work <http://example.org/isAHitSongFrom> ?country} '
                          # VC - p:P495 = country of origin https://www.wikidata.org/wiki/Property:P495
                          'WHERE {?external_work p:P495 ?country. '                           
                          'SERVICE <https://dbpedia.org/sparql> {'
                          '?works a dbo:Song; '
                          'dbp:award ' + duration_hit_threshold + '; ' +
                          'dbo:releaseDate ?releaseDate; '
                          'owl:sameAs ?external_work. ' 
                          'FILTER( ?releaseDate > "' + duration_start_date + '"^^xsd:date '
                          '&& ?releaseDate < "' + duration_end_date + '"^^xsd:date)}}')

createJustlittleTestQueryForwikidata = (prefixes +
                          'CONSTRUCT {?external_work <http://example.org/isAHitSongFrom> ?country} '
                          # VC - p:P495 = country of origin https://www.wikidata.org/wiki/Property:P495
                          'WHERE {?external_work p:P495 ?country. '         # :P361 - PartOf                  
                          '} LIMIT 100')



# dbp:label # like the label columbia from the dbpedia link

#  duration_external_ontology_queries.append(query_dbpedia_isHitSongOf)
#  duration_external_ontology_queries.append(query_dbpedia_sameAs_song)
#  duration_external_ontology_queries.append(query_wikidata_country_of_origin)
duration_external_ontology_queries.append(createJustlittleTestQueryForwikidata)
