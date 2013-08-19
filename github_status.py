import requests
"""Module implementing a basic github status api
"""

class GithubStatus():
    """Class wrapping github status api
    """

    BASE_URL = "https://status.github.com/api.json"

    def __init__(self):
        """Init the github status api, fetch the url used later.
        """
        urls = requests.get(GithubStatus.BASE_URL).json()
        self.status_url = urls['status_url']
        self.messages_url = urls['messages_url']

    @property
    def status(self):
        """Return the github status.
        """
        last_message = requests.get(self.status_url).json()
        if last_message['status'] == 'good':
            status = 'Up'
        else:
            status = 'Down'

        return {'status':status}

    @property
    def message(self):
        """Return a gecko board compatible list of messages posted on 
        github status blog
        """
        messages = requests.get(self.messages_url).json()
        out = []
        for m in messages:
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
        return {'item':out}
