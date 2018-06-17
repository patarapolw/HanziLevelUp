from datetime import datetime, timedelta

from webapp.databases import Sentence


def get_last_day_sentences():
    for sentence in Sentence.query[::-1]:
        if datetime.utcnow() - sentence.modified < timedelta(days=1):
            yield [sentence.id, sentence.sentence, sentence.modified, 'sentence']


def cut_sentence(item):
    sentence = ''
    for char in item:
        if char == '\n':
            yield char
        else:
            sentence += char
            if char in '。？！.?! ':
                yield sentence
                sentence = ''
    yield sentence
