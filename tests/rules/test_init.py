# builtins
import unittest
# ours
import src.rules

class RulesInitTests(unittest.TestCase):
    def test_rule_analyze_raise_not_implemented_error(self):
        rule = src.rules.Rule()
        self.assertRaises(NotImplementedError, rule.analyze, 'foo')
