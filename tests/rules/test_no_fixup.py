# builtins
import unittest
# ours
from src.rules.no_fixup import ExportedRule, UnacceptableContentError

class NoFixupTests(unittest.TestCase):
    def test_start_with_allowed_word(self):
        c = ExportedRule()
        self.assertEqual(None, c.analyze('good'))

    def test_start_with_fixup(self):
        c = ExportedRule()
        self.assertRaises(UnacceptableContentError, c.analyze, 'fixup! This is bad')
