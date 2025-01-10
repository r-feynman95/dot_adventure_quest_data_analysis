from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expensesDB.db'
app.config['SECRET_KEY'] = 'fikj2093wfujsidjfij34kldfaskjl;[-102ikjdsklf]' #ideally you generate a token hex

db = SQLAlchemy(app)

from application import routes