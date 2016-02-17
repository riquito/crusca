# builtins
import unittest
# third parties
from flask import Flask, url_for
# ours
from src.github_bp import blueprint as bp
from .decorators import provider, fixtureFile


class GithubBPTests(unittest.TestCase):
    FIXTURES_DIR = 'fixtures/'

    def dpNotAllowedMethodsForPushAction(self):
        return [
            ['GET'],
            ['PUT'],
            ['DELETE']
        ]

    @provider('dpNotAllowedMethodsForPushAction')
    def test_push_action_accept_only_post_method(self, method):
        app = Flask(__name__)
        app.register_blueprint(bp)
        client = app.test_client()
        with app.test_request_context():
            url = url_for('github_bp.push_action', _method='POST')
            res = client.open(url, method=method)
            self.assertEqual(405, res.status_code)

    def test_push_action_accept_post(self):
        app = Flask(__name__)
        app.register_blueprint(bp)
        client = app.test_client()
        with app.test_request_context():
            url = url_for('github_bp.push_action', _method='POST')
            res = client.post(url)
            self.assertEqual(400, res.status_code)

    @fixtureFile('push_payload.json')
    def test_push_action(self, payload):
        app = Flask(__name__)
        app.register_blueprint(bp)
        client = app.test_client()
        with app.test_request_context():
            url = url_for('github_bp.push_action', _method='POST')
            headers = {'X-Github-Event': 'push'}
            res = client.post(url, data=payload, headers=headers)
            self.assertEqual(200, res.status_code)
            self.assertEqual('application/json', res.headers.get('Content-Type'))
            self.assertEqual(b'{}', res.data)

