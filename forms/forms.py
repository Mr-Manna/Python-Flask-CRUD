from flask_wtf  import  Form
from  wtforms   import  StringField,SubmitField,PasswordField
from wtforms.validators import DataRequired

class SignupForm(Form):
    username = StringField('Username',validators=[DataRequired()])
    name = StringField('Name',validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Signup')


class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class BlogForm(Form):
    title = StringField('Title')
    content = StringField('Content')
    submit = SubmitField('Create')
