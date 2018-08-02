import sqlite3
import dateutil.parser

import pyexcel

import json
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import sessionmaker

from CJKhyperradicals.decompose import Decompose
from CJKhyperradicals.dict import Cedict
from CJKhyperradicals.frequency import ChineseFrequency
from CJKhyperradicals.variant import Variant
from CJKhyperradicals.sentence import SpoonFed, jukuu

engine = create_engine('sqlite:///user_new.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)

decompose = Decompose()
variant = Variant()
cedict = Cedict()
sorter = ChineseFrequency()


class OldReader:
    def __init__(self):
        self.conn = sqlite3.connect('../webapp/user.db')

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
    pinyin = Column(String(250))
    english = Column(String(250))
    _levels = Column(String(250))
    note = Column(String(10000))
    _tags = Column(String(250))

    created = Column(DateTime)

    # Moved columns
    modified = Column(DateTime, nullable=False)

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


class Vocab(Base):
    __tablename__ = 'vocab'

    # Old columns
    id = Column(Integer, primary_key=True, nullable=False)
    vocab = Column(String(250), nullable=False)

    # New columns
    simplified = Column(String(250))
    traditional = Column(String(250))
    pinyin = Column(String(250))
    english = Column(String(250))
    sentences = Column(String(10000))
    level = Column(Integer)
    note = Column(String(10000))
    _tags = Column(String(250))

    is_user = Column(Boolean)
    created = Column(DateTime)
    modified = Column(DateTime)

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


# New table
class Hanzi(Base):
    __tablename__ = 'hanzi'

    id = Column(Integer, primary_key=True, nullable=False)
    hanzi = Column(String(20), nullable=False)
    pinyin = Column(String(250))
    english = Column(String(10000))
    heisig = Column(String(250))
    compositions = Column(String(250))
    supercompositions = Column(String(250))
    variants = Column(String(250))
    kanji = Column(String(250))
    vocab = Column(String(10000))
    sentences = Column(String(10000))
    level = Column(Integer)
    note = Column(String(10000))
    _tags = Column(String(250))

    created = Column(DateTime)
    modified = Column(DateTime)

    @property
    def tags(self):
        return json.loads(self._tags)

    @tags.setter
    def tags(self, value):
        self._tags = json.dumps(value)


class VocabToSentence:
    def __init__(self):
        self.spoon_fed = SpoonFed()

    def convert(self, vocab, online=True):
        sentences = list(self.spoon_fed.get_sentence(vocab))[:10]
        if len(sentences) == 0 and online:
            sentences = list(jukuu(vocab))

        return sentences


def create():
    Base.metadata.create_all(engine)
    session = Session()
    vocab_to_sentence = VocabToSentence()

    old_reader = OldReader()

    # New table
    for i, excel_record in enumerate(ExcelReader().get_data('hanzi')):
        record = dict()
        for k, v in excel_record.items():
            record[k.lower()] = v

        print(record['hanzi'])

        record['id'] = i
        record['created'] = record['modified'] = dateutil.parser.parse(excel_record['Created']).replace(tzinfo=None)

        record['compositions'] = ''.join(decompose.get_sub(record['hanzi']))
        record['supercompositions'] = ''.join(sorter.sort_char(decompose.get_super(record['hanzi'])))
        record['vocab'] = json.dumps(sorter.sort_vocab([list(item)
                                                        for item in cedict.search_hanzi(record['hanzi'])])[:10],
                                     ensure_ascii=False)
        record['sentences'] = json.dumps(list(vocab_to_sentence.convert(record['hanzi'])),
                                         ensure_ascii=False)

        session.add(Hanzi(**record))

    # Pre-existing tables
    table_name = 'vocab'
    for i, excel_record in enumerate(ExcelReader().get_data(table_name)):
        record = old_reader.fetch_one(table_name, excel_record['Vocab'])
        if record is None:
            record = dict()
            record['id'] = i
            record['created'] = record['modified'] = dateutil.parser.parse(excel_record.pop('Created'))\
                .replace(tzinfo=None)
        else:
            record['created'] = record['modified'] = dateutil.parser.parse(record['modified'])\
                .replace(tzinfo=None)
            excel_record.pop('Created')

            record['note'] = record.pop('notes')

        for k, v in excel_record.items():
            record[k.lower()] = v

        print(record['vocab'])

        for item_name in ('simplified', 'traditional', 'pinyin', 'english'):
            record[item_name] = json.dumps([x for x in record[item_name].split(', ') if x != ''],
                                           ensure_ascii=False)

        if record.pop('source') == 'user':
            record['is_user'] = False
        else:
            record['is_user'] = True

        record['sentences'] = json.dumps(list(vocab_to_sentence.convert(record['vocab'])), ensure_ascii=False)

        session.add(Vocab(**record))

    table_name = 'sentences'
    for i, excel_record in enumerate(ExcelReader().get_data(table_name)):
        record = old_reader.fetch_one(table_name, excel_record['Sentence'])
        if record is None:
            record = dict()
            record['id'] = i
            record['created'] = record['modified'] = dateutil.parser.parse(excel_record.pop('Created')) \
                .replace(tzinfo=None)
        else:
            record['created'] = record['modified'] = dateutil.parser.parse(record['modified']) \
                .replace(tzinfo=None)
            excel_record.pop('Created')

            record['note'] = record.pop('notes')

        for k, v in excel_record.items():
            record[k.lower()] = v

        print(record['sentence'])

        for item_name in ('levels', ):
            record[item_name] = [int(level) for level in record[item_name].split(', ') if level != '']

        session.add(Sentence(**record))

    session.commit()


def update():
    session = Session()
    old_reader = OldReader()

    table_name = 'hanzi'
    for i, excel_record in enumerate(ExcelReader().get_data(table_name)):
        session.query().filter(Hanzi.hanzi == excel_record['Hanzi'])\
            .update({'compositions':''.join(decompose.get_sub(excel_record['Hanzi']))})

    table_name = 'sentences'
    for i, excel_record in enumerate(ExcelReader().get_data(table_name)):
        record = old_reader.fetch_one(table_name, excel_record['Sentence'])
        if record is None:
            record = dict()
            record['id'] = i
            record['created'] = record['modified'] = dateutil.parser.parse(excel_record.pop('Created')) \
                .replace(tzinfo=None)
        else:
            record['created'] = record['modified'] = dateutil.parser.parse(record['modified']) \
                .replace(tzinfo=None)
            excel_record.pop('Created')

            record['note'] = record.pop('notes')

        for k, v in excel_record.items():
            record[k.lower()] = v

        print(record['sentence'])

        for item_name in ('levels',):
            record[item_name] = [int(level) for level in record[item_name].split(', ') if level != '']

        session.add(Sentence(**record))

    session.commit()


if __name__ == '__main__':
    create()
