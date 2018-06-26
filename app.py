#!/usr/bin/env python

from webapp import app

if __name__ == '__main__':
    app.run(
        host='localhost',
        # host='192.168.1.13',
        port=8080,
        debug=True,
        # ssl_context='adhoc',
        ssl_context=('cert.pem', 'key.pem'),
    )
