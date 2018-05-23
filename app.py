#!/usr/bin/env python

from webapp.views import app

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
