from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, DecimalField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length, ValidationError

from datetime import datetime

class TargetTripForm(FlaskForm):

    origin = StringField(
              "Origin",
              validators=[DataRequired(),
                        Length(max=200)]
            )
    
    destination = StringField(
                    "Destination",
                    validators=[DataRequired(),
                                Length(max=200)]
                )
    
    travelers = IntegerField(
                  "Travelers",
                  default=1,
                  validators=[DataRequired(),
                               NumberRange(min=1)]
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
    
    start_month = SelectField(
                   "Start Month",
                   coerce=int,
                   choices=[
                        (1, "January"),
                        (2, "February"),
                        (3, "March"),
                        (4, "April"),
                        (5, "May"),
                        (6, "June"),
                        (7, "July"),
                        (8, "August"),
                        (9, "September"),
                        (10, "October"),
                        (11, "November"),
                        (12, "December")
                   ],
                   validators=[DataRequired()]
                )
    
    end_month = SelectField(
                  "End Month",
                    coerce=int,
                    choices=[
                           (1, "January"),
                            (2, "February"),
                            (3, "March"),
                            (4, "April"),
                            (5, "May"),
                            (6, "June"),
                            (7, "July"),
                            (8, "August"),
                            (9, "September"),
                            (10, "October"),
                            (11, "November"),
                            (12, "December")
                        ],
                  validators=[DataRequired()]
                )
    
    travel_year =   IntegerField(
                     "Travel Year",
                     validators=[DataRequired(),
                                NumberRange(min=datetime.now().year, max=2100)]
                    )
    
    flight_min_price =  DecimalField(
                          "Minimum Flight Budget",
                          places=2,
                          validators=[DataRequired(),
                                      NumberRange(min=0)]
                        )
    
    flight_max_price =  DecimalField(
                          "Maximum Flight Budget",
                          places=2,
                          validators=[DataRequired(),
                                      NumberRange(min=0)]
                        )
    
    hotel_min_price = DecimalField(
        "Minimum Hotel Budget",
        places=2,
        validators=[
            DataRequired(),
            NumberRange(min=0)
        ]
    )

    hotel_max_price = DecimalField(
        "Maximum Hotel Budget",
        places=2,
        validators=[
            DataRequired(),
            NumberRange(min=0)
        ]
    )

    submit = SubmitField("Create Target Trip")

    def validate_flight_max_price(self, field):
        if field.data < self.flight_min_price.data:
            raise ValidationError(
                  "Maximum flight price must be greater than or equal to minimum flight price."
            )
        
    def validate_hotel_max_price(self, field):
        if field.data < self.hotel_min_price.data:
            raise ValidationError(
                "Maximum hotel price must be greater than or equal to minimum hotel price."
            ) 

    def validate_end_month(self, field):
        if field.data < self.start_month.data:
            raise ValidationError(
                "End month cannot be earlier than start month."
            )      