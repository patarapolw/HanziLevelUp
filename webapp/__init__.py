from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from .blueprints import blueprint
from .config import Config

app = Flask(__name__)
app.register_blueprint(blueprint)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .views import hanzi, learning, levels, sentence, utils, vocab, item, export, quiz
