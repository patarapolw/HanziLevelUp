from flask import request, jsonify

from webapp import app, db
from webapp.databases import Sentence


@app.route('/getSentence', methods=['POST'])
def get_sentence():
    if request.method == 'POST':
        all_sentences = Sentence.query[-10:]
        return jsonify([[sentence.id, sentence.sentence] for sentence in all_sentences])

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
