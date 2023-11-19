"""
Author: Sharayu
Created a new route file to handle reviews logic 

"""

from apps.reviews import blueprint
from flask import render_template, request, session, redirect, url_for
from flask_login import login_required,current_user
from jinja2 import TemplateNotFound
import datetime
import re
from apps.reviews  import view_reviews
import os





@blueprint.route('/reviews')
@login_required
def reviews():
     
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    database = os.path.join(basedir, 'db.sqlite3')
    conn = view_reviews.create_connection(database)

    user_name= current_user.username

    if conn is not None:
        review_data = view_reviews.select_all_reviews(conn)
        # Close the connection after querying
        conn.close()
    else:
        review_data = []

 

    keys = ["username", "category", "description",  "url", "details", "buffer", "date"]
    review_dicts = [dict(zip(keys, row)) for row in review_data]    


    
    return render_template('home/reviews.html', reviews=review_dicts) 