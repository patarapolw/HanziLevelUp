from flask import request

from webapp import app, db
from webapp.databases import Vocab, Sentence


@app.route('/post/<item>/inLearning', methods=['POST'])
def in_learning(item):
    if request.method == 'POST':
        if item == 'vocab':
            return str(Vocab.query.filter(Vocab.vocab == request.form.get('item')).count())
        elif item == 'sentence':
            return str(Sentence.query.filter(Sentence.sentence == request.form.get('item')).count())

    return '-1'


@app.route('/post/<item>/addToLearning', methods=['POST'])
def add_to_learning(item):
    if request.method == 'POST':
        if item == 'vocab':
            new_item = Vocab(vocab=request.form.get('item'))
        elif item == 'sentence':
            new_item = Sentence(sentence=request.form.get('item'))
        else:
            return '0'

        db.session.add(new_item)
        db.session.commit()

        return '1'

    return '0'


@app.route('/post/<item>/removeFromLearning', methods=['POST'])
def remove_from_learning(item):
    if request.method == 'POST':
        if item == 'vocab':
            Vocab.query.filter_by(vocab=request.form.get('item')).delete()
        elif item == 'sentence':
            Sentence.query.filter_by(sentence=request.form.get('item')).delete()
        else:
            return '0'

        db.session.commit()

        return '1'

    return '0'
