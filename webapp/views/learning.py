from flask import request

from webapp import app, db
from webapp.databases import Vocab, Sentence


@app.route('/post/<item>/inLearning', methods=['POST'])
def in_learning(item):
    if item == 'vocab':
        return str(Vocab.query.filter_by(vocab=request.form.get('item'), is_user=True).count())
    elif item == 'sentence':
        return str(Sentence.query.filter_by(sentence=request.form.get('item')).count())

    return '-1'
