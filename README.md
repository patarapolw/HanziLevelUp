# Hanzi LevelUp

A Hanzi learning suite, with levels based on [Hanzi Level Project](https://hanzilevelproject.blogspot.com), aka. another attempt to clone [WaniKani.com](https://www.wanikani.com) for Chinese.

## Features

- Speak sentences and vocabularies when clicked on. (Tested on Mac OSX)
    - May need to be modified to [google_speech](https://pypi.org/project/google_speech/) if you want it spoken on non-mac.
- Show Hanzi decomposition and super-decomposition (powered by [CJKhyperradicals](http://cjkhyperradicals.herokuapp.com/)).
- 60 major Hanzi levels -- learn or review in each levels, based on [Hanzi Level Project](https://hanzilevelproject.blogspot.com).
- Breakdown sentences into vocab, for learning, with audio -- powered by [jieba](https://github.com/fxsjy/jieba).
- Export to Excel file.
- SRS (Spaced-repetition system) is now possible via Jupyter Notebook.

## Installation and Get-it-running

- Install [Python](https://www.python.org/downloads/) first, if you don't have one.
- Clone the project from GitHub.
- Change the directory to the project folder, in the terminal and create a virtual environment.
- Install [poetry](https://github.com/sdispater/poetry), and run `poetry install`.
- Run `app.py`.
- Go to `https://localhost:8080` on your browser.

## Activating the SRS

The app server has to be running first. In Jupyter Notebook:

```python
>>> from webapp.databases import Vocab
>>> from webapp import db
>>> iter_quiz = Vocab.iter_quiz(tag='col1', is_due=True)
>>> card = next(iter_quiz)
>>> card.hide()
A HTML-rendered front of the card is shown.
>>> card.show()
A HTML-rendered back of the card is shown.
>>> card.get_more_sentences()
Add more sentences to the card, if the number of example sentences is too few.
>>> card.wrong()
Mark the card as wrong.
>>> card.right()
Mark the card as right.
>>> card.mark()
Add the tag "marked" to the card.
>>> card.unmark()
Remove the tag "marked" from the card.
>>> db.session.commit()
Commit changes.
```

## Screenshots

<img src="https://raw.githubusercontent.com/patarapolw/HanziLevelUp/master/screenshots/learnSentence.png">
<img src="https://raw.githubusercontent.com/patarapolw/HanziLevelUp/master/screenshots/viewHanzi.png">
<img src="https://raw.githubusercontent.com/patarapolw/HanziLevelUp/master/screenshots/learnVocab.png">
<img src="https://raw.githubusercontent.com/patarapolw/HanziLevelUp/master/screenshots/viewVocab.png">
<img src="https://raw.githubusercontent.com/patarapolw/HanziLevelUp/master/screenshots/clipboard.png">
<img src="https://raw.githubusercontent.com/patarapolw/HanziLevelUp/master/screenshots/progress.png">
<img src="https://raw.githubusercontent.com/patarapolw/HanziLevelUp/master/screenshots/reviewLevel.png">
<img src="https://raw.githubusercontent.com/patarapolw/HanziLevelUp/master/screenshots/editor.png">
<img src="https://raw.githubusercontent.com/patarapolw/HanziLevelUp/master/screenshots/jupyter.png">

## Related Projects

- [ChineseViewer](https://github.com/patarapolw/ChineseViewer)
- [CJKhyperradicals](https://github.com/patarapolw/CJKhyperradicals)
