from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional, length
from wtforms import SelectField, DateField, IntegerField
from wtforms.validators import ValidationError
from datetime import date

class HotelSearchForm(FlaskForm):
    destination = StringField(
                    "Destination",
                    validators =[DataRequired(
                                message="Destination is required"
                                ),
                                length(max=100,
                               message="Destination must be less than 100 characters")]
                )
    
    check_in_date = DateField(
        "Check-In Date",
        validators=[
            DataRequired(
                message="Check-in date is required."
            )
        ]
    )

    check_out_date = DateField(
        "Check-Out Date",
        validators=[
            DataRequired(
                message="Check-out date is required."
            )
        ]
    )


    adults = IntegerField(
        "Adults",
        default=2,
        validators=[
            DataRequired(),
            NumberRange(
                min=1,
                max=10,
                message="Adults must be between 1 and 10."
            )
        ]
    )

    rooms = IntegerField(
        "Rooms",
        default=2,
        validators=[
            DataRequired(),
            NumberRange(
                min=1,
                max=5,
                message="Rooms must be between 1 and 5."
            )
        ]
    )

    submit = SubmitField("Search Hotels")

    # custom validation
    def validate_destination(self, field):

        field_data = field.data.strip()  # remove the extra space

        if(len(field_data) < 2):
            raise ValidationError("Destination must contain at least 2 characters.")

    def validate_check_in_date(self, field):

        if field.data < date.today():
            raise ValidationError("Check-in date cannot be in the past.")

    def validate_check_out_date(self, field):

        if(
            self.check_in_date.data
            and 
            field.data <= self.check_in_date.data
        ):
            raise ValidationError("Check-out date must be after check-in date.")        
