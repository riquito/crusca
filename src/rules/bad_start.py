# builtins
import re
# ours
from . import Rule, UnacceptableContentError


class BadStartingWordError(UnacceptableContentError):
    pass


class BadStartRule(Rule):

    def __init__(self, config):
        self.bad_starts = config

        if isinstance(self.bad_starts, str):
            self.bad_starts = [self.bad_starts]

        self.bad_starts = [x.lower() for x in self.bad_starts]

    def analyze(self, message):
        words = message.lower().split()
        word = words[0] if words else ''

        if word in self.bad_starts:
            raise BadStartingWordError('Message cannot start with word \"{}\"'.format(word))

ExportedRule = BadStartRule
