import os
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EN\">\n\
            <HTML>\n\
            <HEAD><TITLE>Python on cloudControl</TITLE></HEAD>\n\
            <BODY>\n\
            <center><h1>Hello World!</h1></center>\n\
            </BODY>\n\
            </HTML>"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
