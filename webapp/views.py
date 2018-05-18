from flask import request

from webapp import app
from webapp.utils import do_speak

speak_processes = []


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
