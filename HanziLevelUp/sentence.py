from datetime import datetime, timedelta
import jieba

from webapp.databases import Sentence


def get_last_day_sentences():
    for sentence in Sentence.query[::-1]:
        if datetime.utcnow() - sentence.modified < timedelta(days=1):
            yield [sentence.id, sentence.sentence, sentence.modified, 'sentence']


def cut_sentence(item):
    segments = jieba.cut(item)

    sentence_segments = []
    for segment in segments:
        if segment in ('《', '"', '\''):
            yield ''.join(sentence_segments)
            sentence_segments = []

        sentence_segments.append(segment)

        if segment in ('。', '？', '！', '：', '》', ' ', '\n', '/', '"', '\''):
            yield ''.join(sentence_segments)
            sentence_segments = []

    yield ''.join(sentence_segments)
