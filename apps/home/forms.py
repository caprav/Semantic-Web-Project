###############
    # Ramya Sree S  11/11/23
    # Code to Capture form elements type, start date, end date, artist name
################

from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, StringField
from wtforms.validators import DataRequired

# This class holds the definitions of elements on the interactive_report page 
class Hitsongsparams(FlaskForm):
    start_date = DateField('Start Date',  
                           format='%Y-%m-%d',
                           id='start_date',
                           validators=[DataRequired()])
    end_date = DateField('End Date',
                         format='%Y-%m-%d',
                         id='end_date',
                         validators=[DataRequired()])
    type = SelectField('Type', choices=[
        ('"Gold"@en', 'Gold'),
        ('"Platinum"@en', 'Platinum'),
        ('"Silver"@en', 'Silver')
    ])
    artists = SelectField('Artists', choices=[
        ('solo', 'Solo'),
        ('group', 'Group'),
        ('both','Both')
    ])