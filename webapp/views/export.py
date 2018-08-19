from flask import send_from_directory, Response

from HanziLevelUp.excel import export_excel

from webapp import app


@app.route('/post/export/<export_type>', methods=['POST'])
def do_export(export_type):
    if export_type == 'excel':
        export_excel()
        return Response(status=201)

    return Response(status=304)


@app.route('/get/export/<filename>')
def download_export(filename):
    return send_from_directory('../user', filename, as_attachment=True)
