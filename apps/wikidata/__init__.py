#####
#Author: Sharayu  
#Created a new bleuprint for Wiki related info. 
######

from flask import Blueprint

blueprint = Blueprint(
    'wikidata_blueprint',
    __name__,
    url_prefix=''
)
