from flask import request, send_from_directory, jsonify

from webapp import app, db
from webapp.databases import Sentence
from webapp.utils import do_speak

speak_processes = []


@app.route('/getSentence', methods=['POST'])
def get_sentence():
    if request.method == 'POST':
        all_sentences = Sentence.query[-10:]
        return jsonify([[sentence.id, sentence.sentence] for sentence in all_sentences])

    return '0'


@app.route('/speak', methods=['POST'])
def speak():
    if request.method == 'POST':
        global speak_processes

        for process in speak_processes:
            process.kill()
        speak_processes = list()
        sentence = request.form.get('sentence')
        speak_processes.append(do_speak(sentence))

        return '1'

    return '0'


@app.route('/addSentence', methods=['POST'])
def add_sentence():
    if request.method == 'POST':
        new_sentence = Sentence(sentence=request.form.get('sentence'))
        db.session.add(new_sentence)
        db.session.commit()

        return str(new_sentence.id)

    return '0'


@app.route('/deleteSentence', methods=['POST'])
def delete_sentence():
    if request.method == 'POST':
        Sentence.query.filter_by(id=int(request.form.get('sentence_id'))).delete()
        db.session.commit()
        return '1'

    return '0'


@app.route('/static/js/<pathname>')
def serve_js(pathname):
    return send_from_directory('static/js', pathname)


@app.route('/static/css/<pathname>')
def serve_css(pathname):
    return send_from_directory('static/css', pathname)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')
