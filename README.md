# Hanzi LevelUp

A Hanzi learning suite, with levels based on [Hanzi Level Project](https://hanzilevelproject.blogspot.com), aka. another attempt to clone [WaniKani.com](https://www.wanikani.com) for Chinese.

## Features

- Speak sentences and vocabularies when clicked on. (Tested on Mac OSX)
    - May need to be modified to [google_speech](https://pypi.org/project/google_speech/) if you want it spoken on non-mac.
- Show Hanzi decomposition and super-decomposition (powered by [CJKhyperradicals](http://cjkhyperradicals.herokuapp.com/)).
- 60 major Hanzi levels -- learn or review in each levels, based on [Hanzi Level Project](https://hanzilevelproject.blogspot.com).
- Breakdown sentences into vocab, for learning, with audio -- powered by [jieba](https://github.com/fxsjy/jieba).

## Installation and Get-it-running

- Install [Python](https://www.python.org/downloads/) first, if you don't have one.
- Clone the project from GitHub.
- Change the directory to the project folder, in the terminal and create a virtual environment.
- Install [poetry](https://github.com/sdispater/poetry), and run `poetry install`.
- Create the database: run
```commandline
$ flask db init
$ flask db migrate -m "sentences table"
$ flask db upgrade
```

- Run `app.py`.
- Go to `https://localhost:8080` on your browser.

## Screenshots

<img src="https://raw.githubusercontent.com/patarapolw/HanziLevelUp/master/screenshots/home.png">
<img src="https://raw.githubusercontent.com/patarapolw/HanziLevelUp/master/screenshots/learnSentence.png">
<img src="https://raw.githubusercontent.com/patarapolw/HanziLevelUp/master/screenshots/viewHanzi.png">
<img src="https://raw.githubusercontent.com/patarapolw/HanziLevelUp/master/screenshots/learnVocab.png">
<img src="https://raw.githubusercontent.com/patarapolw/HanziLevelUp/master/screenshots/viewVocab.png">
<img src="https://raw.githubusercontent.com/patarapolw/HanziLevelUp/master/screenshots/progress.png">
<img src="https://raw.githubusercontent.com/patarapolw/HanziLevelUp/master/screenshots/reviewLevel.png">

## Related Projects

- [CJKhyperradicals](https://github.com/patarapolw/CJKhyperradicals)
- [ChineseViewer](https://github.com/patarapolw/ChineseViewer)
