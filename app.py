import os

from webapp.views import app

if __name__ == '__main__':
    if 'DYNO' in os.environ:
       app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))
    else:
       app.run(host='localhost', port=8080, debug=True)
