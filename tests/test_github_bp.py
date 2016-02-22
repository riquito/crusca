# builtins
import unittest
from unittest.mock import patch, Mock
import json
# third parties
from flask import Flask, url_for
# ours
from src.github_bp import blueprint as bp
from .decorators import provider, fixtureFile
from src.rules import UnacceptableContentError


class GithubBPTests(unittest.TestCase):
    FIXTURES_DIR = 'fixtures/'

    @patch('src.github_bp.reader')
    @patch('src.github_client.GithubClient')
    def test_on_blueprint_loaded(self, github_client_class_mock, picky_reader_mock):
        app = Flask(__name__)
        app.config['RULES'] = {'rule_name_x':'conf'}
        app.config['AUTH_TOKEN'] = 'secrettest'
        app.register_blueprint(bp)
        picky_reader_mock.register.assert_called_once_with('rule_name_x', 'conf')
        github_client_class_mock.assert_called_once_with('secrettest')

    def dpNotAllowedMethodsForPushAction(self):
        return [
            ['GET'],
            ['PUT'],
            ['DELETE']
        ]

    @patch('src.github_bp.reader')
    @patch('src.github_client.GithubClient')
    def _get_test_app(self, github_client_class_mock, picky_reader_mock):
        app = Flask(__name__)
        app.config['RULES'] = {'rule_name_x':'conf'}
        app.config['AUTH_TOKEN'] = 'secrettest'
        app.config['TESTING'] = True
        app.register_blueprint(bp)
        return app


    @provider('dpNotAllowedMethodsForPushAction')
    def test_push_action_accept_only_post_method(self, method):
        app = self._get_test_app()
        client = app.test_client()
        with app.test_request_context():
            url = url_for('github_bp.push_action', _method='POST')
            res = client.open(url, method=method)
            self.assertEqual(405, res.status_code)

    def test_push_action_accept_post(self):
        app = self._get_test_app()
        app.register_blueprint(bp)
        client = app.test_client()
        with app.test_request_context():
            url = url_for('github_bp.push_action', _method='POST')
            res = client.post(url)
            self.assertEqual(400, res.status_code)

    @patch('src.github_bp.reader')
    @fixtureFile('push_payload.json')
    def test_push_action_success(self, payload, reader_mock):
        app = self._get_test_app()
        app.register_blueprint(bp)
        client = app.test_client()
        json_payload = json.loads(payload)
        json_payload['commits'][0]['message'] = 'first line\n\nparagraph'
        payload = json.dumps(json_payload)

        with app.test_request_context():
            url = url_for('github_bp.push_action', _method='POST')
            headers = {'X-Github-Event': 'push'}
            res = client.post(url, data=payload, headers=headers, content_type='application/json')
            self.assertEqual(200, res.status_code)
            self.assertEqual('application/json', res.headers.get('Content-Type'))
            self.assertEqual(b'{}', res.data)
            reader_mock.read.assert_called_once_with('first line')

            owner = 'baxterthehacker'
            repo = 'public-repo'
            sha = '0d1a26e67d8f5eaf1f6ba5c57fc3c7d91ac0fd1c'
            state = 'success'
            desc = 'Crusca approved'
            bp.client.set_status.assert_called_once_with(owner, repo, sha, state, desc)

    @patch('src.github_bp.reader')
    @fixtureFile('push_payload.json')
    def test_push_action_unacceptable_message(self, payload, reader_mock):
        app = self._get_test_app()
        app.register_blueprint(bp)
        client = app.test_client()
        with app.test_request_context():
            url = url_for('github_bp.push_action', _method='POST')
            headers = {'X-Github-Event': 'push'}
            reader_mock.read.side_effect = UnacceptableContentError('Boom')
            res = client.post(url, data=payload, headers=headers, content_type='application/json')
            self.assertEqual(200, res.status_code)
            self.assertEqual('application/json', res.headers.get('Content-Type'))
            self.assertEqual(b'{}', res.data)
            
            owner = 'baxterthehacker'
            repo = 'public-repo'
            sha = '0d1a26e67d8f5eaf1f6ba5c57fc3c7d91ac0fd1c'
            state = 'failure'
            desc = 'Boom'
            bp.client.set_status.assert_called_once_with(owner, repo, sha, state, desc)

    @fixtureFile('push_payload.json')
    def test_push_action_return_400_on_missing_commits(self, payload):
        app = self._get_test_app()
        app.register_blueprint(bp)
        client = app.test_client()
        with app.test_request_context():
            payload = json.loads(payload)
            payload.pop('commits')
            payload = json.dumps(payload)

            url = url_for('github_bp.push_action', _method='POST')
            headers = {'X-Github-Event': 'push'}
            res = client.post(url, data=payload, headers=headers, content_type='application/json')
            self.assertEqual(400, res.status_code)

    @fixtureFile('push_payload.json')
    def test_push_action_return_400_on_missing_commit_data(self, payload):
        app = self._get_test_app()
        app.register_blueprint(bp)
        client = app.test_client()
        with app.test_request_context():
            payload = json.loads(payload)
            payload['commits'][0].pop('id')
            payload = json.dumps(payload)

            url = url_for('github_bp.push_action', _method='POST')
            headers = {'X-Github-Event': 'push'}
            res = client.post(url, data=payload, headers=headers, content_type='application/json')
            self.assertEqual(400, res.status_code)

    def test_status_action(self):
        app = self._get_test_app()
        app.register_blueprint(bp)
        client = app.test_client()
        with app.test_request_context():
            url = url_for('github_bp.status_action')
            res = client.get(url)
            self.assertEqual(200, res.status_code)
            self.assertEqual(b'alive', res.data)

