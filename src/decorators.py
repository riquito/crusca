# builtins
from functools import wraps
# third parties
from flask import request, abort


def github_events(events):
    """Decorator that check if the request contains the header X-Github-Event
    and his value is one of `events`
    """
    def dec(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if request.headers.get('X-Github-Event') not in events:
                abort(400)
            return func(*args, **kwargs)
        return wrapper
    return dec
