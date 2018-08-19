from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .blueprints import blueprint
from .config import Config

app = Flask(__name__)
app.register_blueprint(blueprint)
app.config.from_object(Config)

db = SQLAlchemy(app)

from .views import (hanzi, vocab, sentence,
                    learning, levels, utils, item, export, editor)
