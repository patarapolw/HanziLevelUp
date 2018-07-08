from flask import request, send_from_directory

from HanziLevelUp.item import db_to_csv

from webapp import app


# @app.route('/post/export/<export_type>', methods=['POST'])
# def do_export(export_type):
#     if request.method == 'POST':
#         if export_type == 'csv':
#             db_to_csv()
#             return '1'
#
#     return '0'
#
#
# @app.route('/get/export/<filename>')
# def download_export(filename):
#     return send_from_directory('../tmp', filename, as_attachment=True)
