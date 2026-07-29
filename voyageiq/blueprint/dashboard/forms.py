from flask_wtf import FlaskForm
from wtforms import SelectField, StringField,  DateField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length

from datetime import date
from wtforms.validators import ValidationError

class DashboardForm(FlaskForm):

    origin = StringField(
                 "Origin",
                 validators=[DataRequired(),
                            Length(max=100,
                            message="Origin is required")]
            )
    
    destination = StringField(
                  "Destination",
                   validators=[DataRequired(), 
                              Length(max=100,
                                 message="Destination is required")]     
                )
    
    departure_date =DateField(
                       "Departure Date",
                       format="%Y-%m-%d",
                       validators=[DataRequired(message="Departure date is required")
                                   ]
                    )
    
    return_date = DateField(
                    "Return Date",
                    format="%Y-%m-%d",
                    validators=[DataRequired(message=" Return date is required")]
                )
    
    trip_type = SelectField(
                "Trip Type",
                choices=[
                     ("one_way", "One Way"),
                     ("round_trip", "Round Trip")
                    ],
                    validators=[DataRequired(message="Travel trip is required")]
                )
    
    adults = IntegerField(
                "Adults",
                validators=[DataRequired(),
                            NumberRange(min=1,
                            message="At least 1 traveler is required.")]
    )

    travel_class = SelectField(
                     "Travel Class",
                        choices=[
                            ("economy", "Economy"),
                            ("premium_economy", "Premium Economy"),
                            ("business", "Business"),
                            ("first", "First")
                        ],
                        validators=[DataRequired(message="Travel class is required")]
                        
                    ) 

    submit = SubmitField("Analyze Trip")


    def validate_departure_date(self, field):
        if field.data < date.today():
            raise ValidationError(
                 "Departure date cannot be in the past."
            )
    
    def validate_destination(self, field):

        if (
            self.origin.data and
            field.data and
            self.origin.data.strip().lower()
            == field.data.strip().lower()
        ):
            raise ValidationError(
                "Origin and destination cannot be the same."
            )

    def validate_return_date(self, field):
        if self.trip_type.data == "round_trip":

            if not field.data:
                raise ValidationError(
                     "Return date is required for round trips."
                ) 

            if(self.departure_date.data and field.data < self.departure_date.data):
                raise ValidationError(
                     "Return date must be after departure date."
                )     

