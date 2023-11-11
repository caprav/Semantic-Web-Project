from flask_wtf import FlaskForm
from wtforms import DateField
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
