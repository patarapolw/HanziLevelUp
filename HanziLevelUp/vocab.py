import jieba
import regex

from CJKhyperradicals.dict import Cedict
from CJKhyperradicals.sentence import SpoonFed, jukuu
from webapp.databases import Sentence, Vocab

cedict = Cedict()
spoon_fed = SpoonFed()


def get_extra_vocab():
    pre_extra_vocab = set(sum([list(jieba.cut_for_search(sentence.sentence)) for sentence in Sentence.query], []))
    extra_vocab = set()
    for vocab in pre_extra_vocab:
        if regex.match(r'[\p{IsHan}\p{InCJK_Radicals_Supplement}\p{InKangxi_Radicals}]', vocab):
            extra_vocab.add(vocab)

    return extra_vocab


def get_extra_vocab_with_id():
    return [[-i, vocab] for i, vocab in enumerate(get_extra_vocab())]


def get_all_vocab_plus():
    return [[vocab.id, vocab.vocab] for vocab in Vocab.query] + get_extra_vocab_with_id()


def get_vocab_array_info(vocab_list):
    for vocab in vocab_list:
        for entry in cedict.search_vocab(vocab):
            yield entry


def vocab_to_sentences(vocab):
    sentences = list(spoon_fed.get_sentence(vocab))[:10]
    if len(sentences) == 0:
        sentences = list(jukuu(vocab))

    return sentences
