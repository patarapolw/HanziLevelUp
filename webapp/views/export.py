from flask import send_from_directory

from HanziLevelUp.excel import ExcelExport

from webapp import app


@app.route('/post/export/<export_type>', methods=['POST'])
def do_export(export_type):
    if export_type == 'excel':
        ExcelExport('user/HanziLevelUp.xlsx').from_db()
        return '1'

    return '0'


@app.route('/get/export/<filename>')
def download_export(filename):
    return send_from_directory('../user', filename, as_attachment=True)
