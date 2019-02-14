from flask_wtf  import  Form
from  wtforms   import  StringField,SubmitField,PasswordField
from wtforms.validators import DataRequired

class SignupForm(Form):
    username = StringField('Username',validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Signup')