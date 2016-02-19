# third parties
from flask import Blueprint, jsonify
# ours
from .decorators import github_events
from .picky_reader import PickyReader
from .rules import UnacceptableContentError
from . import github_client

bp = blueprint = Blueprint('github_bp', __name__)

reader = PickyReader()


@bp.route("/push-event", methods=['POST'])
@github_events(['push'])
def push_action():
    for commit in form['commits']:
        sha = commit['id']
        repo = commit['repository']['name']
        owner = commit['repository']['owner']['name']
        state = github_client.STATE_SUCCES
        desc = 'Crusca approved'

        try:
            reader.analyze(commit['message'])
        except UnacceptableContentError as err:
            state = github_client.STATE_FAILURE
            desc = err.message

        bp.client.set_status(owner, repo, sha, state, desc)

    return jsonify({})


@bp.record_once
def keep_config(state):
    config = state.app.config
    for rule_name, config in config['RULES'].items():
        reader.register(rule_name, config)

    state.blueprint.client = github_client.GithubClient(config['AUTH_TOKEN'])
