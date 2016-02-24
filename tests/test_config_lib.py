# builtins
import os
import unittest
from unittest.mock import patch, mock_open, Mock
# ours
from .decorators import provider
from src.config_lib import get_config, ConfigError
import src.config_lib


class ConfigLibTests(unittest.TestCase):

    def setUp(self):
        self.open_patcher = patch.object(src.config_lib, 'open', mock_open(read_data=''), create=True)
        self.yaml_patcher = patch('src.config_lib.yaml')

        self.open_mock = self.open_patcher.start()
        self.yaml_mock = self.yaml_patcher.start()

        self.fp_mock = self.open_mock()

        self.base_config = {
            'RULES': {'capital_letter': None},
            'AUTH': {
                'riquito/crusca': {
                    'secret_key': 'foo',
                    'auth_token': 'bar'
                },
                'riquito/valib': {
                    'secret_key': 'baz',
                    'auth_token': 'ram'
                }
            }
        }

        if os.environ.get('CRUSCA_OWNERS_REPOS'):
            del(os.environ['CRUSCA_OWNERS_REPOS'])

        for key in list(os.environ.keys()):
            if key.startswith('CRUSCA_SECRET_KEY') or \
               key.startswith('CRUSCA_AUTH_TOKEN'):
                del(os.environ[key])

    def tearDown(self):
        self.open_patcher.stop()
        self.yaml_patcher.stop()

    def test_get_config_file_only_success(self):
        self.yaml_mock.load.return_value = self.base_config

        config = get_config('path_xyz', 'env_name')

        self.open_mock.assert_called_with('path_xyz')
        self.yaml_mock.load.assert_called_once_with(self.fp_mock)

        expected = {'ENVIRONMENT': 'ENV_NAME'}
        expected.update(self.base_config)
        self.assertEqual(expected, config)

    def test_get_config_file_only_root_env_success(self):
        self.yaml_mock.load.return_value = {'ENV_NAME': self.base_config}

        config = get_config('path_xyz', 'env_name')

        self.open_mock.assert_called_with('path_xyz')
        self.yaml_mock.load.assert_called_once_with(self.fp_mock)

        expected = {'ENVIRONMENT': 'ENV_NAME'}
        expected.update(self.base_config)
        self.assertEqual(expected, config)

    def test_get_config_file_env_variables(self):
        self.yaml_mock.load.return_value = {
            'RULES': {'capital_letter': None}
        }

        os.environ['CRUSCA_OWNERS_REPOS'] = 'riquito/crusca;riquito/valib'
        os.environ['CRUSCA_SECRET_KEY_RIQUITO_CRUSCA'] = 'foo'
        os.environ['CRUSCA_AUTH_TOKEN_RIQUITO_CRUSCA'] = 'bar'
        os.environ['CRUSCA_SECRET_KEY_RIQUITO_VALIB'] = 'baz'
        os.environ['CRUSCA_AUTH_TOKEN_RIQUITO_VALIB'] = 'ram'

        config = get_config('path_xyz', 'env_name')

        self.open_mock.assert_called_with('path_xyz')
        self.yaml_mock.load.assert_called_once_with(self.fp_mock)

        expected = {'ENVIRONMENT': 'ENV_NAME'}
        expected.update(self.base_config)
        self.assertEqual(expected, config)

    def dp_get_config_file_only_required_keys_failure(self):
        return [
            ('AUTH', True),
            ('AUTH', False),
            ('RULES', True),
            ('RULES', False)
        ]

    @provider('dp_get_config_file_only_required_keys_failure')
    def test_get_config_file_only_required_keys_failure(self, key, exists_but_empty):
        conf = {}
        conf.update(self.base_config)

        if exists_but_empty:
            conf[key] = None
        else:
            conf.pop(key)

        self.yaml_mock.load.return_value = conf

        expected = {'ENVIRONMENT': 'ENV_NAME'}
        expected.update(self.base_config)
        self.assertRaises(ConfigError, get_config, 'path_xyz', 'env_name')
