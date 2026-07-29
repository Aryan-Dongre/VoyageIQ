from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

class ContactForm(FlaskForm):

    full_name = StringField(
                 "Full Name",
                 validators=[DataRequired(),
                             Length(max=100)
                            ]
                )
    
    email = EmailField(
             "Email",
             validators=[DataRequired(), Email()]
            )
    
    category = SelectField(
                    "Category",
                    choices=[
                         ("flight", "Flight Search Issue"),
                         ("hotel", "Hotel Search Issue"),
                         ("weather", "Weather Search Issue"),
                         ("feature", "Feature Request"),
                         ("feedback", "Feedback"),
                         ("general", "General Inquiry")
                        ],
                        validators=[DataRequired()]
                )
    
    message  = TextAreaField(
                 "Message",
                 validators=[DataRequired(),
                            Length(min=5, max=1000)]
                )
    
    submit = SubmitField("Send message")