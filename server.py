import os
import datetime
from github_status import GithubStatus

from dateutil import rrule
import requests
import lxml.html
from flask import Flask, jsonify, redirect
from flask.ext.cache import Cache

app = Flask(__name__)
status = GithubStatus()
cache = Cache(app)

@app.route('/')
def home():
    return ("/hour/minute return a dict for geckoboard" 
           "/github for more on github")

@app.route('/<int:hour>/<int:minute>')
def hour(hour, minute):
    t = datetime.datetime(2013, 1, 1, hour, minute, 0, 0)
    r = rrule.rrule(rrule.DAILY, t)
    dt = r.after(datetime.datetime.now()) - datetime.datetime.now()
    return jsonify( { 'item':[{ 'value':dt.seconds//3600, 'text':'hours'},
                    { 'value':(dt.seconds//60)%60, 'text':'minutes'}]})

@app.route('/github/')
def github():
    """Documentation for the github view
    """
    return "/github/status for status (up or down)\n/github/messages for detailed message"

@app.route('/github/status')
@cache.cached(timeout=120)
def github_status():
    """Return a geckoboard compatible message containing the status of github services
    """
    return jsonify(status.status)

@app.route('/github/messages')
@cache.cached(timeout=120)
def github_msg():
    """Return a geckoboard compatible message list send on github status
    """
    return jsonify(status.message)

@app.route('/xkcd')
@cache.cached(timeout=900)
def xkcd():
    """Return the latest xkcd comic. It will redirect the request to the image url.
    """
    xkcd_page = requests.get('http://xkcd.com').content
    html = lxml.html.fromstring(xkcd_page)
    return redirect(html.xpath('//div[@id="comic"]/img/@src')[0])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
