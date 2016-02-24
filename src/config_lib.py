# builtins
import os
# third parties
import yaml

class ConfigError(Exception): pass

def get_config(path, environment):
    environment = environment.upper()

    with open(path) as fp:
        conf = yaml.load(fp)

    # either get a subconf or the whole conf
    conf = conf.get(environment, conf)
    conf['ENVIRONMENT'] = environment

    _get_config_from_env_vars(conf)

    config = {k: v for k, v in conf.items() if k.isupper()}
    _validate_config(config)

    return config

def _get_config_from_env_vars(conf):
    if os.environ.get('CRUSCA_OWNERS_REPOS'):
        owners_repos = os.environ['CRUSCA_OWNERS_REPOS'].split(';')
        conf['AUTH'] = {key:{} for key in owners_repos}
    else:
        owners_repos = (conf.get('AUTH') or {}).keys()

    for owner_repo in owners_repos:
        env_owner_repo = owner_repo.replace('/', '_').upper()

        try: 
            value = os.environ['CRUSCA_SECRET_KEY_' + env_owner_repo]
            conf['AUTH'][owner_repo]['secret_key'] = value
        except KeyError: 
            pass

        try: 
            value = os.environ['CRUSCA_AUTH_TOKEN_' + env_owner_repo]
            conf['AUTH'][owner_repo]['auth_token'] = value
        except KeyError: 
            pass

def _validate_config(config):
    required_keys = [
        'AUTH',
        'ENVIRONMENT',
        'RULES',
    ]

    try:
        for key in required_keys:
            config[key]

            if not config[key]:
                raise ConfigError('{} is empty'.format(key))

        for owner_repo in config['AUTH']:
            config['AUTH'][owner_repo]['auth_token']
            config['AUTH'][owner_repo]['secret_key']

    except KeyError as err:
        raise ConfigError('Key {} is missing'.format(err.args[0]))
