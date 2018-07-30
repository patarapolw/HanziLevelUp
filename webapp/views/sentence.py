from flask import request, jsonify

from HanziLevelUp.sentence import get_last_day_sentences
from webapp import app, db
from webapp.databases import Sentence


@app.route('/post/sentence/getAll', methods=['POST'])
def get_all_sentences():
    all_sentences = [[sentence.id, sentence.sentence] for sentence in Sentence.query]
    return jsonify(all_sentences)


@app.route('/post/sentence/getRecent', methods=['POST'])
def get_recent_sentences():
    entries = list(get_last_day_sentences())
    if len(entries) < 10:
        entries = list(reversed([[sentence.id, sentence.sentence] for sentence in Sentence.query[-10:]]))

    return jsonify(entries)


@app.route('/post/sentence/add', methods=['POST'])
def add_sentence():
    new_sentence = Sentence(sentence=request.form.get('item'))
    db.session.add(new_sentence)
    db.session.commit()

    return str(new_sentence.id)


@app.route('/post/sentence/delete', methods=['POST'])
def delete_sentence():
    Sentence.query.filter_by(id=int(request.form.get('id'))).delete()
    db.session.commit()
    return '1'
