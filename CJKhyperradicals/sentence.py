import requests
from bs4 import BeautifulSoup
import csv

from CJKhyperradicals.dir import chinese_path


def jukuu(vocab):
    params = {
        'q': vocab
    }
    r = requests.get('http://www.jukuu.com/search.php', params=params)
    soup = BeautifulSoup(r.text, 'html.parser')

    for c, e in zip([c.text for c in soup.find_all('tr', {'class': 'c'})],
                    [e.text for e in soup.find_all('tr', {'class': 'e'})]):
        yield {
            'sentence': c,
            'english': e
        }


class SpoonFed:
    def __init__(self):
        self.sentences = dict()
        with open(chinese_path('SpoonFed.tsv')) as f:
            reader = csv.DictReader(f, delimiter='\t')
            for i, entry in enumerate(reader):
                self.sentences[i] = entry

    def get_sentence(self, vocab):
        for sentence in self.sentences.values():
            if vocab in sentence['sentence']:
                yield sentence
