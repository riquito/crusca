# third parties
from flask import Flask, jsonify
# ours
from .decorators import github_events

app = Flask(__name__)


@app.route("/push-event", methods=['POST'])
@github_events(['push'])
def push_action():
    return jsonify({})

if __name__ == "__main__":
    app.run()
