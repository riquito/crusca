# builtins
import unittest
# ours
from src.rules.capital_letter import ExportedRule, UnacceptableContentError

class CapitalLetterTests(unittest.TestCase):
    def test_start_with_upper_case(self):
        c = ExportedRule()
        self.assertEqual(None, c.analyze('Foobar'))

    def test_start_with_lower_case(self):
        c = ExportedRule()
        self.assertRaises(UnacceptableContentError, c.analyze, 'foobar')