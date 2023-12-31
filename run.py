# sk-Import necessary libraries and modules
import os
from flask_migrate import Migrate
from flask_minify import Minify
from sys import exit
from rdflib import Graph, Namespace, Literal
from rdflib.graph import DATASET_DEFAULT_GRAPH_ID as default
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore
from SPARQLWrapper import SPARQLWrapper, JSON, N3
from pprint import pprint
from flask import Flask, render_template, request
from apps.config import config_dict
from apps import create_app, db
import jsonify
from apps.preprocess import db_dict


# WARNING: Don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False") == "True"

# The configuration
get_config_mode = "Debug" if DEBUG else "Production"

try:
    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit("Error: Invalid <config_mode>. Expected values [Debug, Production] ")

app = create_app(app_config)
Migrate(app, db)
ReviewStatus = db_dict["ReviewStatus"]
ArtistStatus = db_dict["ArtistStatus"]
HistoryStatus =  db_dict["HistoryStatus"]

if not DEBUG:
    Minify(app=app, html=True, js=False, cssless=False)


if DEBUG:
    app.logger.info("DEBUG            = " + str(DEBUG))
    app.logger.info("Page Compression = " + "FALSE" if DEBUG else "TRUE")
    app.logger.info("DBMS             = " + app_config.SQLALCHEMY_DATABASE_URI)
    app.logger.info("ASSETS_ROOT      = " + app_config.ASSETS_ROOT)
    app.logger.info("Reviews Table Status      = " + ReviewStatus)
    app.logger.info("Artist Table Status      = " + ArtistStatus)
    app.logger.info("History Table Status      = " + HistoryStatus)



if __name__ == "__main__":
    # Change the port to the desired value (e.g., 8080)
    app.run(debug=True)
