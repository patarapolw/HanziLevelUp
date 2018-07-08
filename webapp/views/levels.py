from flask import send_file, request, jsonify

from HanziLevelUp.dir import database_path
from HanziLevelUp.vocab import get_all_vocab_plus
from webapp import app
from webapp.databases import Sentence


@app.route('/post/file/getLevels', methods=['POST'])
def get_levels():
    return send_file(database_path('hanzi_level.txt'))


@app.route('/post/vocab/getLevel', methods=['POST'])
def get_level_vocab():
    def within_level(vocab):
        for hanzi in vocab:
            if hanzi not in up_to_current_level_hanzi:
                return False
        return True

    def get_vocab():
        for result_to_examine in get_all_vocab_plus():
            for hanzi in current_level_hanzi:
                if hanzi in result_to_examine[1]:
                    if within_level(result_to_examine[1]):
                        yield result_to_examine
                    break

    if request.method == 'POST':
        current_level_hanzi = request.form.get('currentLevelHanzi')
        up_to_current_level_hanzi = request.form.get('previousLevelsHanzi') + current_level_hanzi

        result = list(get_vocab())
        return jsonify(result)

    return '0'


@app.route('/post/sentence/getLevel', methods=['POST'])
def get_level_sentences():
    def get_sentence():
        for sentence in Sentence.query:
            for hanzi in current_level_hanzi:
                if hanzi in sentence.sentence:
                    yield [sentence.id, sentence.sentence]
                    break

    if request.method == 'POST':
        current_level_hanzi = request.form.get('currentLevelHanzi')

        result = list(get_sentence())
        return jsonify(result)

    return '0'
