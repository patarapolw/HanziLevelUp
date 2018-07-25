import pyexcel_export
import regex
from collections import OrderedDict

from CJKhyperradicals.sentence import SpoonFed
from CJKhyperradicals.dict import HanziDict, Cedict
from HanziLevelUp.hanzi import get_all_hanzi, HanziLevel
from HanziLevelUp.vocab import get_all_vocab_plus, VocabToSentence
from webapp.databases import Sentence

HANZI_HEADER = ['Hanzi', 'Pinyin', 'English', 'Heisig', 'Variant', 'Kanji',
                'Level', 'Note', 'Tags']
VOCAB_HEADER = ['Entry', 'Simplified', 'Traditional', 'Pinyin', 'English', 'Sentence',
                'Level', 'Note', 'Tags']
SENTENCE_HEADER = ['Sentence', 'Pinyin', 'English',
                   'Level', 'Note', 'Tags']


class ExcelExport:
    def __init__(self, filename: str):
        self.filename = filename
        self.hanzi_formatter = HanziFormatter()
        self.vocab_formatter = VocabFormatter()
        self.sentence_formatter = SentenceFormatter()

        try:
            self.data, self.meta = pyexcel_export.get_data(self.filename)

            self.pre_existing = {
                'Hanzi': set([row[0] for row in self.data['Hanzi'][1:]]),
                'Vocab': set([row[0] for row in self.data['Vocab'][1:]]),
                'sentences': set([row[0] for row in self.data['sentences'][1:]]),
            }

        except FileNotFoundError:
            self.data = OrderedDict([
                ('Hanzi', list()),
                ('Vocab', list()),
                ('sentences', list())
            ])
            self.meta = pyexcel_export.get_meta()

            self.pre_existing = {
                'Hanzi': set(),
                'Vocab': set(),
                'sentences': set(),
            }

    def from_db(self):
        ws = self.data['Hanzi']
        ws.append(HANZI_HEADER)
        for hanzi in get_all_hanzi():
            if hanzi not in self.pre_existing['Hanzi']:
                ws.append(self.hanzi_formatter.format(hanzi))

        ws = self.data['Vocab']
        ws.append(VOCAB_HEADER)
        for _, vocab in get_all_vocab_plus():
            if vocab not in self.pre_existing['Vocab']:
                ws.append(self.vocab_formatter.format(vocab))

        ws = self.data['sentences']
        ws.append(SENTENCE_HEADER)
        for sent_query in Sentence.query:
            sentence = sent_query.sentence
            if sentence not in self.pre_existing['sentences']:
                ws.append(self.sentence_formatter.format(sentence))

        self.save()

    def save(self):
        pyexcel_export.save_data(self.filename, data=self.data, meta=self.meta)


class HanziFormatter:
    def __init__(self):
        self.hanzi_dict = HanziDict()
        self.hanzi_level = HanziLevel()

    def format(self, hanzi):
        print(hanzi)

        entry = self.hanzi_dict.entries.get(hanzi, dict())
        result = [
            hanzi,
            entry.get('Pin1Yin1', ''),
            entry.get('Meaning', ''),
            entry.get('Heisig', ''),
            entry.get('Variant', ''),
            entry.get('Kanji', ''),
            self.hanzi_level.get_hanzi_level(hanzi),
            '',
            ''
        ]
        assert len(result) == len(HANZI_HEADER), 'Invalid HanziFormatter'

        return result


class VocabFormatter:
    def __init__(self):
        self.cedict = Cedict()
        self.hanzi_level = HanziLevel()
        self.vocab_to_sentence = VocabToSentence()

    def format(self, entry):
        print(entry)

        dict_result = list(self.cedict.search_vocab(entry))
        simplified = ', '.join([item[1] for item in dict_result])
        traditional = ', '.join([item[0] for item in dict_result])
        pinyin = ', '.join([item[2] for item in dict_result])
        english = ', '.join([item[3] for item in dict_result])
        sentences = self.vocab_to_sentence.convert(entry, online=False)
        # traditional = pinyin = english = ''

        level = max([self.hanzi_level.get_hanzi_level(hanzi) for hanzi in entry])

        result = [
            entry,
            simplified,
            traditional,
            pinyin,
            english,
            '\n'.join(['\n'.join(pair) for pair in sentences]),
            level,
            '',
            ''
        ]
        assert len(result) == len(VOCAB_HEADER), 'Invalid VocabFormatter'

        return result


class SentenceFormatter:
    def __init__(self):
        self.spoon_fed = SpoonFed()
        self.hanzi_level = HanziLevel()

    def format(self, sentence):
        print(sentence)

        lookup = list(self.spoon_fed.get_sentence(sentence))
        if len(lookup) > 0:
            english = lookup[0][1]
            try:
                pinyin = lookup[0][2]
            except IndexError:
                pinyin = ''
        else:
            english = pinyin = ''

        result = [
            sentence,
            pinyin,
            english,
            ', '.join([str(self.hanzi_level.get_hanzi_level(char)) for char in sentence
                       if regex.match(r'\p{IsHan}', char)]),
            '',
            ''
        ]
        assert len(result) == len(SENTENCE_HEADER), 'Invalid SentenceFormatter'

        return result
