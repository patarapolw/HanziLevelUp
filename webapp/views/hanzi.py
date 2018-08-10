import regex
from datetime import datetime, timedelta

from flask import request, jsonify

from webapp import app
from webapp.databases import Sentence, Vocab

from CJKhyperradicals.decompose import Decompose
from CJKhyperradicals.dict import Cedict
from CJKhyperradicals.frequency import ChineseFrequency
from CJKhyperradicals.variant import Variant

from HanziLevelUp.vocab import VocabToSentence

decompose = Decompose()
variant = Variant()
cedict = Cedict()
sorter = ChineseFrequency()


@app.route('/post/hanzi/getInfo', methods=['POST'])
def get_info():
    current_char = request.form.get('character')

    return jsonify({
        'compositions': decompose.get_sub(current_char),
        'supercompositions': sorter.sort_char(decompose.get_super(current_char)),
        'variants': variant.get(current_char),
        'vocab': sorter.sort_vocab(list(cedict.search_hanzi(current_char)))[:10]
    })


@app.route('/post/hanzi/getSentences', methods=['POST'])
def from_hanzi_get_sentences():
    current_char = request.form.get('character')

    if not current_char.isdigit():
        sentences = list(VocabToSentence().convert(current_char))
    else:
        sentences = []

    return jsonify({
        'sentences': sentences
    })


@app.route('/post/hanzi/getAll', methods=['POST'])
def get_hanzi():
    all_entries = ([sentence.sentence for sentence in Sentence.query] +
                   [vocab.vocab for vocab in Vocab.query])
    all_hanzi = list(set([char for char in
                          regex.sub(r'[^\p{IsHan}\p{InCJK_Radicals_Supplement}\p{InKangxi_Radicals}]',
                                    '',
                                    ''.join(all_entries))]))
    return ''.join(all_hanzi)


@app.route('/post/hanzi/fromSentence', methods=['POST'])
def sentence_to_hanzi():
    def last_days_entries():
        for sentence in Sentence.query[::-1]:
            if datetime.utcnow() - sentence.modified < timedelta(days=1):
                yield sentence.sentence

    entries = list(last_days_entries())
    print(len(entries))
    if len(entries) < 10:
        entries = reversed([sentence.sentence for sentence in Sentence.query[-10:]])

    all_hanzi = list(set([char for char in
                          regex.sub(r'[^\p{IsHan}\p{InCJK_Radicals_Supplement}\p{InKangxi_Radicals}]',
                                    '',
                                    ''.join(entries))]))
    return ''.join(all_hanzi)


@app.route('/post/hanzi/fromVocab', methods=['POST'])
def vocab_to_hanzi():
    def last_days_entries():
        for vocab in Vocab.query[::-1]:
            if datetime.utcnow() - vocab.modified < timedelta(days=1):
                yield vocab.vocab

    entries = list(last_days_entries())
    if len(entries) < 10:
        entries = reversed([vocab.vocab for vocab in Vocab.query[-10:]])

    all_hanzi = list(set([char for char in
                          regex.sub(r'[^\p{IsHan}\p{InCJK_Radicals_Supplement}\p{InKangxi_Radicals}]',
                                    '',
                                    ''.join(entries))]))
    return ''.join(all_hanzi)
