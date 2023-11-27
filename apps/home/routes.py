from apps.home import blueprint
from flask import render_template, request, session, redirect, url_for
from flask_login import login_required,current_user
from jinja2 import TemplateNotFound
from SPARQLWrapper import SPARQLWrapper, JSON, N3
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore
from rdflib import Graph, Namespace, Literal
from rdflib.graph import DATASET_DEFAULT_GRAPH_ID as default
from two_hit_wonders import two_hit_wonders_queries
from hits_by_country import hits_by_country_queries
from grammy_by_city import grammy_by_city_queries
from apps.home.forms import Hitsongsparams,Hitsongs_bycountry,GrammyArtists
from wtforms.validators import DataRequired 
from apps.history import insert_history
import datetime
import re
from apps.history  import query_history
import os

@blueprint.route("/index")
@login_required
def index():
    return render_template("home/index.html", segment="index")

###############
    # Ramya Sree S  11/11/23
    # Routes for Interactive_report and Artist salesreport

@blueprint.route("/interactive_report")
@login_required
def interactive_report():
    option = request.args.get("option")
    dateForm = Hitsongsparams(request.form)
    print(option)
    return render_template(
        "home/interactive_report.html", option=option, segment="interactive_report", form=dateForm
    )

@blueprint.route("/Artists_sales_report")
@login_required
def Artists_sales_report():
    option = request.args.get("option")
    #dateForm = Hitsongsparams(request.form)   Need to call appropriate form class
    print(option)
    return render_template(
        "home/Artists_sales_report.html", option=option, segment="Artists_sales_report"
    )

@blueprint.route("/hits_by_country")
@login_required
def hits_by_country():
    dateForm = Hitsongs_bycountry(request.form)
    option = request.args.get("option")
    return render_template(
        "home/hits_by_country.html", option=option,query_result={}, segment="hits_by_country", form=dateForm
    )

@blueprint.route("/Grammy_Artists")
@login_required
def Grammy_Artists():
    categoryForm= GrammyArtists(request.form)
    option = request.args.get("option")
    return render_template(
        "home/Grammy_Artists.html", option=option,query_result={}, segment="Grammy_Artists", form= categoryForm
    )

@blueprint.route("/reports")
@login_required
def reports():
    return render_template("home/reports.html", segment="reports")

@blueprint.route('/Return')
def Return():
    return redirect(url_for('home_blueprint.reports')) 

################

@blueprint.route("/<template>")
@login_required
def route_template(template):
    try:
        if not template.endswith(".html"):
            template += ".html"
        # Detect the current page
        segment = get_segment(request)
        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)
    
    except TemplateNotFound:
        return render_template("home/page-404.html"), 404

    except:
        return render_template("home/page-500.html"), 500


# Helper - Extract current page name from request
def get_segment(request):
    try:
        segment = request.path.split("/")[-1]
        if segment == "":
            segment = "index"
        return segment
    except:
        return None


# Sharayu: Define a route to interact with Fuseki and DBpedia
@blueprint.route("/get_fuseki", methods=["GET", "POST"])
def fuseki():

    ###############
    # Ramya Sree S  11/11/23
    # Code to Capture form elements type, start date, end date, artist name
    ################
    dateForm = Hitsongsparams(request.form)
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    type = request.form['type']
    artists = request.form['artists']
    
    print(start_date)
    print(end_date)
    print(type)
    print(artists)

    query_class = two_hit_wonders_queries(
        str(start_date), end_date, type, artists
    )
    print(query_class.external_ontology_queries)
    ################

    ###############
    # Sharayu  11/18/23
    # Code to Capture Query attributes like type, start date, end date, artist name
    # Each time user run queries, the data is stored in database to derive insights such as history, inclination of music, fav time period 
    ################

    user_name= current_user.username
    current_date = datetime.date.today().strftime("%Y-%m-%d")
    input_form = type.strip('"') 

    pattern = re.compile(r'(gold|silver|platinum)', re.IGNORECASE)
    matched_word = None
    if pattern.search(input_form):
    # Get the matched word and capitalize the first letter
        matched_word = pattern.search(input_form).group(0).capitalize()
    
    try:
        history_tbl_query = query_class.external_ontology_queries
        enclosed_query = f'"""{history_tbl_query}"""'
        history_data = (user_name, start_date, end_date, matched_word, artists, current_date, enclosed_query, None, None, None)
        print("history_data",history_data)
        insert_history.load_history(history_data)

    except Exception as e:
        print("Error adding row to the history table.", e)    

    try:
        print("inside fuseki")
        option = request.form.get("option")
        print("chosen option is " + str(option))
        # Define SPARQL query to retrieve data from DBpedia
        sparql = SPARQLWrapper("https://dbpedia.org/sparql")
        sparql.setReturnFormat(JSON)
        store = SPARQLUpdateStore()
        query_endpoint = "http://localhost:3030/music/query"
        update_endpoint = "http://localhost:3030/music/update"
        
        store.open((query_endpoint, update_endpoint))
        g = Graph(store, identifier=default)

        for query in query_class.external_ontology_queries:
            print(query)
            sparql.setQuery(query)
            sparql.setReturnFormat(N3)
            query_result = sparql.query().convert()
            g.parse(query_result)

        store.add_graph(g)

        # Can't use sparql below, need to use the store (pointing to Fuseki), sparql is pointing to dbpedia
        fuseki_result = store.query(query_class.return_fuseki_queries)

        return render_template(
            "home/interactive_report.html", option=option,option1=1, query_result=fuseki_result, form=dateForm
        )

    except Exception as e:
        # Handle exceptions or errors here
        print(f"Error: {str(e)}")
        return "An error occurred while querying data.", 500


    ###############
    # Ramya Sree S  11/25/23
    ################
@blueprint.route("/get_hitsbycountry", methods=["GET", "POST"])
def get_hitsbycountry():
    try:
        dateForm = Hitsongs_bycountry(request.form)
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        print(start_date)
        print(end_date)

        query_class = hits_by_country_queries(str(start_date), str(end_date))
        
        sparql = SPARQLWrapper("https://dbpedia.org/sparql")
        sparql.setReturnFormat(JSON)
        
        store = SPARQLUpdateStore()
        query_endpoint = "http://localhost:3030/music/query"
        update_endpoint = "http://localhost:3030/music/update"
        store.open((query_endpoint, update_endpoint))
        
        g = Graph(store, identifier=default)
        
        sparql.setQuery(query_class.countries_external_ontology_queries[0])
        sparql.setReturnFormat(N3)
        query_result = sparql.query().convert()
        g.parse(query_result)

        store.add_graph(g)

        option = request.form.get("option")
        print("chosen option is " + str(option))

        fuseki_result = query_class.return_federated_fuseki_wikidata()
        print("fueski results are available")
        
        return render_template(
            "home/hits_by_country.html", option=option, option1='1', query_result=fuseki_result, form=dateForm
        )

    except Exception as e:
        # Handle exceptions or errors here
        print(f"Error: {str(e)}")
        return "An error occurred while querying data.", 500

 ###############
    # Ramya Sree S  11/26/23
    ################
@blueprint.route("/get_Grammy", methods=["GET", "POST"])
def Grammy():
    try:
        categoryForm = GrammyArtists(request.form)
        artists = request.form['artists']
        query_class = grammy_by_city_queries(artists)
        sparql = SPARQLWrapper("https://dbpedia.org/sparql")
        #  sparql.setReturnFormat(JSON)
        
        store = SPARQLUpdateStore()
        query_endpoint = "http://localhost:3030/music/query"
        update_endpoint = "http://localhost:3030/music/update"
        store.open((query_endpoint, update_endpoint))
        
        g = Graph(store, identifier=default)

        sparql.setQuery(query_class.gbc_external_ontology_queries[0])
        sparql.setReturnFormat(N3)
        query_result = sparql.query().convert()
        g.parse(query_result)
        print(g)

        store.add_graph(g)

        option = request.form.get("option")
        print("chosen option is " + str(option))

        fuseki_result = query_class.return_fuseki_city_info()
        print("fueski results are available")

        return render_template(
            "home/Grammy_Artists.html", option=option, option1='1', query_result=fuseki_result, form=categoryForm
        ) 

    except Exception as e:
        # Handle exceptions or errors here
        print(f"Error: {str(e)}")
        return "An error occurred while querying data.", 500
