# builtins
import unittest
# third parties
from flask import url_for
# ours
from src.crusca import create_app
from .decorators import provider, fixtureFile


class CruscaTests(unittest.TestCase):
    FIXTURES_DIR = 'fixtures/'

    def setUp(self):
        app = create_app()

        # propagate the exceptions to the test client
        app.config['TESTING'] = True

        # creates a test client
        self.client = app.test_client()

        # enter the current request's context
        self.ctx = app.test_request_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def dpNotAllowedMethodsForPushAction(self):
        return [
            ['GET'],
            ['PUT'],
            ['DELETE']
        ]

    @provider('dpNotAllowedMethodsForPushAction')
    def test_push_action_accept_only_post_method(self, method):
        url = url_for('github_bp.push_action', _method='POST')
        res = self.client.open(url, method=method)
        self.assertEqual(405, res.status_code)

    def test_push_action_accept_post(self):
        url = url_for('github_bp.push_action', _method='POST')
        res = self.client.post(url)
        self.assertEqual(400, res.status_code)

    @fixtureFile('push_payload.json')
    def test_push_action(self, payload):
        url = url_for('github_bp.push_action', _method='POST')
        headers = {'X-Github-Event': 'push'}
        res = self.client.post(url, data=payload, headers=headers)
        self.assertEqual(200, res.status_code)
        self.assertEqual('application/json', res.headers.get('Content-Type'))
        self.assertEqual(b'{}', res.data)
