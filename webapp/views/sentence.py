from flask import request, jsonify, Response

from datetime import datetime
import regex
import jieba

from HanziLevelUp.sentence import get_last_day_sentences
from webapp import app, db
from webapp.databases import Sentence, Vocab, Hanzi


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
    sentence = request.form.get('item')

    previous_entry = Sentence.query.filter_by(sentence=sentence).first()
    if previous_entry is None:
        sentence_query = Sentence(entry=sentence)
        sentence_id = str(sentence_query.id)
        db.session.add(sentence_query)
    else:
        previous_entry.modified = datetime.now()
        sentence_id = str(previous_entry.id)

    for vocab in set((x for x in jieba.cut_for_search(sentence) if regex.search(r'\p{IsHan}', x))):
        previous_entry = Vocab.query.filter_by(vocab=vocab).first()
        if previous_entry is None:
            vocab_query = Vocab(entry=vocab, is_user=False)
            db.session.add(vocab_query)
        else:
            previous_entry.modified = datetime.now()

    for hanzi in set(regex.findall(r'\p{IsHan}', sentence)):
        previous_entry = Hanzi.query.filter_by(hanzi=hanzi).first()
        if previous_entry is None:
            hanzi_query = Hanzi(entry=hanzi)
            db.session.add(hanzi_query)
        else:
            previous_entry.modified = datetime.now()

    db.session.commit()

    return sentence_id


@app.route('/post/sentence/delete', methods=['POST'])
def delete_sentence():
    sentence = Sentence.query.filter_by(sentence=request.form.get('item')).first()
    if sentence is not None:
        db.session.delete(sentence)
        db.session.commit()
        return Response(status=303)
    else:
        return Response(status=304)
