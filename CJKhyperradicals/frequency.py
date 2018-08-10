import math
import csv
from wordfreq import word_frequency

from CJKhyperradicals.dir import chinese_path


class ChineseFrequency:
    def __init__(self):
        self.sequence = []
        with open(chinese_path('junda.tsv')) as f:
            reader = csv.DictReader(f, delimiter='\t')
            for entry in reader:
                self.sequence.append(entry['character'])

    def sort_char(self, hanzi_list, limit=5000):
        return sorted([hanzi for hanzi in hanzi_list if self.freq_char(hanzi) <= limit], key=self.freq_char)

    def freq_char(self, hanzi):
        try:
            return self.sequence.index(hanzi)
        except ValueError:
            return math.inf

    def sort_vocab(self, vocab_dict_list):
        return sorted([vocab_dict for vocab_dict in vocab_dict_list],
                      key=lambda vocab_dict : self.freq_vocab(vocab_dict['simplified']), reverse=True)

    @staticmethod
    def freq_vocab(vocab):
        return word_frequency(vocab, 'zh')
