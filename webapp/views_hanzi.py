import regex
from random import shuffle

from flask import request, jsonify

from webapp import app
from webapp.databases import Sentence, Vocab

from CJKhyperradicals.decompose import Decompose
from CJKhyperradicals.dict import Cedict
from CJKhyperradicals.frequency import ChineseFrequency
from CJKhyperradicals.variant import Variant
from CJKhyperradicals.sentence import jukuu, SpoonFed

decompose = Decompose()
variant = Variant()
cedict = Cedict()
sorter = ChineseFrequency()
spoonfed = SpoonFed()


@app.route('/getHyperradicals', methods=['POST'])
def get_hyperradicals():
    if request.method == 'POST':
        current_char = request.form.get('character')
        sentences = list(spoonfed.get_sentence(current_char))[:10]
        if len(sentences) == 0:
            sentences = list(jukuu(current_char))

        return jsonify({
            'compositions': decompose.get_sub(current_char),
            'supercompositions': sorter.sort_char(decompose.get_super(current_char)),
            'variants': variant.get(current_char),
            'vocab': sorter.sort_vocab([list(item) for item in cedict.search_hanzi(current_char)])[:10],
            'sentences': sentences
        })

    return '0'


@app.route('/getHanzi', methods=['POST'])
def get_hanzi():
    if request.method == 'POST':
        all_entries = ([sentence.sentence for sentence in Sentence.query[-10:]] +
                       [vocab.vocab for vocab in Vocab.query[-10:]])
        all_hanzi = list(set([char for char in
                              regex.sub(r'[^\p{IsHan}\p{InCJK_Radicals_Supplement}\p{InKangxi_Radicals}]',
                                        '',
                                        ''.join(all_entries))]))
        shuffle(all_hanzi)
        return ''.join(all_hanzi)

    return '0'
