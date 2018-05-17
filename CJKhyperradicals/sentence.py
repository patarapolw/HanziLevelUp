import requests
from bs4 import BeautifulSoup

from CJKhyperradicals.dir import chinese_path


def jukuu(vocab):
    params = {
        'q': vocab
    }
    r = requests.get('http://www.jukuu.com/search.php', params=params)
    soup = BeautifulSoup(r.text, 'html.parser')

    return zip([c.text for c in soup.find_all('tr', {'class': 'c'})],
               [e.text for e in soup.find_all('tr', {'class': 'e'})])


class SpoonFed:
    def __init__(self):
        self.sentences = list()
        with open(chinese_path('SpoonFed.tsv')) as f:
            for row in f:
                contents = row.split('\t')
                self.sentences.append((contents[2], contents[0]))

    def get_sentence(self, vocab):
        for sentence in self.sentences:
            if vocab in sentence[0]:
                yield sentence
