from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, StringField
from wtforms.validators import DataRequired

# login and registration


class Date(FlaskForm):
    start_date = DateField('Start Date',  # This is displayed on the page
                           format='%Y-%m-%d',
                           id='start_date',
                           validators=[DataRequired()])
    end_date = DateField('End Date',
                         format='%Y-%m-%d',
                         id='end_date',
                         validators=[DataRequired()])
    type = SelectField('Type', choices=[
        ('gold', 'gold'),
        ('platinum', 'platinum'),
        ('silver', 'silver')
    ])
    artists = SelectField('Artists', choices=[
        ('solo', 'solo'),
        ('group', 'group'),
        ('both','both')
    ])
    artist_search_string = StringField('Please enter an artist name to search')


    # VC - to implement eventually in routes.py, we can state that
    # dateForm.artist_searchResults.choices =
    # [#The returned contents from our artist_sales.query_dbpedia_matching_artists formatted to strings#]
    artist_searchResults = SelectField('Possible Matching Artists', choices=[])