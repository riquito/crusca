# builtins
import importlib
import re
# ours
from .rules import rules_names

# discard initial tag
# e.g. [UI] New layout
MESSAGE_REGEXP = re.compile(r'^(\[.*?\]\s+)?(?P<message>.*)')


class RuleNotFoundError(Exception):
    pass


class PickyReader:

    def __init__(self):
        self.rules = []

    def register(self, name, config):
        if not name in rules_names:
            raise RuleNotFoundError(name)

        module = importlib.import_module('.' + name, 'src.rules')
        self.rules.append(module.ExportedRule(config))

    def read(self, message):
        message = MESSAGE_REGEXP.match(message).group('message')
        for rule in self.rules:
            rule.analyze(message)
