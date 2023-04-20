from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField

from wtforms.validators import  InputRequired, Length

class RegistrationForm(FlaskForm):
    """Form for adding new users."""

    username = StringField("Username", 
                       validators=[InputRequired(), Length(min =0, max=20, message="Username cannot be longer than 20 characters.")])
    password = PasswordField("Password",  
                          validators=[InputRequired(), Length(min=8, message="Password must be at least 8 characters.")])
    email = StringField("Email", 
                            validators=[InputRequired()])
    first_name = StringField("First Name", 
                       validators=[InputRequired(), Length(max=30)])
    last_name = StringField("Last Name", 
                       validators=[InputRequired(), Length(max=30)])
    
class LoginForm(FlaskForm):
    """Form for users to sign in."""
    username = StringField("Username", 
                       validators=[InputRequired(), Length(min =0, max=20, message="Username cannot be longer than 20 characters.")])
    password = PasswordField("Password",  
                          validators=[InputRequired(), Length(min=8, message="Password must be at least 8 characters.")])
    
class FeedbackForm(FlaskForm):
    """Form for users to submit feedback"""
    title = StringField("Title", 
                        validators = [InputRequired(), Length(max=100)])
    content = TextAreaField("Content")



    

