class two_hit_wonders_queries:
    # VC - a list of queries to execute external ontologies
    external_ontology_queries = []
    return_Fuseki_results_queries = []
    start_date = ""
    end_date = ""
    hit_threshold = ""
    include_featured_artist = ""
    check_for_group_or_solo = ""
    group_or_solo_query_string = ""

    prefixes = "prefix foaf: <http://xmlns.com/foaf/0.1/> " ""

    def __init__(self, start_date, end_date, hit_threshold, check_for_group_or_solo):
        self.start_date = start_date
        self.end_date = end_date
        self.hit_threshold = hit_threshold
        """
        VC TO DO: Add an if statement here and a checkbox variable to include featured artists in the results
        if Checked add query_dbpedia_isHitSongOf to the list, if not add query_is_primary_song_artist 

        NOTE: IN the return set you will also need to chaneg the variable to get the correct data from 
        Fuseki and display on the site. 
        """
        self.include_featured_artist = True

        """
        VC - This can be set from the front-end, should have a drop down for the following options:
        group - returns results for only groups - executes query: 
        solo - returns results for only solo artists - executes query: 
        both - returns results for both groups amd solo artists - executes query: 
        """
        self.check_for_group_or_solo = check_for_group_or_solo

        #  VC = need a way to reset this on a new selection from the drop down
        # should break out into separate method and call here and any time the query is executed
        match check_for_group_or_solo:
            case "solo":
                self.group_or_solo_query_string = "?artist a dbo:Person. "
            case "group":
                self.group_or_solo_query_string = "?artist a dbo:Group. "
                #  VC - Need to add a union statement here for dbo:Band (ex: https://dbpedia.org/page/Black_Eyed_Peas)

            #  VC - this is the default case and catches the "both" option or if the user doesn't specify
            case _:
                self.group_or_solo_query_string = "?artist a owl:Thing. "

        # VC - constructs a triple in the format  ?song isHitSongOf ?artist
        self.query_dbpedia_isHitSongOf = (
                "CONSTRUCT {?works <http://example.org/isHitSongOf> ?artist} "
                "WHERE {?works a dbo:Song; "
                "dbp:award "
                + self.hit_threshold
                + "; "
                + "dbo:artist ?artist; "  # user defines "hits" as either gold or platinum
                  "dbo:releaseDate ?releaseDate. "
                + self.group_or_solo_query_string
                + 'FILTER( ?releaseDate > "'
                + self.start_date
                + '"^^xsd:date '
                  '&& ?releaseDate < "' + self.end_date + '"^^xsd:date)}'
        )

        # VC - Query to get the literal names of the artists and add to the insert
        query_foaf_artist_name = (
                self.prefixes +
                "CONSTRUCT {?artist_uri foaf:name ?artist} "
                "WHERE {?works a dbo:Song; "
                "dbp:award " + self.hit_threshold + "; "
                + "dbo:artist ?artist_uri; "  # user defines "hits" as either gold or platinum
                "dbo:releaseDate ?releaseDate. "
                "?artist_uri foaf:name ?artist "
                'FILTER( ?releaseDate > "' + self.start_date + '"^^xsd:date '
                '&& ?releaseDate < "' + self.end_date + '"^^xsd:date)}'
        )

        """
        VC - if song belongs to an album using that to determine the primary artist of a song. This, in effect, removes
        the featured artist as the one who has the hit. We can resuse this query in other places as well. 
        """
        query_is_primary_song_artist = (
                "CONSTRUCT {?works <http://example.org/isHitSongOfPrimaryArtist> ?artist} "
                "WHERE {?works a dbo:Song; "
                "dbp:award " + self.hit_threshold + "; " +
                "dbo:artist ?artist_uri; "
                "dbo:releaseDate ?releaseDate; "
                "dbo:album ?works_album. "
                "?works_album dbp:artist ?artist. " + self.group_or_solo_query_string +
                # '?artist a owl:Thing. '
                'FILTER( ?releaseDate > "' + self.start_date + '"^^xsd:date '
                '&& ?releaseDate < "' + self.end_date + '"^^xsd:date)}'
        )
        return_all_isHitSongOfPrimaryArtist_artists = "temp"

        #  VC - here is where we can introduce a case statement
        self.external_ontology_queries.append(self.query_dbpedia_isHitSongOf)
        self.external_ontology_queries.append(query_foaf_artist_name)
        #  external_ontology_queries.append(query_is_primary_song_artist)

    @property
    def return_fuseki_queries(self):
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
        two_hit_wonders_queries.return_Fuseki_results_queries.append(return_all_isHitSongOf_artists)
        return return_all_isHitSongOf_artists  # two_hit_wonders_queries.return_Fuseki_results_queries
