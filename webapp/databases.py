from time import time
from datetime import datetime, timedelta
import dateutil.parser
import json
import regex
from collections import OrderedDict
import os
from IPython.display import IFrame
import random

from CJKhyperradicals.sentence import SpoonFed, jukuu
from CJKhyperradicals.dict import HanziDict, Cedict
from CJKhyperradicals.decompose import Decompose
from CJKhyperradicals.frequency import ChineseFrequency
from HanziLevelUp.hanzi import HanziLevel
from HanziLevelUp.vocab import VocabToSentence

from webapp import db
from webapp.utils import to_raw_tags, tag_reader, SRS


spoon_fed = SpoonFed()
hanzi_level = HanziLevel()
cedict = Cedict()
hanzi_dict = HanziDict()
vocab_to_sentence = VocabToSentence()
decompose = Decompose()
sorter = ChineseFrequency()


class SrsRecord:
    __tablename__ = NotImplemented
    id = NotImplemented
    tags = NotImplemented
    modified = NotImplemented
    srs_level = NotImplemented
    next_review = NotImplemented
    data = NotImplemented

    @property
    def json(self):
        return json.loads(self.data)

    @json.setter
    def json(self, value):
        self.data = json.dumps(value, ensure_ascii=False)

    def hide(self):
        return IFrame('http://{}:{}/card/{}/{}'.format(os.getenv('HOST', 'localhost'),
                                                       os.getenv('PORT', 8080),
                                                       self.__tablename__,
                                                       self.id),
                      width=800, height=100)

    def show(self):
        return IFrame('http://{}:{}/card/{}/{}/show'.format(os.getenv('HOST', 'localhost'),
                                                            os.getenv('PORT', 8080),
                                                            self.__tablename__,
                                                            self.id),
                      width=800, height=200)

    def next_srs(self):
        if not self.srs_level:
            self.srs_level = 1
        else:
            self.srs_level = self.srs_level + 1

        self.next_review = (datetime.now()
                            + SRS.get(int(self.srs_level), timedelta(weeks=4)))
        self.modified = datetime.now()

    correct = right = next_srs

    def previous_srs(self, duration=timedelta(minutes=1)):
        if self.srs_level and self.srs_level > 1:
            self.srs_level = self.srs_level - 1

        self.bury(duration)

    incorrect = wrong = previous_srs

    def bury(self, duration=timedelta(minutes=1)):
        self.next_review = datetime.now() + duration
        self.modified = datetime.now()

    def mark(self, tag_name='marked'):
        if self.tags is None:
            self.tags = ''

        all_tags = tag_reader(self.tags)
        all_tags.add(tag_name)
        self.tags = to_raw_tags(all_tags)

    def unmark(self, tag_name='marked'):
        if self.tags is None:
            self.tags = ''

        all_tags = tag_reader(self.tags)
        if tag_name in all_tags:
            all_tags.remove(tag_name)
        self.tags = to_raw_tags(all_tags)

    @classmethod
    def iter_quiz(cls, level=5, is_due=True, tag=None):
        def _filter_tag(srs_record):
            if not tag or tag in tag_reader(srs_record.tags):
                yield srs_record

        def _filter():
            for srs_record in cls.query.order_by(cls.modified.desc()):
                record_data = srs_record.data
                if record_data:
                    record_data = json.loads(record_data)
                    if ((not level or record_data['level'] <= level)
                            and getattr(srs_record, 'is_user', True)):
                        if is_due is None:
                            yield from _filter_tag(srs_record)
                        elif is_due is True:
                            if not srs_record.next_review or srs_record.next_review < datetime.now():
                                yield from _filter_tag(srs_record)
                        else:
                            if srs_record.next_review is None:
                                yield from _filter_tag(srs_record)
                else:
                    yield srs_record

        all_records = list(_filter())
        random.shuffle(all_records)

        return iter(all_records)

    def _get_more_sentences(self, vocab_or_hanzi):
        data_dict = self.json
        if 'sentences' in data_dict.keys() \
                and not any([sentence['english'].startswith('1. ') for sentence in data_dict['sentences']]):
            data_dict['sentences'].extend(list(jukuu(vocab_or_hanzi)))
            self.json = data_dict

            db.session.commit()


class Sentence(db.Model, SrsRecord):
    __tablename__ = 'sentences'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    sentence = db.Column(db.String(250), nullable=False)

    data = db.Column(db.String(10000))
    tags = db.Column(db.String(250))

    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime, default=datetime.now)

    front = db.Column(db.String(250))
    back = db.Column(db.String(250))
    srs_level = db.Column(db.Integer)
    next_review = db.Column(db.DateTime)

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


class Vocab(db.Model, SrsRecord):
    __tablename__ = 'vocab'

    # Old columns
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    vocab = db.Column(db.String(250), nullable=False)

    # New columns
    data = db.Column(db.String(10000))
    tags = db.Column(db.String(250))

    is_user = db.Column(db.Boolean, nullable=False)

    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime, default=datetime.now)

    front = db.Column(db.String(250))
    back = db.Column(db.String(250))
    srs_level = db.Column(db.Integer)
    next_review = db.Column(db.DateTime)

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

    def get_more_sentences(self):
        self._get_more_sentences(self.vocab)


class Hanzi(db.Model, SrsRecord):
    __tablename__ = 'hanzi'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    hanzi = db.Column(db.String(20), nullable=False)
    data = db.Column(db.String(10000))
    tags = db.Column(db.String(250))

    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime, default=datetime.now)

    front = db.Column(db.String(250))
    back = db.Column(db.String(250))
    srs_level = db.Column(db.Integer)
    next_review = db.Column(db.DateTime)

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
            'sentences': list(vocab_to_sentence.convert(value)),
            'level': hanzi_level.get_hanzi_level(value)
        }, ensure_ascii=False)

    def get_more_sentences(self):
        self._get_more_sentences(self.hanzi)


def row2dict(row):
    d = OrderedDict()
    for column in row.__table__.columns:
        d[column.name] = getattr(row, column.name)

    return d


class SrsTuple:
    __slots__ = ('front', 'back', 'tags', 'srs_level', 'next_review')

    def __init__(self, *args):
        for i, arg in enumerate(args):
            setattr(self, self.__slots__[i], arg)

    def to_db(self):
        entry = dict()
        for key in self.__slots__:
            entry[key] = getattr(self, key, None)

        if entry['next_review'] is not None:
            entry['next_review'] = dateutil.parser.parse(entry['next_review'])

        return entry

    @staticmethod
    def from_db(srs_record):
        result = srs_record.entry

        for k, v in result.items():
            if isinstance(v, datetime):
                result[k] = v.isoformat()

        return result
