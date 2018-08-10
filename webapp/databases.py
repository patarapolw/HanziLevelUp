from time import time
from datetime import datetime
import json
import regex
from collections import OrderedDict

from CJKhyperradicals.sentence import SpoonFed
from CJKhyperradicals.dict import HanziDict, Cedict
from CJKhyperradicals.decompose import Decompose
from CJKhyperradicals.frequency import ChineseFrequency
from HanziLevelUp.hanzi import HanziLevel
from HanziLevelUp.vocab import VocabToSentence

from webapp import db

spoon_fed = SpoonFed()
hanzi_level = HanziLevel()
cedict = Cedict()
hanzi_dict = HanziDict()
vocab_to_sentence = VocabToSentence()
decompose = Decompose()
sorter = ChineseFrequency()


class Sentence(db.Model):
    __tablename__ = 'sentences'

    # Old columns
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    sentence = db.Column(db.String(250), nullable=False)

    # New columns
    data = db.Column(db.String(10000))
    _tags = db.Column(db.String(250))

    created = db.Column(db.DateTime, default=datetime.now)

    # Moved columns
    modified = db.Column(db.DateTime, default=datetime.now)

    @property
    def tags(self):
        return json.loads(self._tags)

    @tags.setter
    def tags(self, value):
        self._tags = json.dumps(value, ensure_ascii=False)

    @property
    def entry(self):
        return row2dict(self)

    @entry.setter
    def entry(self, value):
        self.id = int(time()*1000)
        self.sentence = value

        lookup = list(spoon_fed.get_sentence(value))
        if len(lookup) > 0:
            english = lookup[0]['english']
            try:
                pinyin = lookup[0]['pinyin']
            except IndexError:
                pinyin = ''
        else:
            english = pinyin = ''

        self.data = json.dumps({
            'pinyin': pinyin,
            'english': english,
            'levels': [hanzi_level.get_hanzi_level(char) for char in value if
                       regex.match(r'\p{IsHan}', char)]
        }, ensure_ascii=False)


class Vocab(db.Model):
    __tablename__ = 'vocab'

    # Old columns
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    vocab = db.Column(db.String(250), nullable=False)

    # New columns
    data = db.Column(db.String(10000))
    _tags = db.Column(db.String(250))

    is_user = db.Column(db.Boolean, nullable=False)

    created = db.Column(db.DateTime, default=datetime.now)

    # Moved columns
    modified = db.Column(db.DateTime, default=datetime.now)

    @property
    def tags(self):
        return json.loads(self._tags)

    @tags.setter
    def tags(self, value):
        self._tags = json.dumps(value, ensure_ascii=False)

    @property
    def entry(self):
        return row2dict(self)

    @entry.setter
    def entry(self, value):
        self.id = int(time() * 1000)
        self.vocab = value

        dict_result = list(cedict.search_vocab(value))
        self.data = json.dumps({
            'dictionary': dict_result,
            'sentences': vocab_to_sentence.convert(value),
            'level': max([hanzi_level.get_hanzi_level(hanzi) for hanzi in value])
        }, ensure_ascii=False)


# New table
class Hanzi(db.Model):
    __tablename__ = 'hanzi'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    hanzi = db.Column(db.String(20), nullable=False)
    data = db.Column(db.String(10000))
    _tags = db.Column(db.String(250))

    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime, default=datetime.now)

    @property
    def tags(self):
        return json.loads(self._tags)

    @tags.setter
    def tags(self, value):
        self._tags = json.dumps(value)

    @property
    def entry(self):
        return row2dict(self)

    @entry.setter
    def entry(self, value):
        self.id = int(time() * 1000)
        self.hanzi = value

        self.data = json.dumps({
            'compositions': decompose.get_sub(value),
            'supercompositions': sorter.sort_char(decompose.get_super(value)),
            'vocab': sorter.sort_vocab(list(cedict.search_hanzi(value)))[:10],
            'sentences': list(vocab_to_sentence.convert(value))
        }, ensure_ascii=False)


def row2dict(row):
    d = OrderedDict()
    for column in row.__table__.columns:
        d[column.name] = getattr(row, column.name)

    return d
