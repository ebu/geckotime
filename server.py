import os
from flask import Flask, jsonify
from dateutil import rrule
import datetime
import requests
from collections import defaultdict
import logging

app = Flask(__name__)
API_JSON = ""

class GithubStatus():
    BASE_URL = "https://status.github.com/api.json"
    STATUS_TRANSLATE = defaultdict(good='Up')
    def __init__(self):
        logging.msg("fetching the base url for github status")
        _, _, self.last_message_url = requests.get(GithubStatus.BASE_URL).json()


    @property
    def json(self):
        last_message = requests.get(self.last_message_url).json()
        last_message['status'] = GithubStatus.STATUS_TRANSLATE[last_message['status']]
        return {'status':'up', 'responseTime':last_message['message']}

status = GithubStatus()

@app.route('/')
def home():
    return "/hour/minute return a dict for geckoboard"

@app.route('/to/<int:hour>/<int:minute>')
def hour(hour, minute):
    t = datetime.datetime(2013, 1, 1, hour, minute, 0, 0)
    r = rrule.rrule(rrule.DAILY, t)
    dt = r.after(datetime.datetime.now()) - datetime.datetime.now()
    return jsonify({'item':[{'value':dt.seconds//3600, 'description':'hours'},{'value':(dt.seconds//60)%60, 'description':'minutes'}]})

@app.route('/github')
def github():
    return status.json

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
