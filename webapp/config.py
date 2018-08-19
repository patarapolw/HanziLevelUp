import os
basedir = os.path.abspath(os.path.dirname(__file__))


def database_url(database_filename='user.db'):
    return os.path.join(basedir, database_filename)


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
