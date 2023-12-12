#####
#Author: Sharayu  
#Created a new bleuprint for dbpedia related info. 
######

from flask import Blueprint

blueprint = Blueprint(
    'dbpedia_blueprint',
    __name__,
    url_prefix=''
)
