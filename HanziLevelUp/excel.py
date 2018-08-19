import pyexcel_xlsxwx
import json
from datetime import datetime
from collections import OrderedDict

from webapp.databases import Hanzi, Vocab, Sentence


def export_excel():
    def _dump(table_object):
        headers = table_object.__table__.columns.keys()

        i = headers.index('data')
        headers.pop(i)
        all_keys = set()
        for record in table_object.query:
            if record.data is not None:
                all_keys.update(json.loads(record.data).keys())
        all_keys = list(all_keys)
        headers[i:i] = all_keys

        sheet_data = [headers]
        for record in table_object.query:
            sheet_data.append(_to_minimal_string(record.entry, all_keys))

        return sheet_data

    def _to_minimal_string(v_list, all_keys):
        output = []
        for k, v in v_list.items():
            if k != 'data':
                if isinstance(v, datetime):
                    output.append(v.isoformat())
                else:
                    output.append(v)
            else:
                output2 = [None for _ in all_keys]
                for k2, v2 in json.loads(v).items():
                    if not isinstance(v2, (str, int)):
                        output2[all_keys.index(k2)] = json.dumps(v2, ensure_ascii=False)
                    else:
                        output2[all_keys.index(k2)] = v2
                output.extend(output2)

        return output

    data = OrderedDict()

    data[Hanzi.__tablename__] = _dump(Hanzi)
    data[Vocab.__tablename__] = _dump(Vocab)
    data[Sentence.__tablename__] = _dump(Sentence)

    pyexcel_xlsxwx.save_data(
        'user/HanziLevelUp.xlsx', data,
        config={'format': None}
        # config={'format': {'_default': {'num_format': '0'}}}
    )
