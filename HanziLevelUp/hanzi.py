import regex

from HanziLevelUp.dir import database_path


class HanziLevel:
    def __init__(self):
        self.level_dict = dict()
        level = 0
        with open(database_path('hanzi_level.txt')) as f:
            for row in f:
                if regex.match(r'\p{IsHan}', row):
                    level += 1
                    for char in row.strip():
                        self.level_dict[char] = level

    def get_hanzi_level(self, hanzi):
        return self.level_dict.get(hanzi, 0)


def get_all_hanzi():
    from webapp.databases import Sentence, Vocab

    sentences = [sentence.sentence for sentence in Sentence.query]
    vocabs = [vocab.vocab for vocab in Vocab.query]

    return set(regex.findall(r'\p{IsHan}', ''.join(sentences) + ''.join(vocabs)))
