# VC - a list of queries to execute external ontologies
external_ontology_queries = []
return_Fuseki_results_queries = []
prefixes = "prefix foaf: <http://xmlns.com/foaf/0.1/>"

"""
VC - Here parameterized values for the user to specify @Ramya, these need to be hooked up to front end
"""
start_date = "2002-01-01"  # need to get as input from webpage, might need to cast to a string
end_date = "2008-02-01"  # need to get as input from webpage, might need to cast to a string
hit_threshold = '"Platinum"@en'

"""
VC TO DO: Add an if statement here and a checkbox variable to include featured artists in the results
if Checked add query_dbpedia_isHitSongOf to the list, if not add query_is_primary_song_artist 

NOTE: IN the return set you will also need to chaneg the variable to get the correct data from 
Fuseki and display on the site. 
"""

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

"""
VC - if song belongs to an album using that to determine the primary artist of a song. This, in effect, removes
the featured artist as the one who has the hit. We can resuse this query in other places as well. 
"""

query_is_primary_song_artist =('CONSTRUCT{?works <http://example.org/isHitSongOfPrimaryArtist> ?album_artist} '
                               'WHERE {?works a dbo:Song; '
                               'dbp:award ' + hit_threshold + '; ' +
                               'dbo:artist ?artist_uri; '
                               'dbo:releaseDate ?releaseDate; '
                               'dbo:album ?works_album. '
                               '?works_album dbp:artist ?album_artist. '
                               '?album_artist a owl:Thing. '
                               'FILTER( ?releaseDate > "' + start_date + '"^^xsd:date '
                               '&& ?releaseDate < "' + end_date + '"^^xsd:date)}')

external_ontology_queries.append(query_is_primary_song_artist)


"""
Here are the queries that return results from Fuseki and they can be used on our front-end
"""
return_all_isHitSongOf_artists = (
    "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
    "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> "
    "PREFIX ex: <http://example.org/> "
    "PREFIX foaf: <http://xmlns.com/foaf/0.1/> "
    "SELECT DISTINCT ?artist_name WHERE { "
    "?song ex:isHitSongOf ?artist. "
    "?artist foaf:name ?artist_name "
    "}"
)
return_Fuseki_results_queries.append(return_all_isHitSongOf_artists)

return_all_isHitSongOfPrimaryArtist_artists = "temp"