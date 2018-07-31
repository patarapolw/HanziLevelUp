import sqlite3
import dateutil.parser

import pyexcel

import json
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///user_new.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)


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
    levels = Column(String(250))
    note = Column(String(10000))
    tags = Column(String(250))

    created = Column(DateTime)

    # Supposed columns -- Planning to store JSON string
    # _levels = Column(String(250))
    # _tags = Column(String(250))

    # Moved columns
    modified = Column(DateTime, nullable=False)


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
    tags = Column(String(250))

    is_user = Column(Boolean)
    created = Column(DateTime)

    # Supposed columns -- Planning to store JSON string
    # _simplified = Column(String(250))
    # _traditional = Column(String(250))
    # _pinyin = Column(String(250))
    # _english = Column(String(250))
    # _sentences = Column(String(10000))
    # _tags = Column(String(250))

    # Moved columns
    modified = Column(DateTime)


# New table
class Hanzi(Base):
    __tablename__ = 'hanzi'

    id = Column(Integer, primary_key=True, nullable=False)
    hanzi = Column(String(20), nullable=False)
    pinyin = Column(String(250))
    english = Column(String(10000))
    heisig = Column(String(250))
    variants = Column(String(250))
    kanji = Column(String(250))
    level = Column(Integer)
    note = Column(String(10000))
    tags = Column(String(250))

    created = Column(DateTime)
    modified = Column(DateTime)

    # Supposed columns -- Planning to store JSON string
    # _tags = Column(String(250))

    # @property
    # def tags(self):
    #     return json.loads(self._tags)
    #
    # @tags.setter
    # def tags(self, value):
    #     self._tags += json.dumps(value)


def main():
    Base.metadata.create_all(engine)
    session = Session()

    old_reader = OldReader()

    # New table
    for i, excel_record in enumerate(ExcelReader().get_data('hanzi')):
        record = dict()
        for k, v in excel_record.items():
            record[k.lower()] = v

        record['id'] = i
        record['created'] = record['modified'] = dateutil.parser.parse(excel_record['Created']).replace(tzinfo=None)
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

        for item_name in ('simplified', 'traditional', 'pinyin', 'english', 'sentences'):
            record[item_name] = json.dumps(record[item_name].split(', '))

        if record.pop('source') == 'user':
            record['is_user'] = False
        else:
            record['is_user'] = True

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

        for item_name in ('levels', ):
            record[item_name] = json.dumps(record[item_name].split(', '))

        session.add(Sentence(**record))

    session.commit()


if __name__ == '__main__':
    main()
