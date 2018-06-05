from datetime import datetime, timedelta
import requests

from flask import request, jsonify

from webapp import app, db
from webapp.databases import Sentence


@app.route('/post/sentence/getAll', methods=['POST'])
def get_all_sentences():
    if request.method == 'POST':
        all_sentences = [[sentence.id, sentence.sentence] for sentence in Sentence.query]
        return jsonify(all_sentences)

    return '0'


@app.route('/post/sentence/getRecent', methods=['POST'])
def get_recent_sentences():
    def last_days_entries():
        for sentence in Sentence.query[::-1]:
            if datetime.utcnow() - sentence.modified < timedelta(days=1):
                yield [sentence.id, sentence.sentence]

    if request.method == 'POST':
        entries = list(last_days_entries())
        if len(entries) < 10:
            entries = list(reversed([[sentence.id, sentence.sentence] for sentence in Sentence.query[-10:]]))

        return jsonify(entries)

    return '0'


@app.route('/post/sentence/add', methods=['POST'])
def add_sentence():
    if request.method == 'POST':
        new_sentence = Sentence(sentence=request.form.get('item'))
        db.session.add(new_sentence)
        db.session.commit()

        return str(new_sentence.id)

    return '0'


@app.route('/post/sentence/delete', methods=['POST'])
def delete_sentence():
    if request.method == 'POST':
        Sentence.query.filter_by(id=int(request.form.get('id'))).delete()
        db.session.commit()
        return '1'

    return '0'
