from flask import send_from_directory

from webapp import app


@app.route('/getLevels', methods=['POST'])
def get_levels():
    return send_from_directory('static', 'hanzilevel.txt')
