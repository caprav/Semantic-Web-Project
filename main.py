from bs4 import BeautifulSoup
import requests
import re

results_array = []

test_search_Query = 'SELECT distinct ?works ?artist WHERE {?works a dbo:Song; dbp:award "Platinum"@en; dbo:artist ?artist; dbo:releaseDate ?releaseDate. FILTER( ?releaseDate > "2007-01-01"^^xsd:date && ?releaseDate < "2007-02-01"^^xsd:date)}'

"""
FOR DBPEDIA ONLY!!!
This class generates a string object formatted to the output results of a Query. It 
Can then be used with a get request to scrape the results 
"""
class DBPediaQueryResultsURLGenerator:
    BaseURLHeader = 'https://dbpedia.org/sparql?default-graph-uri=http%3A%2F%2Fdbpedia.org&query='
    BaseURLTrailer = '&format=text%2Fhtml&timeout=30000&signal_void=on&signal_unconnected=on'

    def __init__(self, Input_Query_String):
        self.Input_Query_String = Input_Query_String

    """
    Some notes on the URL character conversions:
    %3F = ?
    %3A = : colon
    %3B = ; semi-colon
    %7B = {
    %7D = }
    %40 = @
    %5E = ^
    %22 = "
    %3C = <
    %3E = > 
    %26 = &
    %28 = (
    %29 = )
    .

    Full info can be found: https://www.werockyourweb.com/url-escape-characters/
    """

    @staticmethod
    def create_query_results_URL(query_text):
        query_text = query_text.replace('?', '%3F')
        query_text = query_text.replace(':', '%3A')
        query_text = query_text.replace(';', '%3B')
        query_text = query_text.replace('{', '%7B')
        query_text = query_text.replace('}', '%7D')
        query_text = query_text.replace('@', '%40')
        query_text = query_text.replace('^', '%5E')
        query_text = query_text.replace('"', '%22')
        query_text = query_text.replace('<', '%3C')
        query_text = query_text.replace('>', '%3E')
        query_text = query_text.replace('&', '%26')
        query_text = query_text.replace('(', '%28')
        query_text = query_text.replace(')', '%29')
        query_text = query_text.replace(' ', '+')
        return (DBPediaQueryResultsURLGenerator.BaseURLHeader
                + query_text +
                DBPediaQueryResultsURLGenerator.BaseURLTrailer)


# This gets all the HTML from a target page with known results
results_url = DBPediaQueryResultsURLGenerator.create_query_results_URL(test_search_Query)
html_text = requests.get(results_url).text
print(results_url)
"""
html_text = requests.get(
    'https://dbpedia.org/sparql?default-graph-uri=http%3A%2F%2Fdbpedia.org&query='
    'SELECT+distinct+%3Fworks+%3Fartist%0D%0AWHERE+%7B%0D%0A%3Fworks+a+dbo%3ASong%3B+'
    '+%0D%0Adbp%3Aaward+%22Platinum%22%40en%3B+%23+%22Gold%22%40en%3B+%0D%0Adbo%3Aartist'
    '+%3Fartist%3B+%23+can+also+use+dbp%3A%2Fdbo%3Aartist+it+seems+dbo+seems+to+give+'
    'better+results%0D%0Adbo%3AreleaseDate+%3FreleaseDate.+%0D%0A%23%3Fartist'
    '+rdfs%3Alabel+rdfs%3Aliteral.+%23not+sure+why+this+doesn%27t+work%0D%0A%23%3Fartist'
    '+a+dbr%3Atype%0D%0A%0D%0AFILTER%28+%3FreleaseDate+%3E+%222007-01-01%22%5E%5Exsd%3Adate+'
    '%26%26+%3FreleaseDate+%3C+%222007-02-01%22%5E%5Exsd%3Adate%29%0D%0A%7D%0D%0A%0D%0A&format'
    '=text%2Fhtml&timeout=30000&signal_void=on&signal_unconnected=on').text
"""

soup = BeautifulSoup(html_text, 'lxml')
data_table_records = soup.find_all('tr')

for record in data_table_records:
    results_array = record.find_all_next('a')
    hit_songs_URI = results_array[0].text
    artist_URI = results_array[1].text
    print(hit_songs_URI)
    print(artist_URI)
    print("\n")


    """
    FOR DBPEDIA ONLY!!!
    This class generates a string object formatted to the output results of a Query. It 
    Can then be used with a get request to scrape the results 
    """
