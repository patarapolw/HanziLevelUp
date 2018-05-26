import jieba
import regex

from webapp.databases import Sentence, Vocab


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
