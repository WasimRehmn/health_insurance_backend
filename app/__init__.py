from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from config import Config

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
mongo = PyMongo(app)

from app import routes
