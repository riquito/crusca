# builtins
import unittest
from unittest.mock import patch, mock_open, Mock
import builtins
# ours
from src.crusca import create_app, config_lib, main
import src.crusca


class CruscaTests(unittest.TestCase):

    @patch('src.crusca.github_bp')
    def test_blueprint_loaded(self, github_bp_mock):
        app = create_app()
        registered_blueprints = list(app.blueprints.values())
        self.assertEqual(1, len(registered_blueprints))
        self.assertIs(github_bp_mock.blueprint, registered_blueprints[0])

    @patch('src.crusca.os.path.realpath')
    @patch('src.crusca.config_lib')
    @patch('src.crusca.create_app')
    def test_main(self, create_app_mock, config_lib_mock, os_path_realpath_mock):
        os_path_realpath_mock.return_value = '/a/b/c/foo.py'
        config_lib_mock.get_config.return_value = {'x':1}
        app_mock = Mock()
        create_app_mock.return_value = app_mock
        res = main()
        config_lib_mock.get_config.assert_called_once_with('/a/b/c/../config/config.yml', 'DEVELOPMENT')
        create_app_mock.assert_called_once_with({'x':1})
        self.assertIs(app_mock, res)

