# Form structure maintent 
# In this file we are fixing the structure of forms use in registration and login


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

# Registration form structure 
class RegisterForm(FlaskForm):

    full_name = StringField(
                  "Full Name",
                 validators=[DataRequired(), Length(min=3, max=100)]
                )
    
    user_name = StringField(
                   "User Name",
                  validators=[DataRequired(), Length(min=3, max=20)]
                )
    
    email = StringField(
             "Email Address",
            validators=[DataRequired(), Email()]
             )
    
    phone = StringField(
                       "Phone Number",
                  validators=(DataRequired(), Length(min=10, max=15))
            )
    
    password= PasswordField(
                    "Password",
                    validators=[DataRequired(), Length(min=8, max=128)]
                )
    
    confirm_password = PasswordField(
                        "Confirm Password",
                         validators=[DataRequired(), 
                                    EqualTo("password", 
                                            message="Password must match")
                                            ]
                       )
    
    submit = SubmitField("Create Account")

# Login form structure
class LoginForm(FlaskForm):

    identifier = StringField(
                "Username or Email",
                validators=[DataRequired()]
               )

    password = PasswordField(
                "Password",
                validators=[DataRequired()]
               )
    
    submit = SubmitField("Login")

