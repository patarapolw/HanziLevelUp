import os
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import sessionmaker

from webapp import db
from webapp.databases import Hanzi, Vocab, Sentence

engine = create_engine('sqlite:///' + os.path.abspath('../webapp/_user.db'))
Base = declarative_base()
Session = sessionmaker(bind=engine)


class _Sentence(Base):
    __tablename__ = 'sentences'

    id = Column(Integer, primary_key=True, nullable=False)
    sentence = Column(String(250), nullable=False)

    data = Column(String(10000))
    _tags = Column(String(250))

    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now)


class _Vocab(Base):
    __tablename__ = 'vocab'

    id = Column(Integer, primary_key=True, nullable=False)
    vocab = Column(String(250), nullable=False)

    data = Column(String(10000))
    _tags = Column(String(250))

    is_user = Column(Boolean, nullable=False)

    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now)


class _Hanzi(Base):
    __tablename__ = 'hanzi'

    id = Column(Integer, primary_key=True, nullable=False)
    hanzi = Column(String(20), nullable=False)
    data = Column(String(10000))
    _tags = Column(String(250))

    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now)


def create():
    session = Session()
    db.create_all()

    for _sentence in session.query(_Sentence):
        sentence = Sentence()
        sentence.id = _sentence.id
        sentence.sentence = _sentence.sentence
        sentence.data = _sentence.data
        sentence.created = _sentence.created
        sentence.modified = _sentence.modified
        db.session.add(sentence)

    db.session.commit()

    for _vocab in session.query(_Vocab):
        vocab = Vocab()
        vocab.id = _vocab.id
        vocab.vocab = _vocab.vocab
        vocab.data = _vocab.data
        vocab.created = _vocab.created
        vocab.modified = _vocab.modified
        vocab.is_user = _vocab.is_user
        db.session.add(vocab)

    db.session.commit()

    for _hanzi in session.query(_Hanzi):
        hanzi = Hanzi()
        hanzi.id = _hanzi.id
        hanzi.hanzi = _hanzi.hanzi
        hanzi.data = _hanzi.data
        hanzi.created = _hanzi.created
        hanzi.modified = _hanzi.modified
        db.session.add(hanzi)

    db.session.commit()


if __name__ == '__main__':
    create()
