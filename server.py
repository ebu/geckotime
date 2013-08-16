import os
import datetime
import logging

from dateutil import rrule
import requests
import lxml.html
from flask import Flask, jsonify, redirect

app = Flask(__name__)
API_JSON = ""

class GithubStatus():
    BASE_URL = "https://status.github.com/api.json"


    def __init__(self):
        logging.info("fetching the base url for github status")
        _, self.messages_url, self.last_message_url = requests.get(GithubStatus.BASE_URL).json().values()


    @property
    def status(self):
        last_message = requests.get(self.last_message_url).json()
        if last_message['status'] == 'good':
            status = 'Up'
        else:
            status = 'Down'

        return {'status':status}

    @property
    def message(self):
        messages = requests.get(self.messages_url).json()
        out = []
        for m in messages:
            logging.info(m)
            summary = {}
            if m['status'] == 'good':
               summary['type'] = 0
            elif m['status'] == 'minor':
               summary['type'] = 1
            else:
               summary['type'] = 2
            t = m['created_on']
            summary['text'] = m['body'] + "\n" + t.replace('T', ' ').replace('Z', '')
            out.append(summary)
        logging.log(out)
        return {'item':out}

status = GithubStatus()

@app.route('/')
def home():
    return "/hour/minute return a dict for geckoboard\n/github for more on github"

@app.route('/<int:hour>/<int:minute>')
def hour(hour, minute):
    t = datetime.datetime(2013, 1, 1, hour, minute, 0, 0)
    r = rrule.rrule(rrule.DAILY, t)
    dt = r.after(datetime.datetime.now()) - datetime.datetime.now()
    return jsonify({'item':[{'value':dt.seconds//3600, 'text':'hours'},{'value':(dt.seconds//60)%60, 'text':'minutes'}]})

@app.route('/github/')
def github():
    return "/github/status for status (up or down)\n/github/messages for detailed message"

@app.route('/github/status')
def github_status():
    return jsonify(status.status)

@app.route('/github/messages')
def github_msg():
    return jsonify(status.message)

@app.route('/xkcd')
def xkcd():
    xkcd_page = requests.get('http://xkcd.com').content
    html = lxml.html.fromstring(xkcd_page)
    return redirect(html.xpath('//div[@id="comic"]/img/@src')[0])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
