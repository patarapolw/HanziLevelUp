import requests
from bs4 import BeautifulSoup


def jukuu(vocab):
    params = {
        'q': vocab
    }
    r = requests.get('http://www.jukuu.com/search.php', params=params)
    soup = BeautifulSoup(r.text, 'html.parser')

    return zip([c.text for c in soup.find_all('tr', {'class': 'c'})],
               [e.text for e in soup.find_all('tr', {'class': 'e'})])
