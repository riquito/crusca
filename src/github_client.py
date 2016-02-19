# third parties
import requests

STATE_SUCCESS = 'success'
STATE_FAILURE = 'failure'
STATE_PENDING = 'pending'
STATE_ERROR = 'error'

CONTEXT = 'crusca'


class GithubClient:

    def __init__(self, authtoken):
        self.authtoken = authtoken

    def set_status(self, owner, repo, sha, state, description):
        url_format = 'https://api.github.com/repos/{owner}/{repo}/statuses/{sha}'
        url = url_format.format(owner=owner, repo=repo, sha=sha)

        requests.post(url, headers={
            'Authorization': 'token ' + self.authtoken,
        }, json={
            'context': CONTEXT,
            'state': state,
            'description': description
        })
