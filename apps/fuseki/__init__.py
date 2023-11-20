#####
#Author: Sharayu  
#Created a new bleuprint for Fuseki related info. 
######

from flask import Blueprint

blueprint = Blueprint(
    'fuseki_blueprint',
    __name__,
    url_prefix=''
)
