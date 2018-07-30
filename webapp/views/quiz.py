from flask import request, jsonify, Response

from HanziLevelUp.quiz import create_search_engine, search
from webapp import app


@app.route('/post/quiz/index/<data_type>', methods=['POST'])
def quiz_index(data_type):
    create_search_engine(data_type)

    return Response(status=201)


@app.route('/post/quiz/read/<data_type>', methods=['POST'])
def quiz_read(data_type):
    def sorter(x):
        level = int(x.get('Level', -1))
        if level == 0:
            level = 101

        return level

    return jsonify(sorted(search(data_type,
                                 search_query=request.form.get('search'),
                                 level=request.form.get('level'),
                                 created=request.form.get('created')),
                          key=sorter))
