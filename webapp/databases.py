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
    pinyin = db.Column(db.String(250))
    english = db.Column(db.String(250))
    _levels = db.Column(db.String(250))
    note = db.Column(db.String(10000))
    _tags = db.Column(db.String(250))

    created = db.Column(db.DateTime, default=datetime.now)

    # Moved columns
    modified = db.Column(db.DateTime, default=datetime.now)

    srs_level = db.Column(db.Integer)
    next_review = db.Column(db.DateTime)

    def __init__(self, **kwargs):
        super().__init__(
                    id=int(time()*1000),
                    **kwargs
                )

    @property
    def levels(self):
        return json.loads(self._levels)

    @levels.setter
    def levels(self, value):
        self._levels = json.dumps(value, ensure_ascii=False)

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
        self.sentence = value

        lookup = list(spoon_fed.get_sentence(value))
        if len(lookup) > 0:
            english = lookup[0][1]
            try:
                pinyin = lookup[0][2]
            except IndexError:
                pinyin = ''
        else:
            english = pinyin = ''

        self.pinyin = pinyin
        self.english = english
        self._levels = json.dumps([hanzi_level.get_hanzi_level(char) for char in value
                                   if regex.match(r'\p{IsHan}', char)])
        self.created = self.modified = datetime.now()


class Vocab(db.Model):
    __tablename__ = 'vocab'

    # Old columns
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    vocab = db.Column(db.String(250), nullable=False)

    # New columns
    simplified = db.Column(db.String(250))
    traditional = db.Column(db.String(250))
    pinyin = db.Column(db.String(250))
    english = db.Column(db.String(250))
    sentences = db.Column(db.String(10000))
    level = db.Column(db.Integer)
    note = db.Column(db.String(10000))
    _tags = db.Column(db.String(250))

    is_user = db.Column(db.Boolean)
    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime, default=datetime.now)

    srs_level = db.Column(db.Integer)
    next_review = db.Column(db.DateTime)

    def __init__(self, **kwargs):
        super().__init__(
                    id=int(time()*1000),
                    **kwargs
                )

    # @property
    # def simplified(self):
    #     return json.loads(self._simplified)
    #
    # @simplified.setter
    # def simplified(self, value):
    #     self._simplified = json.dumps(value, ensure_ascii=False)
    #
    # @property
    # def traditional(self):
    #     return json.loads(self._traditional)
    #
    # @traditional.setter
    # def traditional(self, value):
    #     self._traditional = json.dumps(value, ensure_ascii=False)
    #
    # @property
    # def pinyin(self):
    #     return json.loads(self._pinyin)
    #
    # @pinyin.setter
    # def pinyin(self, value):
    #     self._pinyin = json.dumps(value, ensure_ascii=False)
    #
    # @property
    # def english(self):
    #     return json.loads(self._english)
    #
    # @english.setter
    # def english(self, value):
    #     self._english = json.dumps(value, ensure_ascii=False)

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
        self.vocab = value

        dict_result = list(cedict.search_vocab(value))
        self.simplified = json.dumps([item[1] for item in dict_result], ensure_ascii=False)
        self.traditional = json.dumps([item[0] for item in dict_result], ensure_ascii=False)
        self.pinyin = json.dumps([item[2] for item in dict_result], ensure_ascii=False)
        self.english = json.dumps([item[3] for item in dict_result], ensure_ascii=False)
        self.sentences = json.dumps(vocab_to_sentence.convert(value), ensure_ascii=False)
        self.level = max([hanzi_level.get_hanzi_level(hanzi) for hanzi in value])


# New table
class Hanzi(db.Model):
    __tablename__ = 'hanzi'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    hanzi = db.Column(db.String(20), nullable=False)
    pinyin = db.Column(db.String(250))
    english = db.Column(db.String(10000))
    heisig = db.Column(db.String(250))
    compositions = db.Column(db.String(250))
    supercompositions = db.Column(db.String(250))
    variants = db.Column(db.String(250))
    kanji = db.Column(db.String(250))
    vocab = db.Column(db.String(10000))
    sentences = db.Column(db.String(10000))
    level = db.Column(db.Integer)
    note = db.Column(db.String(10000))
    _tags = db.Column(db.String(250))

    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime, default=datetime.now)

    srs_level = db.Column(db.Integer)
    next_review = db.Column(db.DateTime)

    def __init__(self, **kwargs):
        super().__init__(
                    id=int(time()*1000),
                    **kwargs
                )

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
        self.hanzi = value

        dict_entry = hanzi_dict.entries.get(value, dict())
        self.pinyin = dict_entry.get('Pin1Yin1', '')
        self.english = dict_entry.get('Meaning', '')
        self.heisig = dict_entry.get('Heisig', '')
        self.variants = dict_entry.get('Variant', '')
        self.kanji = dict_entry.get('Kanji', '')
        self.level = hanzi_level.get_hanzi_level(value)

        self.compositions = ''.join([x for x in decompose.get_sub(value) if not x.isdigit()])
        self.supercompositions = ''.join(sorter.sort_char(decompose.get_super(value)))
        self.vocab = json.dumps(sorter.sort_vocab([list(item)
                                                   for item in cedict.search_hanzi(value)])[:10],
                                ensure_ascii=False)
        self.sentences = json.dumps(list(vocab_to_sentence.convert(value)),
                                    ensure_ascii=False)


def row2dict(row):
    d = OrderedDict()
    for column in row.__table__.columns:
        d[column.name] = getattr(row, column.name)

    return d
