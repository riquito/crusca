# builtins
import os, re, importlib

# discard initial tag
# e.g. [UI] New layout
MESSAGE_REGEXP = re.compile(r'^(\[.*?\]\s+)?(?P<message>.*)')

RULE_NAME_REGEXP = re.compile(r'[a-zA-Z0-9_]')

def _get_rules_names():
    curdir = os.path.abspath(os.path.dirname(__file__))

    for fname in os.listdir(curdir):
        if fname.endswith('.py') and fname != '__init__.py':
            yield fname[:-3]

rules_names = list(_get_rules_names())

class UnacceptableContentError(Exception): pass
class RuleNotFoundError(Exception): pass

class Rule:
    def __init__(self, *args, **kwargs):
        pass

    def analyze(message):
        raise NotImplementedError

class PickyReader:
    def __init__(self):
        self.rules = []

    def register(self, name, config):
        if not name in rules_names:
            raise RuleNotFoundError(name)

        module = importlib.import_module('.'+name, 'src.rules')
        self.rules.append(module.ExportedRule(config))

    def read(self, message):
        message = MESSAGE_REGEXP.match(message).group('message')
        for rule in rules:
            rule.analyze(message)
