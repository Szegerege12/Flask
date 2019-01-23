from flask_wtf import FlaskForm  # import modułu do tworzenia logowania
from wtforms import StringField, PasswordField, BooleanField, SubmitField  # import pól
from wtforms.validators import DataRequired  # validator - czyli coś co w tym przypadku sprawdzi czy pole nie jest puste

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')




