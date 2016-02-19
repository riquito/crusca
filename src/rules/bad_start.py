# builtins
import re
# ours
from . import Rule, UnacceptableContentError


class BadStartingWordError(UnacceptableContentError):
    pass


class BadStartRule(Rule):

    def __init__(self, config):
        self.mustNot = config

        if isinstance(self.mustNot, str):
            self.mustNot = [self.mustNot]

    def analyze(self, message):
        words = message.split()
        word = words[0] if words else ''

        if word in self.mustNot:
            raise BadStartingWordError('Message cannot start with ' + word)

ExportedRule = BadStartRule
