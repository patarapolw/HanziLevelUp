import json
from datetime import datetime

from flask import request, jsonify, Response

from HanziLevelUp.vocab import (get_all_vocab_plus, VocabInfo, VocabToSentence, sentence_to_vocab,
                                get_last_day_vocab)
from webapp import app, db
from webapp.databases import Vocab, Hanzi


@app.route('/post/vocab/getAll', methods=['POST'])
def get_all_vocab():
    return jsonify(get_all_vocab_plus())


@app.route('/post/vocab/getRecent', methods=['POST'])
def get_recent_vocab():
    entries = list(get_last_day_vocab())
    if len(entries) < 10:
        entries = list(reversed([[vocab.id, vocab.vocab] for vocab in Vocab.query[-10:]]))

    return jsonify(entries)


@app.route('/post/vocab/add', methods=['POST'])
def add_vocab():
    vocab = request.form.get('item')

    previous_entry = Vocab.query.filter_by(vocab=vocab).first()
    if previous_entry is None:
        vocab_query = Vocab(entry=vocab, is_user=True)
        vocab_id = str(vocab_query.id)
        db.session.add(vocab_query)
    else:
        previous_entry.is_user = True
        previous_entry.modified = datetime.now()
        vocab_id = str(previous_entry.id)

    for hanzi in set(vocab):
        previous_entry = Hanzi.query.filter_by(hanzi=hanzi).first()
        if previous_entry is None:
            pass
            hanzi_query = Hanzi(entry=hanzi)
            db.session.add(hanzi_query)
        else:
            previous_entry.modified = datetime.now()

    db.session.commit()

    return vocab_id


@app.route('/post/vocab/delete', methods=['POST'])
def delete_vocab():
    Vocab.query.filter_by(vocab=request.form.get('item')).delete()
    db.session.commit()
    return Response(status=303)


@app.route('/post/vocab/getListInfo', methods=['POST'])
def get_array_info():
    return jsonify(list(VocabInfo().get_iter(json.loads(request.form.get('list')))))


@app.route('/post/vocab/getSentences', methods=['POST'])
def get_sentences():
    return jsonify(list(VocabToSentence().convert(request.form.get('vocab'))))


@app.route('/post/vocab/fromSentence', methods=['POST'])
def from_sentence():
    return jsonify(list(sentence_to_vocab(request.form.get('sentence'))))
