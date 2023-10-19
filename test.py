from rdflib import Graph
from SPARQLWrapper import SPARQLWrapper, JSON, N3
from pprint import pprint


sparql = SPARQLWrapper('https://dbpedia.org/sparql')
sparql.setQuery('''
    SELECT ?artist ?birthplace
WHERE {
  ?artist a dbo:MusicalArtist ;
          dbo:birthPlace ?birthplace .
}
LIMIT 10
''')
sparql.setReturnFormat(JSON)
qres = sparql.query().convert()

pprint(qres)


#for result in qres['results']['bindings']:
#    print(result['object'])
    
    #lang, value = result['object']['xml:lang'], result['object']['value']
    #print(f'Lang: {lang}\tValue: {value}')
    # if lang == 'en':
        # print(value)