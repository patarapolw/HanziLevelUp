import json

from flask import request, jsonify

from HanziLevelUp.vocab import (get_all_vocab_plus, VocabInfo, VocabToSentence, sentence_to_vocab,
                                get_last_day_vocab)
from webapp import app, db
from webapp.databases import Vocab


@app.route('/post/vocab/getAll', methods=['POST'])
def get_all_vocab():
    if request.method == 'POST':
        return jsonify(get_all_vocab_plus())

    return '0'


@app.route('/post/vocab/getRecent', methods=['POST'])
def get_recent_vocab():
    if request.method == 'POST':
        entries = list(get_last_day_vocab())
        if len(entries) < 10:
            entries = list(reversed([[vocab.id, vocab.vocab] for vocab in Vocab.query[-10:]]))

        return jsonify(entries)

    return '0'


@app.route('/post/vocab/add', methods=['POST'])
def add_vocab():
    if request.method == 'POST':
        new_vocab = Vocab(vocab=request.form.get('item'))
        db.session.add(new_vocab)
        db.session.commit()

        return str(new_vocab.id)

    return '0'


@app.route('/post/vocab/delete', methods=['POST'])
def delete_vocab():
    if request.method == 'POST':
        Vocab.query.filter_by(id=int(request.form.get('id'))).delete()
        db.session.commit()
        return '1'

    return '0'


@app.route('/post/vocab/getListInfo', methods=['POST'])
def get_array_info():
    if request.method == 'POST':
        return jsonify(list(VocabInfo().get_iter(json.loads(request.form.get('list')))))

    return '0'


@app.route('/post/vocab/getSentences', methods=['POST'])
def get_sentences():
    if request.method == 'POST':
        return jsonify(list(VocabToSentence().convert(request.form.get('vocab'))))

    return '0'


@app.route('/post/vocab/fromSentence', methods=['POST'])
def from_sentence():
    if request.method == 'POST':
        return jsonify(list(sentence_to_vocab(request.form.get('sentence'))))

    return '0'
