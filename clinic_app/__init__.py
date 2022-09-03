from flask import Flask

from config import DevelopementConfig
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder="templates",  static_folder="static")
app.config.from_object(DevelopementConfig)
db = SQLAlchemy(app)
