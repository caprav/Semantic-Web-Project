# VC - a list of queries to execute external ontologies
external_ontology_queries = []
prefixes = "prefix foaf: <http://xmlns.com/foaf/0.1/>"

"""
VC - Here parameterized values for the user to specify @Ramya, these need to be hooked up to front end
"""
start_date = "2002-01-01"  # need to get as input from webpage, might need to cast to a string
end_date = "2008-02-01"  # need to get as input from webpage, might need to cast to a string
hit_threshold = '"Platinum"@en' #  VC - or "Gold"

# VC - constructs a triple in the format  ?song isHitSongOf ?artist
query_dbpedia_isHitSongOf = ('CONSTRUCT {?works <http://example.org/isHitSongOf> ?artist} '
                             'WHERE {?works a dbo:Song; '
                             'dbp:award ' + hit_threshold + '; ' +  # user defines "hits" as either gold or platinum
                             'dbo:artist ?artist; '
                             'dbo:releaseDate ?releaseDate. '
                             'FILTER( ?releaseDate > "' + start_date + '"^^xsd:date '
                             '&& ?releaseDate < "' + end_date + '"^^xsd:date)}')
external_ontology_queries.append(query_dbpedia_isHitSongOf)

# VC - Query to get the literal names of the artists and add to the insert
query_foaf_artist_name = (prefixes +
                          'CONSTRUCT {?artist_uri foaf:name ?artist} '
                          'WHERE {?works a dbo:Song; '
                          'dbp:award ' + hit_threshold + '; ' +  # user defines "hits" as either gold or platinum
                          'dbo:artist ?artist_uri; '
                          'dbo:releaseDate ?releaseDate. '
                          '?artist_uri foaf:name ?artist '
                          'FILTER( ?releaseDate > "' + start_date + '"^^xsd:date '
                          '&& ?releaseDate < "' + end_date + '"^^xsd:date)}')
external_ontology_queries.append(query_foaf_artist_name)

# VC - Need a query that returns the primary artis of a song. Can be done using
"""
if song belongs to an album use that > IE primary artist is the one who recorded the album
else, other idea, some other source have maybe some type of property? that defines this
What about songs that don't belong to any album? billing order on the listing?
"""


