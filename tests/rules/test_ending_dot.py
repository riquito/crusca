# builtins
import unittest
# ours
from src.rules.ending_dot import ExportedRule, UnacceptableContentError

class EndingDotTests(unittest.TestCase):
    def test_ends_with_a_dot_and_it_must(self):
        c = ExportedRule(True)
        self.assertEqual(None, c.analyze('foobar.'))

    def test_does_not_ends_with_a_dot_but_it_is_supposed_to(self):
        c = ExportedRule(True)
        self.assertRaises(UnacceptableContentError, c.analyze, 'foobar')

    def test_does_not_ends_with_a_dot_and_it_must_not(self):
        c = ExportedRule(False)
        self.assertEqual(None, c.analyze('foobar'))

    def test_ends_with_a_dot_but_it_must_not(self):
        c = ExportedRule(False)
        self.assertRaises(UnacceptableContentError, c.analyze, 'foobar.')