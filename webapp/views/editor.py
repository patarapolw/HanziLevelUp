from flask import request, jsonify, Response
import math
import json
from datetime import datetime
import sqlalchemy.exc

from webapp import app, db
from webapp.databases import Hanzi, Vocab, Sentence, SrsTuple


@app.route('/post/editor/<item_type>/all/<page_number>')
def all_records(item_type, page_number, page_size=10):
    if item_type == 'hanzi':
        SrsRecord = Hanzi
    elif item_type == 'vocab':
        SrsRecord = Vocab
    elif item_type == 'sentences':
        SrsRecord = Sentence
    else:
        return Response(status=404)

    def _filter():
        for srs_record in SrsRecord.query.order_by(SrsRecord.modified.desc()):
            # record_data = srs_record.data
            # if record_data:
            #     record_data = json.loads(record_data)
            #     if 'level' not in record_data.keys():
            #         record_data['level'] = max(record_data['levels'])
            #
            #     if record_data['level'] <= 5 and getattr(srs_record, 'is_user', True):
            #         yield srs_record
            # else:
                yield srs_record

    page_number = int(page_number)

    query = list(_filter())
    total = len(query)

    if page_number < 0:
        page_number = math.ceil(total / page_size) + page_number + 1

    offset = (page_number - 1) * page_size

    records = query[offset:offset + page_size]

    data = [SrsTuple.from_db(record) for record in records]

    return jsonify({
        'data': data,
        'pages': {
            'from': offset + 1 if total > 0 else 0,
            'to': total if offset + page_size > total else offset + page_size,
            'number': page_number,
            'total': total
        }
    })


@app.route('/post/editor/<item_type>/search/<page_number>', methods=['POST'])
def search(item_type, page_number, page_size=10):
    if item_type == 'hanzi':
        SrsRecord = Hanzi
    elif item_type == 'vocab':
        SrsRecord = Vocab
    elif item_type == 'sentences':
        SrsRecord = Sentence
    else:
        return Response(status=404)

    def _search():
        query_string = request.get_json()['q'].lower()

        for srs_record in SrsRecord.query.order_by(SrsRecord.modified.desc()):
            if any([query_string in cell.lower()
                    for cell in (srs_record.front, srs_record.back, srs_record.tags, srs_record.data) if cell]):
                yield srs_record

    page_number = int(page_number)

    query = list(_search())
    total = len(query)

    if page_number < 0:
        page_number = math.ceil(total / page_size) + page_number + 1

    offset = (page_number - 1) * page_size

    records = query[offset:offset + page_size]

    data = [SrsTuple.from_db(record) for record in records]

    return jsonify({
        'data': data,
        'pages': {
            'from': offset + 1 if total > 0 else 0,
            'to': total if offset + page_size > total else offset + page_size,
            'number': page_number,
            'total': total
        }
    })


@app.route('/post/editor/<item_type>/edit', methods=['POST'])
def edit_record(item_type):
    if item_type == 'hanzi':
        SrsRecord = Hanzi
    elif item_type == 'vocab':
        SrsRecord = Vocab
    elif item_type == 'sentences':
        SrsRecord = Sentence
    else:
        return Response(status=404)

    record = request.get_json()
    old_record = SrsRecord.query.filter_by(id=record['id']).first()
    if old_record is None:
        srs_tuple = SrsTuple()
        setattr(srs_tuple, record['fieldName'], record['data'])

        new_record = SrsRecord(**srs_tuple.to_db())

        try:
            db.session.add(new_record)
            db.session.commit()
            record_id = new_record.id
        except sqlalchemy.exc.IntegrityError:
            return Response(status=400)
    else:
        setattr(old_record, record['fieldName'], record['data'])
        old_record.modified = datetime.now()

        db.session.commit()
        record_id = old_record.id

    return jsonify({
        'id': record_id
    }), 201

