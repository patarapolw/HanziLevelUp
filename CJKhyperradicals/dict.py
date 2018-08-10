import regex
import csv
from collections import OrderedDict

from CJKhyperradicals.dir import chinese_path


class Cedict:
    def __init__(self):
        self.entries = dict()
        with open(chinese_path('cedict_ts.u8')) as f:
            for i, row in enumerate(f):
                _ = regex.match(r'([^ ]+) ([^ ]+) \[(.+)\] /(.+)/', row)
                if _ is not None:
                    # trad, simp, pinyin, english = _.groups()
                    self.entries[i] = OrderedDict(zip(('traditional', 'simplified', 'pinyin', 'english'),
                                                      _.groups()))
                else:
                    # print(row)
                    pass

    def search_hanzi(self, hanzi):
        for entry in self.entries.values():
            if hanzi in (entry['traditional'] + entry['simplified']):
                yield entry

    def search_vocab(self, vocab):
        for entry in self.entries.values():
            if (vocab in (entry['traditional'], entry['simplified'])
                    # or vocab in regex.findall('[^\p{IsHan}\p{InCJK_Radicals_Supplement}\p{InKangxi_Radicals}\W]+',
                    #                           entry['english'])
            ):
                yield entry


class HanziDict:
    def __init__(self):
        self.entries = dict()
        with open(chinese_path('hanzi_dict.csv'), newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.entries[row['Character']] = row
