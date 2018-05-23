from flask import send_file

from HanziLevelUp.dir import database_path
from webapp import app


@app.route('/getLevels', methods=['POST'])
def get_levels():
    return send_file(database_path('hanzi_level.txt'))
