# builtins
import unittest
# ours
from src.rules.bad_word import ExportedRule, UnacceptableContentError

class BadWordTests(unittest.TestCase):
    def test_words_allowed(self):
        c = ExportedRule(['bad1','bad2'])
        self.assertEqual(None, c.analyze('all fine here'))

    def test_words_forbidden_provide_string(self):
        c = ExportedRule('bad1')
        self.assertRaises(UnacceptableContentError, c.analyze, 'cannot use bad1 here')

    def test_words_forbidden_provide_list(self):
        c = ExportedRule(['bad1','bad2'])
        self.assertRaises(UnacceptableContentError, c.analyze, 'cannot use bad1 here')

    def test_start_with_forbidden_word_different_case(self):
        c = ExportedRule(['bad1','bad2'])
        self.assertRaises(UnacceptableContentError, c.analyze, 'cannot use BaD1 here')
