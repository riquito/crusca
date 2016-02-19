# builtins
import os


def _get_rules_names():
    curdir = os.path.abspath(os.path.dirname(__file__))

    for fname in os.listdir(curdir):
        if fname.endswith('.py') and fname != '__init__.py':
            yield fname[:-3]

rules_names = list(_get_rules_names())


class UnacceptableContentError(Exception):
    pass


class Rule:

    def __init__(self, *args, **kwargs):
        pass

    def analyze(message):
        raise NotImplementedError
