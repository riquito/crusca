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

    def setUp(self):
        self.picky_reader_patcher = patch('src.github_bp.reader')
        self.github_client_patcher = patch('src.github_client.GithubClient')

        self.picky_reader_mock = self.picky_reader_patcher.start()
        self.github_client_cls_mock = self.github_client_patcher.start()
        self.github_client_mock = self.github_client_cls_mock.return_value

        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['RULES'] = {'rule_name_x': 'conf'}
        self.app.config['AUTH'] = {
            'baxterthehacker/public-repo': {
                'secret_key': 'the secret key',
                'auth_token': 'the oauth token'
            }
        }

        self.client = self.app.test_client()

        self.request_context = self.app.test_request_context()
        self.request_context.push()

    def tearDown(self):
        self.picky_reader_mock = self.picky_reader_patcher.stop()
        self.github_client_cls_mock = self.github_client_patcher.stop()
        self.request_context.pop()
        if hasattr(bp, 'config'):
            del(bp.config)

    def test_on_blueprint_loaded(self):
        self.app.register_blueprint(bp)

        self.picky_reader_mock.register.assert_called_once_with('rule_name_x', 'conf')
        self.assertTrue(hasattr(bp, 'config'))
        self.assertEqual(bp.config, self.app.config)

    def dpNotAllowedMethodsForPushAction(self):
        return [
            ['GET'],
            ['PUT'],
            ['DELETE']
        ]

        return app

    @provider('dpNotAllowedMethodsForPushAction')
    def test_push_action_accept_only_post_method(self, method):
        self.app.register_blueprint(bp)
        url = url_for('github_bp.push_action', _method='POST')
        res = self.client.open(url, method=method)
        self.assertEqual(405, res.status_code)

    def test_push_action_accept_post(self):
        self.app.register_blueprint(bp)
        url = url_for('github_bp.push_action', _method='POST')
        res = self.client.post(url)
        self.assertEqual(400, res.status_code)

    @fixtureFile('push_payload.json')
    def test_push_action_success(self, payload):
        self.app.register_blueprint(bp)
        json_payload = json.loads(payload)
        json_payload['commits'][0]['message'] = 'first line\n\nparagraph'
        payload = json.dumps(json_payload)

        url = url_for('github_bp.push_action', _method='POST')
        headers = {'X-Github-Event': 'push'}
        res = self.client.post(url, data=payload, headers=headers, content_type='application/json')
        self.assertEqual(200, res.status_code)
        self.assertEqual('application/json', res.headers.get('Content-Type'))
        self.assertEqual(b'{}', res.data)
        self.picky_reader_mock.read.assert_called_once_with('first line')

        owner = 'baxterthehacker'
        repo = 'public-repo'
        sha = '0d1a26e67d8f5eaf1f6ba5c57fc3c7d91ac0fd1c'
        state = 'success'
        desc = 'Crusca approved'

        self.github_client_cls_mock.assert_called_once_with('the oauth token')
        self.github_client_mock.set_status.assert_called_once_with(owner, repo, sha, state, desc)

    @fixtureFile('push_payload.json')
    def test_push_action_unacceptable_message(self, payload):
        self.app.register_blueprint(bp)
        url = url_for('github_bp.push_action', _method='POST')
        headers = {'X-Github-Event': 'push'}
        self.picky_reader_mock.read.side_effect = UnacceptableContentError('Boom')
        res = self.client.post(url, data=payload, headers=headers, content_type='application/json')
        self.assertEqual(200, res.status_code)
        self.assertEqual('application/json', res.headers.get('Content-Type'))
        self.assertEqual(b'{}', res.data)

        owner = 'baxterthehacker'
        repo = 'public-repo'
        sha = '0d1a26e67d8f5eaf1f6ba5c57fc3c7d91ac0fd1c'
        state = 'failure'
        desc = 'Boom'

        self.github_client_cls_mock.assert_called_once_with('the oauth token')
        self.github_client_mock.set_status.assert_called_once_with(owner, repo, sha, state, desc)

    @fixtureFile('push_payload.json')
    def test_push_action_return_400_on_missing_commits(self, payload):
        self.app.register_blueprint(bp)
        payload = json.loads(payload)
        payload.pop('commits')
        payload = json.dumps(payload)

        url = url_for('github_bp.push_action', _method='POST')
        headers = {'X-Github-Event': 'push'}
        res = self.client.post(url, data=payload, headers=headers, content_type='application/json')
        self.assertEqual(400, res.status_code)

    @fixtureFile('push_payload.json')
    def test_push_action_return_400_on_missing_commit_data(self, payload):
        self.app.register_blueprint(bp)
        payload = json.loads(payload)
        payload['commits'][0].pop('id')
        payload = json.dumps(payload)

        url = url_for('github_bp.push_action', _method='POST')
        headers = {'X-Github-Event': 'push'}
        res = self.client.post(url, data=payload, headers=headers, content_type='application/json')
        self.assertEqual(400, res.status_code)

    @fixtureFile('push_payload.json')
    def test_push_action_return_400_on_missing_repo(self, payload):
        self.app.register_blueprint(bp)
        payload = json.loads(payload)
        payload['repository'].pop('name')
        payload = json.dumps(payload)

        url = url_for('github_bp.push_action', _method='POST')
        headers = {'X-Github-Event': 'push'}
        res = self.client.post(url, data=payload, headers=headers, content_type='application/json')
        self.assertEqual(400, res.status_code)

    @fixtureFile('push_payload.json')
    def test_push_action_return_400_on_missing_owner(self, payload):
        self.app.register_blueprint(bp)
        payload = json.loads(payload)
        payload['repository']['owner'].pop('name')
        payload = json.dumps(payload)

        url = url_for('github_bp.push_action', _method='POST')
        headers = {'X-Github-Event': 'push'}
        res = self.client.post(url, data=payload, headers=headers, content_type='application/json')
        self.assertEqual(400, res.status_code)

    @fixtureFile('push_payload.json')
    def test_push_action_return_401_on_missing_config_secret_key(self, payload):
        self.app.register_blueprint(bp)
        bp.config['AUTH']['baxterthehacker/public-repo'].pop('secret_key')

        url = url_for('github_bp.push_action', _method='POST')
        headers = {'X-Github-Event': 'push'}
        res = self.client.post(url, data=payload, headers=headers, content_type='application/json')
        self.assertEqual(401, res.status_code)

    @fixtureFile('push_payload.json')
    def test_push_action_return_401_on_missing_config_auth_token(self, payload):
        self.app.register_blueprint(bp)
        bp.config['AUTH']['baxterthehacker/public-repo'].pop('auth_token')

        url = url_for('github_bp.push_action', _method='POST')
        headers = {'X-Github-Event': 'push'}
        res = self.client.post(url, data=payload, headers=headers, content_type='application/json')
        self.assertEqual(401, res.status_code)

    def test_status_action(self):
        self.app.register_blueprint(bp)
        url = url_for('github_bp.status_action')
        res = self.client.get(url)
        self.assertEqual(200, res.status_code)
        self.assertEqual(b'alive', res.data)
