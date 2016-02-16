# third parties
from flask import Flask
# ours
from .decorators import github_events
from . import github_bp

app = Flask(__name__)
app.register_blueprint(github_bp.blueprint)



if __name__ == "__main__":
    app.run()
