"""
Author: Sharayu
Created a new route file to handle history logic 

"""

from apps.history import blueprint
from flask import render_template, request, session, redirect, url_for
from flask_login import login_required,current_user
from jinja2 import TemplateNotFound
from apps.history import insert_history
import datetime
import re
from apps.history  import query_history
import os





@blueprint.route('/history')
@login_required
def history():
     
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    database = os.path.join(basedir, 'db.sqlite3')
    conn = query_history.create_connection(database)

    user_name= current_user.username

    if conn is not None:
        history_data = query_history.show_user_history(conn,user_name)
        # Close the connection after querying
        conn.close()
    else:
        history_data = []

    print(history_data)    

    keys = ["username", "start_date", "end_date", "type", "artist_name", "query_date",
            "parameter_1", "parameter_2", "parameter_3", "parameter_4"]
    history_dicts = [dict(zip(keys, row)) for row in history_data]    


    
    return render_template('home/history.html', history=history_dicts) 