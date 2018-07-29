import jieba
import regex
from datetime import datetime, timedelta

from CJKhyperradicals.dict import Cedict
from CJKhyperradicals.sentence import SpoonFed, jukuu
from webapp.databases import Sentence, Vocab


def get_extra_vocab():
    pre_extra_vocab = set(sum([list(jieba.cut_for_search(sentence.sentence)) for sentence in Sentence.query], []))
    extra_vocab = set()
    for vocab in pre_extra_vocab:
        if regex.match(r'[\p{IsHan}\p{InCJK_Radicals_Supplement}\p{InKangxi_Radicals}]', vocab):
            if Vocab.query.filter(Vocab.vocab == vocab).count() == 0:
                extra_vocab.add(vocab)

    return extra_vocab


def get_extra_vocab_with_id():
    return [[-i, vocab, 'jieba'] for i, vocab in enumerate(get_extra_vocab())]


def get_all_vocab_plus():
    return [[vocab.id, vocab.vocab, 'user'] for vocab in Vocab.query] + get_extra_vocab_with_id()


class VocabInfo:
    def __init__(self):
        self.cedict = Cedict()

    def get_iter(self, vocab_list: list):
        for vocab in vocab_list:
            for entry in self.cedict.search_vocab(vocab):
                yield entry


class VocabToSentence:
    def __init__(self):
        self.spoon_fed = SpoonFed()

    def convert(self, vocab, online=True):
        sentences = list(self.spoon_fed.get_sentence(vocab))[:10]
        if len(sentences) == 0 and online:
            sentences = list(jukuu(vocab))

        return sentences


def sentence_to_vocab(sentence):
    used_vocab = set()
    for vocab in jieba.cut_for_search(sentence):
        if regex.match(r'[\p{IsHan}\p{InCJK_Radicals_Supplement}\p{InKangxi_Radicals}]', vocab):
            if vocab not in used_vocab:
                yield vocab
            used_vocab.add(vocab)


def get_last_day_vocab():
    for vocab in Vocab.query[::-1]:
        if datetime.utcnow() - vocab.modified < timedelta(days=1):
            yield [vocab.id, vocab.vocab, vocab.modified, 'vocab']
