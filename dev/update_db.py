from datetime import datetime
import json

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
    for record in Hanzi.query:
        print(record.entry)

        if record.front is None:
            record.front = "%(hanzi)s"
        if record.back is None:
            record.back = '%(data)s'

    for record in Vocab.query:
        print(record.entry)

        if record.front is None or '%(' in record.front:
            data = json.loads(record.data)
            if len(data['dictionary']) > 0:
                record.front = ', '.join([item['english'] for item in data['dictionary']])
            else:
                record.front = '%(vocab)s'

        if record.back is None:
            record.back = '%(data)s'

    for record in Sentence.query:
        print(record.entry)

        if record.front is None:
            record.front = '%(sentence)s'
        if record.back is None:
            record.back = '%(data)s'

    db.session.commit()
