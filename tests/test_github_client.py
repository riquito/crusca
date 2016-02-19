# builtins
import unittest
from unittest.mock import patch
# ours
from src.github_client import GithubClient, STATE_SUCCESS


class GithubClientTests(unittest.TestCase):

    def test_constructor(self):
        token = 'foo'
        client = GithubClient(token)
        self.assertEqual(token, client.authtoken)
        
    @patch('src.github_client.requests')
    def test_set_status(self, requests_mock):
        token = 'foo'
        owner = 'owner-name'
        repo = 'repo-name'
        sha = 'abc123'
        state = STATE_SUCCESS
        desc = 'some desc'

        client = GithubClient(token)
        client.set_status(owner, repo, sha, state, desc)

        requests_mock.post.assert_called_once_with(
            'https://api.github.com/repos/owner-name/repo-name/statuses/abc123',
            headers = { 'Authorization': 'token foo' },
            json = { 'context': 'crusca', 'state': state, 'description': desc}
        )
