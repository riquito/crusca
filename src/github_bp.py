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

    try:
        repo = payload['repository']['name']
        owner = payload['repository']['owner']['name']
    except KeyError:
        abort(400)

    owner_repo = '{}/{}'.format(owner, repo)
    try:
        secret_key = bp.config['AUTH'][owner_repo]['secret_key']
        auth_token = bp.config['AUTH'][owner_repo]['auth_token']
    except KeyError:
        abort(401)

    client = github_client.GithubClient(auth_token)

    for commit in payload.get('commits') or abort(400):
        try:
            sha = commit['id']
            state = github_client.STATE_SUCCESS
            message = ''.join(commit['message'].splitlines()[:1])
            desc = 'Crusca approved'
        except KeyError:
            abort(400)

        try:
            reader.read(message)
        except UnacceptableContentError as err:
            state = github_client.STATE_FAILURE
            desc = str(err)

        client.set_status(owner, repo, sha, state, desc)

    return jsonify({})

@bp.route('/status')
def status_action():
    return 'alive'


@bp.record_once
def on_blueprint_loaded(state):
    config = state.app.config
    for rule_name, rule_config in config['RULES'].items():
        reader.register(rule_name, rule_config)

    # attach the whole config to the blueprint
    bp.config = config
