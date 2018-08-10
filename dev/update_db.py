from datetime import datetime
import json

from webapp.databases import Hanzi, Vocab, Sentence
from webapp import db

from CJKhyperradicals.sentence import SpoonFed
from CJKhyperradicals.dict import HanziDict, Cedict
from CJKhyperradicals.decompose import Decompose
from CJKhyperradicals.frequency import ChineseFrequency
from HanziLevelUp.hanzi import HanziLevel
from HanziLevelUp.vocab import VocabToSentence

spoon_fed = SpoonFed()
hanzi_level = HanziLevel()
cedict = Cedict()
hanzi_dict = HanziDict()
vocab_to_sentence = VocabToSentence()
decompose = Decompose()
sorter = ChineseFrequency()


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
    for record in Vocab.query:
        vocab = record.vocab
        print(vocab)
        is_user = record.is_user
        record.is_user = not record.is_user

    db.session.commit()
