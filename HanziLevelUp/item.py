from zipfile import ZipFile
import os

from HanziLevelUp.vocab import vocab_to_csv
from HanziLevelUp.sentence import sentence_to_csv


def db_to_csv():
    vocab_to_csv()
    sentence_to_csv()

    with ZipFile(os.path.join('tmp', 'Chinese.zip'), 'w') as zipfile:
        zipfile.write(os.path.join('tmp', 'vocab.csv'), arcname='vocab.csv')
        zipfile.write(os.path.join('tmp', 'sentence.csv'), arcname='sentence.csv')
