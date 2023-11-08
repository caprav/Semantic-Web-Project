from two_hit_wonders import query_dbpedia_isHitSongOf

# VC - a list of queries to execute external ontologies
duration_external_ontology_queries = []
duration_return_Fuseki_results_queries = []

prefixes = ("prefix foaf: <http://xmlns.com/foaf/0.1/> "
            "prefix owl:  <http://www.w3.org/2002/07/owl#> "
            "PREFIX mo: <http://purl.org/ontology/mo/> "
            "")

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

query_mbrainz_duration = ('CONSTRUCT {?external_work <http://example.org/hasDuration> ?duration} '
                          'WHERE {?external_work mo:length ?duration. '
                          'SERVICE <https://dbpedia.org/sparql> {'
                          '?works a dbo:Song; '
                          'dbp:award ' + duration_hit_threshold + '; ' +
                          'dbo:releaseDate ?releaseDate; '
                          'owl:sameAs ?external_work. ' 
                          'FILTER( ?releaseDate > "' + duration_start_date + '"^^xsd:date '
                          '&& ?releaseDate < "' + duration_end_date + '"^^xsd:date)}}')

#  duration_external_ontology_queries.append(query_dbpedia_isHitSongOf)
#  duration_external_ontology_queries.append(query_dbpedia_sameAs_song)
duration_external_ontology_queries.append(query_mbrainz_duration)
