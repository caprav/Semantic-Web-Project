"""
Author: Sharayu
Created a new route file to handle dbpedia logic 

"""

from apps.dbpedia import blueprint
from flask import render_template, request, session, redirect, url_for
from flask_login import login_required,current_user
from jinja2 import TemplateNotFound
import os
from SPARQLWrapper import SPARQLWrapper, JSON
import urllib.parse




@blueprint.route('/get_artist', methods=['POST'])
@login_required
def get_artist():

    pattern = request.form['artistName']
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")
    sparql.setQuery("""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        SELECT DISTINCT ?artist ?artist_name WHERE {{
            ?artist a dbo:MusicalArtist ;
                    foaf:name ?artist_name .
            FILTER(CONTAINS(LCASE(str(?artist_name)), LCASE("{pattern}")))
        }}
       
    """.format(pattern=pattern.lower()))
    sparql.setReturnFormat(JSON)
    suggestions = sparql.query().convert()
    artist_names = []

    if suggestions and suggestions["results"]["bindings"]:
        for suggestion in suggestions["results"]["bindings"]:
            artist_uri = suggestion['artist']['value']
            print(f"\nArtist URI: {artist_uri}")
            artist_name = artist_uri.split('/')[-1]
            artist_name = artist_name.replace('(', '').replace(')', '')
            artist_names.append(artist_name)

    return render_template('home/Artists_sales_report.html', artist_names=artist_names) 





@blueprint.route('/get_sales', methods=['POST'])
def get_sales():
    artist_name = request.form['selectArtist']
    
    # Extracting the artist name from the URI
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")
    sparql.setQuery("""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dbp: <http://dbpedia.org/property/>
        PREFIX dbr: <http://dbpedia.org/resource/>
        SELECT DISTINCT ?work ?sales WHERE {{
            ?work dbo:artist dbr:{artist_name} ;
                  a dbo:Song ;
                  dbp:salesamount ?sales.
        }}
    """.format(artist_name=artist_name))
    
    sparql.setReturnFormat(JSON)
    sales_info = sparql.query().convert()
    
    total_sales = 0
    info_message = None

    if sales_info and 'results' in sales_info and 'bindings' in sales_info['results']:
        for sale in sales_info["results"]["bindings"]:
            if 'sales' in sale and 'value' in sale['sales']:
                try:
                    sales = float(sale['sales']['value'])
                    total_sales += sales
                except ValueError:
                    error_message = 'Invalid sales value: {}'.format(sale['sales']['value'])
                    print(error_message)
    
    if total_sales == 0:
        info_message = 'Sales information not available for the selected artist.'

    return render_template('home/Artists_sales_report.html', total_sales=total_sales, info_message=info_message)