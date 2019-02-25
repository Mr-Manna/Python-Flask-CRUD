
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:psotgres@localhost/flask'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/flask.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask.db'
db = SQLAlchemy(app)