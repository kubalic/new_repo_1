from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tajny_klucz'

from app import routes


