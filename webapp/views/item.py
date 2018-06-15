import html

from flask import request, jsonify

from HanziLevelUp.sentence import get_last_day_sentences, cut_sentence
from HanziLevelUp.vocab import get_last_day_vocab
from webapp import app
from webapp.databases import Sentence, Vocab


@app.route('/post/item/getRecent', methods=['POST'])
def get_recent_items():
    if request.method == 'POST':
        entries = sorted(list(get_last_day_sentences()) + list(get_last_day_vocab()), key=lambda x: x[2], reverse=True)

        if len(entries) < 10:
            entries = sorted([[sentence.id, sentence.sentence, sentence.modified, 'sentence']
                              for sentence in Sentence.query[-10:]]
                             + [[vocab.id, vocab.vocab, vocab.modified, 'vocab']
                                for vocab in Vocab.query[-10:]],
                             key=lambda x: x[2], reverse=True)[:10]

        return jsonify(entries)

    return '0'


@app.route('/post/item/cut', methods=['POST'])
def cut_item():
    if request.method == 'POST':
        return jsonify(list(cut_sentence(html.escape(request.form.get('item')))))

    return '0'
