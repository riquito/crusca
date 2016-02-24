# builtins
import os
# third parties
from flask import Flask
# ours
from . import github_bp
from . import config_lib


def create_app(config=None):
    app = Flask(__name__)
    app.config.update(config or {})
    app.register_blueprint(github_bp.blueprint)
    return app

def main():
    env = os.environ.get('ENVIRONMENT', 'DEVELOPMENT')
    root_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(root_path, '../config/config.yml')
    config = config_lib.get_config(config_path, env)

    app = create_app(config)
    return app

