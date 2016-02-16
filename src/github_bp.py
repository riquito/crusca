# third parties
from flask import Blueprint, jsonify
# ours
from .decorators import github_events

bp = blueprint = Blueprint('github_bp', __name__)


@bp.route("/push-event", methods=['POST'])
@github_events(['push'])
def push_action():
    return jsonify({})
