# builtins
import os
# third parties
from flask import Flask
import yaml
# ours
from . import github_bp


def create_app(config=None):
    app = Flask(__name__)
    app.config.update(config or {})
    app.register_blueprint(github_bp.blueprint)
    return app


def get_yaml_config(path, environment):
    environment = environment.upper()

    with open(path) as fp:
        conf = yaml.load(fp)

    # either get a subconf or the whole conf
    conf = conf.get(environment, conf)
    conf['ENVIRONMENT'] = environment
    return {k: v for k, v in conf.items() if k.isupper()}


def main():
    env = os.environ.get('ENVIRONMENT', 'DEVELOPMENT')
    root_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(root_path, '../config/config.yml')
    config = get_yaml_config(config_path, env)

    app = create_app(config)
    return app

