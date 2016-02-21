# builtins
import re
# ours
from . import Rule, UnacceptableContentError


class BadWordError(UnacceptableContentError):
    pass


class BadWordRule(Rule):
    def __init__(self, config):
        self.bad_words = config

        if isinstance(self.bad_words, str):
            self.bad_words = [self.bad_words]

        self.bad_words = [x.lower() for x in self.bad_words]

    def analyze(self, message):
        for word in message.lower().split():
            if word in self.bad_words:
                raise BadWordError('Message can\'t contain the word "{}"'.format(word))

ExportedRule = BadWordRule
