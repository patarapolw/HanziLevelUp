import jieba
import regex

from flask import request, jsonify

from webapp import app, db
from webapp.databases import Vocab, Sentence

all_vocab = [[vocab.id, vocab.vocab] for vocab in Vocab.query]
pre_extra_vocab = set(sum([list(jieba.cut_for_search(sentence.sentence)) for sentence in Sentence.query], []))
extra_vocab = set()
for vocab in pre_extra_vocab:
    if regex.match(r'[\p{IsHan}\p{InCJK_Radicals_Supplement}\p{InKangxi_Radicals}]', vocab):
        extra_vocab.add(vocab)
all_vocab = list(enumerate(extra_vocab)) + all_vocab


@app.route('/getVocab', methods=['POST'])
def get_vocab():
    if request.method == 'POST':
        return jsonify(all_vocab)

    return '0'


@app.route('/addVocab', methods=['POST'])
def add_vocab():
    if request.method == 'POST':
        new_vocab = Vocab(vocab=request.form.get('vocab'))
        db.session.add(new_vocab)
        db.session.commit()

        return str(new_vocab.id)

    return '0'


@app.route('/deleteVocab', methods=['POST'])
def delete_vocab():
    if request.method == 'POST':
        Vocab.query.filter_by(id=int(request.form.get('vocab_id'))).delete()
        db.session.commit()
        return '1'

    return '0'
