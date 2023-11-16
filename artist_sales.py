class artist_sales_queries:
    """VC - THis entire query is constructed for the sales of songs only,
    We can add the option for album sales if worthwhile"""

    user_input_artist_search =""
    query_dbpedia_matching_artists = ""
    query_dbpedia_total_artist_sales = ""

    prefixes = ("prefix foaf: <http://xmlns.com/foaf/0.1/> "
                "prefix dbo: <http://dbpedia.org/ontology/> "
                "prefix dbp: <http://dbpedia.org/property/> "
                )


    def __init__(self, user_input_artist_search):
        self.user_input_artist_search = user_input_artist_search

        """
        VC - Here we are going to find all artists that contain the substring proposed by the user
        """

        query_dbpedia_matching_artists = (self.prefixes +
                "CONSTRUCT {?artist_uri foaf:name ?artist_name."
                "?artist a <http://example.org/coolGuy>. "
                "??} " #THIS IS A TEST TO SEE IF MULTI STRINGS CAN GET SAVED
                "WHERE {?works dbo:artist ?artist_uri; "
                "a dbo:Song. "
                "?artist_uri foaf:name ?artist_name "
                "filter( contains (lcase(?artist_name), 'rush')) " # to replace rush user_input_artist_search.lower()
                "} "
        )

        #  Just store all the foaf terms, then rerun a fuseki search to get the names to
        #  display back on the page to the user. Then the user can select one such name from the list
        #  Once the name is selected then we can plug into the next DBPedia query:


    def query_total_sales_of_artist(self, confirmed_artist_name):

        "Need to get the confirmed artist name URI from the fuseki DB to plug into next query:"

        """
        VC - This query will construct all of the songs belonging to the artist
        and the sales of that song
        """
        query_dbpedia_total_artist_sales = (self.prefixes +
                "CONSTRUCT {?works dbp:sales ?song_sales_amount. "
                "?works dbo:artist dbr:Amy_Winehouse.}" # for now use Winehouse to test, but confirmed_artist_name URI after
                "WHERE {?works dbo:artist dbr:Amy_Winehouse; " # for now use Winehouse to test but confirmed_artist_name URI after
                "a dbo:Song; "
                "dbp:salesamount ?sales }"
        )

        total_artist_sales = 0
        result_set = ""
        """Then here can directly query the Fuseki DB and loop through the results to return an int value, 
          but for now print a result"""
        for result in result_set:
            #total_artist_sales += result_set.salesvalue , somethign like this
            print("something")

        print(total_artist_sales)
