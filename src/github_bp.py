# third parties
from flask import Blueprint, jsonify, request, abort
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
    payload = request.get_json()
    for commit in payload.get('commits') or abort(400):
        try:
            sha = commit['id']
            repo = payload['repository']['name']
            owner = payload['repository']['owner']['name']
            state = github_client.STATE_SUCCESS
            message = commit['message']
            desc = 'Crusca approved'
        except KeyError:
            abort(400)

        try:
            reader.read(message)
        except UnacceptableContentError as err:
            state = github_client.STATE_FAILURE
            desc = err.message

        bp.client.set_status(owner, repo, sha, state, desc)

    return jsonify({})


@bp.record_once
def on_blueprint_loaded(state):
    config = state.app.config
    for rule_name, rule_config in config['RULES'].items():
        reader.register(rule_name, rule_config)

    state.blueprint.client = github_client.GithubClient(config['AUTH_TOKEN'])
