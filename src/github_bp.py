# third parties
from flask import Blueprint, jsonify
# ours
from .decorators import github_events
from .picky_reader import PickyReader
from .rules import UnacceptableContentError

bp = blueprint = Blueprint('github_bp', __name__)

reader = PickyReader()


@bp.route("/push-event", methods=['POST'])
@github_events(['push'])
def push_action():
    errors = []
    for commit in form['commits']:
        try:
            reader.analyze(commit['message'])
        except UnacceptableContentError as err:
            errors.push(commit['id'], err)

    return jsonify({})


@bp.record_once
def keep_config(state):
    config = state.app.config
    for rule_name, config in config['RULES'].items():
        reader.register(rule_name, config)
