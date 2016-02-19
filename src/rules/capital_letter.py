# builtins
import re
# ours
from . import Rule, UnacceptableContentError

# yes, only ascii
CAPITAL_LETTER_REGEXP = re.compile(r'^[A-Z]')


class CapitalLetterError(UnacceptableContentError):
    pass


class CapitalLetterRule(Rule):

    def analyze(self, message):
        if not CAPITAL_LETTER_REGEXP.match(message[0:1]):
            raise CapitalLetterError('First letter is not uppercase')

ExportedRule = CapitalLetterRule
