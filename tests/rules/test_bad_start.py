# builtins
import unittest
# ours
from src.rules.bad_start import ExportedRule, UnacceptableContentError

class BadStartTests(unittest.TestCase):
    def test_start_with_allowed_word(self):
        c = ExportedRule(['bad1','bad2'])
        self.assertEqual(None, c.analyze('good'))

    def test_start_with_forbidden_word(self):
        c = ExportedRule(['bad1','bad2'])
        self.assertRaises(UnacceptableContentError, c.analyze, 'bad2 is no good')