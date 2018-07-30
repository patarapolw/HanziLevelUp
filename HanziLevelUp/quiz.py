import pyexcel
from pathlib import Path
import dateutil.parser
from dateutil.tz import tzstr, tzlocal

import whoosh.fields
import whoosh.index
import whoosh.writing
from whoosh.qparser import MultifieldParser

RAW_DATA_PATH = str(Path('user/HanziLevelUp.xlsx'))

searchers = dict()


def create_search_engine(data_type: str):
    writer = None

    for record in pyexcel.iget_records(file_name=RAW_DATA_PATH, sheet_name=data_type):
        if writer is None:
            schema = whoosh.fields.Schema(**dict.fromkeys(record.keys(), whoosh.fields.TEXT(stored=True)))
            searchers[data_type] = whoosh.index.create_in("whoosh_index", schema)
            writer = searchers[data_type].writer()

        writer.add_document(**dict([(k, str(v)) for k, v in record.items()]))

    writer.commit(mergetype=whoosh.writing.CLEAR)
    pyexcel.free_resources()


def search(data_type: str, search_query: str, level, created: str):
    def level_matches():
        if 'Level' in record.keys():
            if record['Level'] and level:
                return int(record['Level']) < int(level)
            else:
                return True
        elif 'Levels' in record.keys():
            if record['Levels'] and level:
                return max([int(record_level) for record_level in record['Levels'].split(', ')]) < int(level)
            else:
                return True
        else:
            raise KeyError('Either "Level" or "Levels" must match the header.')

    def created_matches():
        if created and record['Created']:
            query_dt = dateutil.parser.parse(created).replace(tzinfo=tzlocal())
            database_dt = dateutil.parser.parse(record['Created'])
            if database_dt.tzinfo is None or database_dt.tzinfo.utcoffset(database_dt) is None:
                database_dt = database_dt.replace(tzinfo=tzstr('Asia/Bangkok'))

            return query_dt < database_dt
        else:
            return True

    ix = searchers[data_type]
    with ix.searcher() as searcher:
        search_query += ' *'
        query = MultifieldParser(set(ix.schema.names()) - {'Level', 'Created'}, ix.schema).parse(search_query)
        for hit in searcher.search(query, limit=500):
            record = hit.fields()
            if level_matches() and created_matches():
                yield record
