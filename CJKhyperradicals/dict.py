import regex

from CJKhyperradicals.dir import chinese_path


class Cedict:
    def __init__(self):
        self.entries = set()
        with open(chinese_path('cedict_ts.u8')) as f:
            for row in f:
                _ = regex.match(r'([^ ]+) ([^ ]+) \[(.+)\] /(.+)/', row)
                if _ is not None:
                    # trad, simp, pinyin, english = _.groups()
                    self.entries.add(_.groups())
                else:
                    # print(row)
                    pass

    def search_hanzi(self, hanzi):
        for entry in self.entries:
            if hanzi in (entry[0] + entry[1]):
                yield entry

    def search_vocab(self, vocab):
        for entry in self.entries:
            if (vocab in (entry[0], entry[1])
                    or vocab in regex.findall('[^\p{IsHan}\p{InCJK_Radicals_Supplement}\p{InKangxi_Radicals}\W]+',
                                              entry[3])):
                yield entry
