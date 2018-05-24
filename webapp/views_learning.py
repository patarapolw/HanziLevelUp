from flask import request

from webapp import app, db
from webapp.databases import Vocab, Sentence


@app.route('/vocabInLearning', methods=['POST'])
def vocab_in_learning():
    if request.method == 'POST':
        return str(Vocab.query.filter(Vocab.vocab == request.form.get('vocab')).count())

    return '-1'


@app.route('/addVocabToLearning', methods=['POST'])
def add_vocab_to_learning():
    if request.method == 'POST':
        new_vocab = Vocab(vocab=request.form.get('vocab'))
        db.session.add(new_vocab)
        db.session.commit()

        return '1'

    return '0'


@app.route('/removeVocabFromLearning', methods=['POST'])
def remove_vocab_from_learning():
    if request.method == 'POST':
        Vocab.query.filter_by(vocab=request.form.get('vocab')).delete()
        db.session.commit()

        return '1'

    return '0'


@app.route('/sentenceInLearning', methods=['POST'])
def sentence_in_learning():
    if request.method == 'POST':
        return str(Sentence.query.filter(Sentence.sentence == request.form.get('sentence')).count())

    return '-1'


@app.route('/addSentenceToLearning', methods=['POST'])
def add_sentence_to_learning():
    if request.method == 'POST':
        new_sentence = Sentence(sentence=request.form.get('sentence'))
        db.session.add(new_sentence)
        db.session.commit()

        return '1'

    return '0'


@app.route('/removeSentenceFromLearning', methods=['POST'])
def remove_sentence_from_learning():
    if request.method == 'POST':
        Sentence.query.filter_by(sentence=request.form.get('sentence')).delete()
        db.session.commit()

        return '1'

    return '0'
