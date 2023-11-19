#####
#Author: Sharayu  
#Created a new bleuprint for reviews related info. 
######


from flask import Blueprint

blueprint = Blueprint(
    'reviews_blueprint',
    __name__,
    url_prefix=''
)
