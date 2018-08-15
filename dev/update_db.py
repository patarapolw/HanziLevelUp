from datetime import datetime
import json
import regex

from webapp.databases import Hanzi, Vocab, Sentence
from webapp import db

from CJKhyperradicals.sentence import SpoonFed
from CJKhyperradicals.dict import HanziDict, Cedict
from CJKhyperradicals.decompose import Decompose
from CJKhyperradicals.frequency import ChineseFrequency
from HanziLevelUp.hanzi import HanziLevel
from HanziLevelUp.vocab import VocabToSentence

spoon_fed = SpoonFed()
hanzi_level = HanziLevel()
cedict = Cedict()
hanzi_dict = HanziDict()
vocab_to_sentence = VocabToSentence()
decompose = Decompose()
sorter = ChineseFrequency()


def get_earliest_modified(hanzi):
    sentence = Sentence.query.filter(Sentence.sentence.like('%{}%'.format(hanzi))).first()
    vocab = Vocab.query.filter(Vocab.vocab.like('%{}%'.format(hanzi))).first()

    if sentence is None:
        if vocab is None:
            return datetime.now()
        else:
            return vocab.modified
    elif vocab is None:
        return sentence.modified
    elif sentence.modified < vocab.modified:
        return sentence.modified
    else:
        return vocab.modified


if __name__ == '__main__':
    # for record in Hanzi.query:
        # data = json.loads(record.data)
        # data['level'] = hanzi_level.get_hanzi_level(record.hanzi)
        # data['dictionary'] = hanzi_dict.entries.get(record.hanzi, dict())
        # record.data = json.dumps(data, ensure_ascii=False)

        # record.back = '%(data)s'

    # for record in Vocab.query:
        # data = json.loads(record.data)
        # if len(data['dictionary']) > 0:
        #     record.front = ', '.join([item['english'] for item in data['dictionary']])
        # else:
        #     record.front = '%(data[0].pinyin)s'
        # print(record.data)

        # record.back = '%(data)s'
        # break

    for record in Sentence.query:
        # record.front = '%(sentence)s'
        # record.back = '%(data)s'
        # print(record.data)
        # break
        lookup = list(spoon_fed.get_sentence(record.sentence))
        if len(lookup) > 0:
            english = lookup[0]['english']
            try:
                pinyin = lookup[0]['pinyin']
            except IndexError:
                pinyin = ''
        else:
            english = pinyin = ''

        record.data = json.dumps({
            'pinyin': pinyin,
            'english': english,
            'levels': [hanzi_level.get_hanzi_level(char) for char in record.sentence if
                       regex.match(r'\p{IsHan}', char)]
        }, ensure_ascii=False)

    db.session.commit()
