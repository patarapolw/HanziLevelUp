from datetime import datetime, timedelta
import os
import csv

from CJKhyperradicals.sentence import SpoonFed
from webapp.databases import Sentence

spoonfed = SpoonFed()


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


def format_sentence_entry(sentence, sentence_id):
    lookup = list(spoonfed.get_sentence(sentence))
    if len(lookup) > 0:
        english = lookup[0][1]
        try:
            pinyin = lookup[0][2]
        except IndexError:
            pinyin = ''
    else:
        english = pinyin = ''

    return [
        english,
        pinyin,
        sentence,
        sentence_id
    ]


def sentence_to_csv():
    with open(os.path.join('tmp', 'sentence.csv'), 'w') as f:
        writer = csv.writer(f)
        for entry_id, entry in [(sentence.id, sentence.sentence) for sentence in Sentence.query]:
            writer.writerow(format_sentence_entry(entry, entry_id))
