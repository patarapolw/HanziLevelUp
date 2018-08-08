from datetime import datetime

from webapp.databases import Hanzi, Vocab, Sentence
from webapp import db


def get_earliest_modified(hanzi):
    sentence = Sentence.query.filter(Sentence.sentence.like('%{}%'.format(hanzi))).first()
    vocab = Vocab.query.filter(Vocab.vocab.like('%{}%'.format(hanzi))).first()

    if sentence is None:
        if vocab is None:
            return datetime.now()
        else:
            return vocab.modified
    elif vocab is None:
        return sentence.modified
    elif sentence.modified < vocab.modified:
        return sentence.modified
    else:
        return vocab.modified


if __name__ == '__main__':
    for hanzi in Hanzi.query:
        hanzi.modified = get_earliest_modified(hanzi.hanzi)
        hanzi.created = get_earliest_modified(hanzi.hanzi)

    db.session.commit()
