from random import shuffle
from datetime import datetime, timedelta

from flask import request, jsonify

from webapp import app, db
from webapp.databases import Sentence


@app.route('/getAllSentences', methods=['POST'])
def get_all_sentences():
    if request.method == 'POST':
        all_sentences = [[sentence.id, sentence.sentence] for sentence in Sentence.query]
        shuffle(all_sentences)

        return jsonify(all_sentences)

    return '0'


@app.route('/getRecentSentences', methods=['POST'])
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


@app.route('/addSentence', methods=['POST'])
def add_sentence():
    if request.method == 'POST':
        new_sentence = Sentence(sentence=request.form.get('sentence'))
        db.session.add(new_sentence)
        db.session.commit()

        return str(new_sentence.id)

    return '0'


@app.route('/deleteSentence', methods=['POST'])
def delete_sentence():
    if request.method == 'POST':
        Sentence.query.filter_by(id=int(request.form.get('sentence_id'))).delete()
        db.session.commit()
        return '1'

    return '0'
