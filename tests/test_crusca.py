# builtins
import unittest
from unittest.mock import patch, mock_open, Mock
import builtins
# ours
from src.crusca import create_app, get_yaml_config, main
import src.crusca


class CruscaTests(unittest.TestCase):

    @patch('src.crusca.github_bp')
    def test_blueprint_loaded(self, github_bp_mock):
        app = create_app()
        registered_blueprints = list(app.blueprints.values())
        self.assertEqual(1, len(registered_blueprints))
        self.assertIs(github_bp_mock.blueprint, registered_blueprints[0])

    @patch('src.crusca.yaml')
    def test_get_yaml_config(self, yaml_mock):
        data = ''
        with patch.object(src.crusca,'open', mock_open(read_data=data), create=True) as mo:
            fp_mock = mo()
            yaml_mock.load.return_value = {'ENV_NAME':{'FOO':'bar'}}
            config = get_yaml_config('path_xyz','env_name')
            mo.assert_called_with('path_xyz')
            yaml_mock.load.assert_called_once_with(fp_mock)
            self.assertEqual({'FOO':'bar', 'ENVIRONMENT':'ENV_NAME'}, config)

    @patch('src.crusca.os.path.realpath')
    @patch('src.crusca.get_yaml_config')
    @patch('src.crusca.create_app')
    def test_main(self, create_app_mock, get_yaml_config_mock, os_path_realpath_mock):
        os_path_realpath_mock.return_value = '/a/b/c/foo.py'
        get_yaml_config_mock.return_value = {'x':1}
        app_mock = Mock()
        create_app_mock.return_value = app_mock
        main()
        get_yaml_config_mock.assert_called_once_with('/a/b/c/../config/config.yml', 'DEVELOPMENT')
        create_app_mock.assert_called_once_with({'x':1})
        app_mock.run.assert_called_once()

