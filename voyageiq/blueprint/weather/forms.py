from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired,  length
from wtforms.validators import ValidationError

class WeatherSearchForm(FlaskForm):

    destination = StringField(
                     "Destination",
                     validators=[DataRequired(
                          message= "Please enter a destination"
                     ),
                      length(
                          min= 2,
                          max = 100
                      )
                      ], 
                      render_kw={"Placegholder": "Enter city name"}
                    )
    
    submit = SubmitField(
                   "Check Weather"
    )