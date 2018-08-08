from flask import send_from_directory, Response

from collections import OrderedDict
from datetime import datetime
import pyexcel_xlsxwx

from webapp import app
from webapp.databases import Hanzi, Vocab, Sentence


@app.route('/post/export/<export_type>', methods=['POST'])
def do_export(export_type):
    def _to_minimal_string(v_list):
        output = []
        for v in v_list:
            if isinstance(v, datetime):
                output.append(str(v))
            else:
                output.append(v)

        return output

    if export_type == 'excel':
        data = OrderedDict()

        data['hanzi'] = [Hanzi.__table__.columns.keys()]
        for hanzi in Hanzi.query:
            data['hanzi'].append(_to_minimal_string(hanzi.entry.values()))

        data['vocab'] = [Vocab.__table__.columns.keys()]
        for vocab in Vocab.query:
            data['vocab'].append(_to_minimal_string(vocab.entry.values()))

        data['sentences'] = [Sentence.__table__.columns.keys()]
        for sentence in Sentence.query:
            data['sentences'].append(_to_minimal_string(sentence.entry.values()))

        pyexcel_xlsxwx.save_data('user/HanziLevelUp.xlsx', data, config={'format': None})
        return Response(status=201)

    return Response(status=304)


@app.route('/get/export/<filename>')
def download_export(filename):
    return send_from_directory('../user', filename, as_attachment=True)
