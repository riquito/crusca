# ours
from . import Rule, UnacceptableContentError


class NoFixupError(UnacceptableContentError):
    pass


class NoFixupRule(Rule):

    def analyze(self, message):
        if message.startswith('fixup!'):
            raise NoFixupError('Message starts with fixup!')

ExportedRule = NoFixupRule
