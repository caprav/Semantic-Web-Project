from apps.home import blueprint
from flask import render_template, request, session
from flask_login import login_required
from jinja2 import TemplateNotFound
from SPARQLWrapper import SPARQLWrapper, JSON, N3
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore
from rdflib import Graph, Namespace, Literal
from rdflib.graph import DATASET_DEFAULT_GRAPH_ID as default
from two_hit_wonders import two_hit_wonders_queries
from apps.templates.forms import Date
from wtforms.validators import DataRequired

@blueprint.route("/index")
@login_required
def index():
    return render_template("home/index.html", segment="index")


@blueprint.route("/interactive_report")
@login_required
def interactive_report():
    option = request.args.get("option")

    return render_template(
        "home/interactive_report.html", option=option, segment="interactive_report"
    )


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
    # go and get the 4 parameters from interactive_report and pass it to
    # two_hit_wonders.py username = request.form['username'] password = request.form['password']

    dateForm = Date(request.form)
    # if dateForm.validate_on_submit():
    # session['startDate'] = dateForm.startDate.data
    # session['endDate'] = dateForm.endDate.data
    start_date = request.form['start_date']
    print(start_date)

    query_class = two_hit_wonders_queries(
        str(start_date), "2023-11-10", '"Platinum"@en', "both"
    )

    try:
        print("inside fuseki")
        option = request.args.get("option")
        # Define SPARQL query to retrieve data from DBpedia
        sparql = SPARQLWrapper("https://dbpedia.org/sparql")

        print("Sparql query built for DBpedia")

        sparql.setReturnFormat(JSON)

        store = SPARQLUpdateStore()
        query_endpoint = "http://localhost:3030/music/query"
        update_endpoint = "http://localhost:3030/music/update"
        store.open((query_endpoint, update_endpoint))

        print("Store, endpoints set, and store opened")

        g = Graph(store, identifier=default)

        print("called graph method")

        for query in query_class.external_ontology_queries:
            print(query)
            sparql.setQuery(query)
            sparql.setReturnFormat(N3)
            query_result = sparql.query().convert()
            g.parse(query_result)

        print("for each query called the for loop to get results")

        # This line actually puts the info into Fuseki
        store.add_graph(g)

        print("ading graph to store")

        # Can't use sparql below, need to use the store (pointing to Fuseki), sparql is pointing to dbpedia
        fuseki_result = store.query(query_class.return_fuseki_queries)

        print("ading graph to store")

        # for row in fuseki_result.bindings:
        #   print(row)

        return render_template(
            "home/interactive_report.html", option=option, query_result=fuseki_result
        )

    except Exception as e:
        # Handle exceptions or errors here
        print(f"Error: {str(e)}")
        return "An error occurred while querying data.", 500
