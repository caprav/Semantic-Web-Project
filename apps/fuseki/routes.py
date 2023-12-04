from flask import render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user
)

from apps import db, login_manager
from apps.fuseki import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm
from apps.authentication.models import Users

from apps.authentication.util import verify_pass
from apps.fuseki.querydb import create_connection, select_all_users, extract_query
from flask import jsonify 
from apps.fuseki.fusekilogic import fueski_query_execution
import json


@blueprint.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    user_input = data.get('user_input')

    conn = create_connection()
    suggestions = select_all_users(conn, user_input)

    # Check if suggestions is not empty before appending to the list
    suggestions_list = []

    for suggestion in suggestions:
        # Assuming 'suggestion' is a dictionary representing an object
        suggestions_list.append(suggestion)

    # Return the suggestions list as a JSON response
    return jsonify(suggestions_list)

@blueprint.route('/fueski_endpoint', methods=['POST'])
def execute():
    data = request.get_json()
     
    data = str(data['suggestion'])

    if data.startswith('[') and data.endswith(']'):
        output_string = data[2:-2]
    else:
        output_string = data
 
    conn = create_connection()
    query = extract_query(conn, output_string)

    print(query)


    fuseki_result=fueski_query_execution((query))
 

    print(fuseki_result)
 

   

    # Return the result as a JSON response
    return jsonify(fuseki_result)