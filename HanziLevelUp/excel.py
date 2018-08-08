import pyexcel_xlsxwx
import regex
from collections import OrderedDict
import namedlist as nl
from datetime import datetime

from CJKhyperradicals.sentence import SpoonFed
from CJKhyperradicals.dict import HanziDict, Cedict
from HanziLevelUp.hanzi import get_all_hanzi, HanziLevel
from HanziLevelUp.vocab import get_all_vocab_plus, VocabToSentence
from webapp.databases import Sentence


HanziRecord = nl.namedlist('HanziRecord', [
    'Hanzi', 'Pinyin', 'English', 'Heisig', 'Variants', 'Kanji',
    'Level', 'Note', 'Tags',
    ('Created', datetime.now(datetime.now().astimezone().tzinfo).isoformat())
], default='')

VocabRecord = nl.namedlist('VocabRecord', [
    'Vocab', 'Simplified', 'Traditional', 'Pinyin', 'English', 'Sentence',
    'Level', 'Note', 'Tags',
    'Source',
    ('Created', datetime.now(datetime.now().astimezone().tzinfo).isoformat())
], default='')

SentenceRecord = nl.namedlist('SentenceRecord', [
    'Sentence', 'Pinyin', 'English',
    'Levels', 'Note', 'Tags',
    ('Created', datetime.now(datetime.now().astimezone().tzinfo).isoformat())
], default='')


class ExcelExport:
    def __init__(self, filename: str):
        self.filename = filename
        self.hanzi_formatter = HanziFormatter()
        self.vocab_formatter = VocabFormatter()
        self.sentence_formatter = SentenceFormatter()

        try:
            self.data, self.meta = pyexcel_export.get_data(self.filename)

            self.pre_existing = {
                'hanzi': set([HanziRecord(*row).Hanzi for row in self.data['Hanzi'][1:]]),
                'vocab': set(),
                'sentences': set([SentenceRecord(*row).Sentence for row in self.data['sentences'][1:]]),
            }

            to_pop = set()
            for i, row in enumerate(self.data['Vocab'][1:]):
                record = VocabRecord(*row)
                if record.Source == 'user':
                    self.pre_existing['Vocab'].add(record.Entry)
                else:
                    to_pop.add(i + 1)

            self.data['Vocab'] = [row for i, row in enumerate(self.data['Vocab']) if i not in to_pop]

        except FileNotFoundError:
            self.data = OrderedDict([
                ('hanzi', [HanziRecord._fields]),
                ('vocab', [VocabRecord._fields]),
                ('sentences', [SentenceRecord._fields])
            ])
            self.meta = pyexcel_export.get_meta()

            self.pre_existing = {
                'hanzi': set(),
                'vocab': set(),
                'sentences': set(),
            }

    def from_db(self):
        ws = self.data['hanzi']
        for hanzi in get_all_hanzi():
            if hanzi not in self.pre_existing['Hanzi']:
                ws.append(self.hanzi_formatter.format(hanzi))

        ws = self.data['vocab']
        for _, vocab, source in get_all_vocab_plus():
            if vocab not in self.pre_existing['Vocab']:
                ws.append(self.vocab_formatter.format(vocab, source))

        ws = self.data['sentences']
        for sent_query in Sentence.query:
            sentence = sent_query.sentence
            if sentence not in self.pre_existing['sentences']:
                ws.append(self.sentence_formatter.format(sentence))

        self.save()

    def save(self):
        pyexcel_export.save_data(self.filename, data=self.data, meta=self.meta,
                                 reset_height=True)


class HanziFormatter:
    def __init__(self):
        self.hanzi_dict = HanziDict()
        self.hanzi_level = HanziLevel()

    def format(self, hanzi):
        print(hanzi)

        entry = self.hanzi_dict.entries.get(hanzi, dict())
        result = HanziRecord(
            Hanzi=hanzi,
            Pinyin=entry.get('Pin1Yin1', ''),
            English=entry.get('Meaning', ''),
            Heisig=entry.get('Heisig', ''),
            Variant=entry.get('Variant', ''),
            Kanji=entry.get('Kanji', ''),
            Level=self.hanzi_level.get_hanzi_level(hanzi)
        )

        return result


class VocabFormatter:
    def __init__(self):
        self.cedict = Cedict()
        self.hanzi_level = HanziLevel()
        self.vocab_to_sentence = VocabToSentence()

    def format(self, entry, source):
        print(entry, source)

        dict_result = list(self.cedict.search_vocab(entry))
        simplified = ', '.join([item[1] for item in dict_result])
        traditional = ', '.join([item[0] for item in dict_result])
        pinyin = ', '.join([item[2] for item in dict_result])
        english = ', '.join([item[3] for item in dict_result])
        sentences = self.vocab_to_sentence.convert(entry, online=False)
        # traditional = pinyin = english = ''

        level = max([self.hanzi_level.get_hanzi_level(hanzi) for hanzi in entry])

        result = VocabRecord(
            Entry=entry,
            Simplified=simplified,
            Traditional=traditional,
            Pinyin=pinyin,
            English=english,
            Sentence='\n'.join(['\n'.join(pair) for pair in sentences]),
            Level=level,
            Source=source
        )

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

        result = SentenceRecord(
            Sentence=sentence,
            Pinyin=pinyin,
            English=english,
            Levels=', '.join([str(self.hanzi_level.get_hanzi_level(char)) for char in sentence
                              if regex.match(r'\p{IsHan}', char)])
        )

        return result
