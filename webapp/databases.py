from time import time
from datetime import datetime

from webapp import db


# class User(db.Model):
#     __tablename__ = 'user'
#     id = db.Column(db.Integer, primary_key=True, nullable=False)
#     username = db.Column(db.String(20), nullable=False)
#     modified = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     notes = db.Column(db.String(250))
#     current_hanzi = db.Column(db.Integer, nullable=False, default=1)
#     current_vocab_hsk = db.Column(db.Integer, nullable=False, default=1)
#     current_sentence = db.Column(db.Integer, nullable=False, default=0)
#
#     def __init__(self, **kwargs):
#         super().__init__(
#             id=int(time()*1000),
#             **kwargs
#         )


class Sentence(db.Model):
    __tablename__ = 'sentences'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    sentence = db.Column(db.String(250), nullable=False)
    modified = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    notes = db.Column(db.String(250))

    def __init__(self, **kwargs):
        super().__init__(
            id=int(time()*1000),
            **kwargs
        )


class Vocab(db.Model):
    __tablename__ = 'vocab'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    vocab = db.Column(db.String(20), nullable=False)
    modified = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    notes = db.Column(db.String(250))

    def __init__(self, **kwargs):
        super().__init__(
            id=int(time()*1000),
            **kwargs
        )
