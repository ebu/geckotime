import os
from flask import Flask, jsonify
from dateutil import rrule
import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return "/hour/minute return a dict"

@app.route('/<int:hour>/<int:minute>')
def hour(hour, minute):
    t = datetime.datetime(2013, 1, 1, hour, minute, 0, 0)
    r = rrule.rrule(rrule.DAILY, t)
    dt = r.after(datetime.datetime.now()) - datetime.datetime.now()
    return jsonify({'item':[{'value':dt.seconds//3600, 'description':'hours'},{'value':(dt.seconds//60)%60, 'description':'minutes'}]})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
