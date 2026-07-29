from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Email, DataRequired, Length, Optional, URL

class ProfileForm(FlaskForm):

    full_name = StringField(
                  "Full Name",
                  validators=[DataRequired(), Length(max=100)]
                 )
    
    email = StringField(
        "Email Address",
        validators=[
            DataRequired(),
            Email(),
            Length(max=255)
        ]
    )

    phone = StringField(
            "Phone Number",
            validators=[DataRequired(), Length(max=15)]
    )

    country = StringField(
        "Country",
        validators=[
            Optional(),
            Length(max=100)
        ]
    )
    

    profile_picture = StringField(
        "Profile Picture URL",
        validators=[
            Optional(),
            URL(),
            Length(max=1000)
        ]
    )

    Submit = SubmitField(
                 "Update Profile"
             )

