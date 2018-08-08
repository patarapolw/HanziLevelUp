from flask import request

from webapp import app, db
from webapp.databases import Vocab, Sentence


@app.route('/post/<item>/inLearning', methods=['POST'])
def in_learning(item):
    if item == 'vocab':
        return str(Vocab.query.filter(Vocab.vocab == request.form.get('item')).count())
    elif item == 'sentence':
        return str(Sentence.query.filter(Sentence.sentence == request.form.get('item')).count())

    return '-1'
