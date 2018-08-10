import sqlite3
import dateutil.parser
from datetime import datetime
import regex

import pyexcel

import json
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import sessionmaker

from CJKhyperradicals.sentence import SpoonFed
from CJKhyperradicals.dict import HanziDict, Cedict
from CJKhyperradicals.decompose import Decompose
from CJKhyperradicals.frequency import ChineseFrequency
from HanziLevelUp.hanzi import HanziLevel
from HanziLevelUp.vocab import VocabToSentence

engine = create_engine('sqlite:///user.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)

spoon_fed = SpoonFed()
hanzi_level = HanziLevel()
cedict = Cedict()
hanzi_dict = HanziDict()
vocab_to_sentence = VocabToSentence()
decompose = Decompose()
sorter = ChineseFrequency()


class OldReader:
    def __init__(self):
        self.conn = sqlite3.connect('../webapp/_user.db')

    def load(self, table_name):
        cursor = self.conn.execute('SELECT * FROM {}'.format(table_name))
        header = [description[0] for description in cursor.description]
        for row in cursor:
            yield dict(zip(header, row))

    def fetch_one(self, table_name, item):
        if table_name == 'sentences':
            item_name = 'sentence'
        else:
            item_name = table_name

        cursor = self.conn.execute('SELECT * FROM {} WHERE {}=?'.format(table_name, item_name), (item, ))
        row = cursor.fetchone()

        if row is None:
            return None
        else:
            header = [description[0] for description in cursor.description]
            return dict(zip(header, row))

    def get_earliest_modified(self, hanzi):
        def _get_modified(table_name):
            if table_name == 'sentences':
                item_name = 'sentence'
            else:
                item_name = table_name

            cursor = self.conn.execute('SELECT * FROM {} WHERE {} LIKE ?'.format(table_name, item_name),
                                       ('%{}%'.format(hanzi),))
            row = cursor.fetchone()

            if row is None:
                return None
            else:
                return row[0]

        sentence_modified = _get_modified('sentences')
        vocab_modified = _get_modified('vocab')

        if sentence_modified is None:
            if vocab_modified is None:
                return datetime.now()
        elif vocab_modified is None:
            return sentence_modified
        elif sentence_modified < vocab_modified:
            return sentence_modified
        else:
            return vocab_modified


class ExcelReader:
    filename = '../user/HanziLevelUp.xlsx'

    def max_width(self, sheet_name):
        data = dict()
        for record in pyexcel.iget_records(file_name=self.filename, sheet_name=sheet_name):
            for k, v in record.items():
                data.setdefault(k, []).append(len(str(v)))

        pyexcel.free_resources()

        for k, v in data.items():
            data[k] = max(v)

        return data

    def get_data(self, sheet_name):
        yield from pyexcel.iget_records(file_name=self.filename, sheet_name=sheet_name)
        pyexcel.free_resources()


class Sentence(Base):
    __tablename__ = 'sentences'

    # Old columns
    id = Column(Integer, primary_key=True, nullable=False)
    sentence = Column(String(250), nullable=False)

    # New columns
    data = Column(String(10000))
    _tags = Column(String(250))

    created = Column(DateTime, nullable=False)

    # Moved columns
    modified = Column(DateTime, nullable=False)

    @property
    def tags(self):
        return json.loads(self._tags)

    @tags.setter
    def tags(self, value):
        self._tags = json.dumps(value, ensure_ascii=False)


class Vocab(Base):
    __tablename__ = 'vocab'

    # Old columns
    id = Column(Integer, primary_key=True, nullable=False)
    vocab = Column(String(250), nullable=False)

    # New columns
    data = Column(String(10000))
    _tags = Column(String(250))

    is_user = Column(Boolean)

    created = Column(DateTime, nullable=False)

    # Moved columns
    modified = Column(DateTime)

    @property
    def tags(self):
        return json.loads(self._tags)

    @tags.setter
    def tags(self, value):
        self._tags = json.dumps(value, ensure_ascii=False)


# New table
class Hanzi(Base):
    __tablename__ = 'hanzi'

    id = Column(Integer, primary_key=True, nullable=False)
    hanzi = Column(String(20), nullable=False)
    data = Column(String(10000))
    _tags = Column(String(250))

    created = Column(DateTime, nullable=False)
    modified = Column(DateTime)

    @property
    def tags(self):
        return json.loads(self._tags)

    @tags.setter
    def tags(self, value):
        self._tags = json.dumps(value)


def create():
    # Base.metadata.create_all(engine)
    session = Session()

    old_reader = OldReader()

    # New table
    for i, excel_record in enumerate(ExcelReader().get_data('hanzi')):
        record = dict()
        for k, v in excel_record.items():
            record[k.lower()] = v

        print(record['hanzi'])

        record['id'] = i
        record['created'] = record['modified'] = dateutil.parser.parse(excel_record.pop('created')) \
            .replace(tzinfo=None)
        # record['created'] = record['modified'] = old_reader.get_earliest_modified(record['hanzi'])

        record['data'] = json.dumps({
            'compositions': decompose.get_sub(record['hanzi']),
            'supercompositions': sorter.sort_char(decompose.get_super(record['hanzi'])),
            'vocab': sorter.sort_vocab(list(cedict.search_hanzi(record['hanzi'])))[:10],
            'sentences': list(vocab_to_sentence.convert(record['hanzi']))
        }, ensure_ascii=False)
        print(len(record['data']))

        session.add(Hanzi(**dict([(k, v) for k, v in record.items() if k in Hanzi.__table__.columns.keys()])))

    session.commit()

    # Pre-existing tables
    table_name = 'vocab'
    for i, excel_record in enumerate(ExcelReader().get_data(table_name)):
        # if session.query(Vocab).filter_by(vocab=excel_record['vocab']).one_or_none() is not None:
        #     continue

        record = old_reader.fetch_one(table_name, excel_record['vocab'])
        if record is None:
            record = dict()
            record['id'] = i
            record['created'] = record['modified'] = dateutil.parser.parse(excel_record.pop('created'))\
                .replace(tzinfo=None)
        else:
            record['created'] = record['modified'] = dateutil.parser.parse(record['modified'])\
                .replace(tzinfo=None)

            record['note'] = record.pop('notes')

        for k, v in excel_record.items():
            if k not in ('created', 'modified'):
                record[k.lower()] = v

        print(record['vocab'])

        dict_result = list(cedict.search_vocab(record['vocab']))
        record['data'] = json.dumps({
            'dictionary': dict_result,
            'sentences': vocab_to_sentence.convert(record['vocab']),
            'level': max([hanzi_level.get_hanzi_level(hanzi) for hanzi in record['vocab']])
        }, ensure_ascii=False)
        print(len(record['data']))

        session.add(Vocab(**dict([(k, v) for k, v in record.items() if k in Vocab.__table__.columns.keys()])))

        session.commit()

    table_name = 'sentences'
    for i, excel_record in enumerate(ExcelReader().get_data(table_name)):
        record = dict()
        for k, v in excel_record.items():
            record[k.lower()] = v

        print(record['sentence'])

        record = old_reader.fetch_one(table_name, excel_record['sentence'])
        if record is None:
            record['id'] = i
            record['created'] = record['modified'] = dateutil.parser.parse(excel_record.pop('created')) \
                .replace(tzinfo=None)
        else:
            record['created'] = record['modified'] = dateutil.parser.parse(record['modified']) \
                .replace(tzinfo=None)

            record['note'] = record.pop('notes')

        lookup = list(spoon_fed.get_sentence(record['sentence']))
        if len(lookup) > 0:
            english = lookup[0]['english']
            try:
                pinyin = lookup[0]['pinyin']
            except IndexError:
                pinyin = ''
        else:
            english = pinyin = ''

        record['data'] = json.dumps({
            'pinyin': pinyin,
            'english': english,
            'levels': [hanzi_level.get_hanzi_level(char) for char in record['sentence'] if regex.match(r'\p{IsHan}', char)]
        }, ensure_ascii=False)
        print(len(record['data']))

        session.add(Sentence(**dict([(k, v) for k, v in record.items() if k in Sentence.__table__.columns.keys()])))

    session.commit()


def update():
    session = Session()
    old_reader = OldReader()

    table_name = 'hanzi'
    for i, excel_record in enumerate(ExcelReader().get_data(table_name)):
        print(excel_record['Hanzi'])
        mod = old_reader.get_earliest_modified(excel_record['Hanzi'])
        session.query().filter(Hanzi.hanzi == excel_record['Hanzi'])\
            .update({'created': mod, 'modified': mod})

    session.commit()


if __name__ == '__main__':
    create()
