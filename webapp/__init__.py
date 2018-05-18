from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from webapp.blueprints import blueprint

app = Flask(__name__)
app.register_blueprint(blueprint)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
db = SQLAlchemy(app)

from webapp import views, views_hanzi, views_vocab, views_sentence
