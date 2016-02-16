# third parties
from flask import Blueprint, jsonify
# ours
from .decorators import github_events

gbp = blueprint = Blueprint('github_bp', __name__)

@gbp.route("/push-event", methods=['POST'])
@github_events(['push'])
def push_action():
    return jsonify({})
