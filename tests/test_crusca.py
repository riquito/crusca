# builtins
import unittest
from unittest.mock import patch
# ours
from src.crusca import create_app


class CruscaTests(unittest.TestCase):

    @patch('src.crusca.github_bp')
    def test_blueprint_loaded(self, github_bp_mock):
        app = create_app()
        registered_blueprints = list(app.blueprints.values())
        self.assertEqual(1, len(registered_blueprints))
        self.assertIs(github_bp_mock.blueprint, registered_blueprints[0])

