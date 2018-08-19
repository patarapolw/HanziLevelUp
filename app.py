#!/usr/bin/env python

import os

from webapp import app, db
from webapp.config import database_url

if __name__ == '__main__':
    if not os.path.exists(database_url()):
        db.create_all()

    app.run(
        host='localhost',
        # host='192.168.1.13',
        port=8080,
        debug=True,
        # ssl_context='adhoc',
        # ssl_context=('cert.pem', 'key.pem'),
    )
