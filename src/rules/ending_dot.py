# builtins
import re
# ours
from . import Rule, UnacceptableContentError


class EndingDotError(UnacceptableContentError):
    pass


class EndingDotRule(Rule):

    def __init__(self, config):
        self.isExpected = config

    def analyze(self, message):
        last_char = message[-1:]

        if self.isExpected and last_char != '.':
            raise EndingDotError('Message must end with a dot')
        elif last_char == '.' and not self.isExpected:
            raise EndingDotError('Message must not end with a dot')

ExportedRule = EndingDotRule
