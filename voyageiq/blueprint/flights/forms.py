# Form structure for flight 

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional
from wtforms import SelectField , DateField, IntegerField

from wtforms.validators import ValidationError
from datetime import date

class FlightSearchForm(FlaskForm):

    origin = StringField(
              "Origin",
              validators=[DataRequired()]
    )

    destination = StringField(
                   "Destination",
                   validators=[DataRequired()]
    )

    departure_date  = DateField(
                     "Departure Date",
                     format="%Y-%m-%d",
                     validators=[DataRequired()]
    )

    return_date = DateField(
                  "Return Date",
                  format="%Y-%m-%d",
                  validators=[Optional()]
    )

    trip_type = SelectField(
                "Trip Type",
                choices=[
                     ("one_way", "One Way"),
                     ("round_trip", "Round Trip")
                    ],
                    validators=[DataRequired()]
                )

    adults = IntegerField(
                  "Adults",
                  validators=[
                       DataRequired(),
                       NumberRange(min=1)
                  ]
                )

    travel_class = SelectField(
        "Travel Class",
        choices=[
            ("economy", "Economy"),
            ("premium_economy", "Premium Economy"),
            ("business", "Business"),
            ("first", "First")
        ],
        validators=[DataRequired()]
    )

    submit = SubmitField("Search Flights")
     
     # Custom validation 
     # validate<field_name> ye tarika hai validation ke form ke function ko likhne ka 

    def validate_origin(self, field):
            
           # here field = origin  
           # field.data = self.origin.data 
           # and because we are checking destination and origin so we are youring self 

        if(
            self.origin.data
            and self.destination.data
            and self.origin.data.strip().lower()
            == self.destination.data.strip().lower()
        ):
            raise ValidationError(
                 "Origin and destination cannot be the same."
            )
        
    def validate_departure_date(self, field):
         
         # field =  departure
         # field.data = departure.data

        if field.data < date.today():
            raise ValidationError(
                 "Departure date cannot be in the past."
            )

    def validate_return_date(self, field):

        if self.trip_type.data == "round_trip":

            if not field.data:
                raise ValidationError(
                     "Return date is required for round trips."
                ) 

            if(
                self.departure_date.data
                and field.data <= self.departure_date.data
            ):
                raise ValidationError(
                     "Return date must be after departure date."
                )       