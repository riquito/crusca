# builtins
import unittest
from unittest.mock import patch, Mock
# ours
from src.picky_reader import PickyReader, RuleNotFoundError
from src.rules import capital_letter

class PickyReaderTests(unittest.TestCase):

    def test_constructor(self):
        reader = PickyReader()
        self.assertEqual([], reader.rules)

    @patch('src.picky_reader.rules_names', new=['capital_letter'])
    def test_register_valid_rule(self):
        reader = PickyReader()
        reader.register('capital_letter', {'foo': 1})
        self.assertEqual(1, len(reader.rules))
        self.assertIsInstance(reader.rules[0], capital_letter.CapitalLetterRule)

    @patch('src.picky_reader.rules_names', new=['capital_letter'])
    def test_register_invalid_rule(self):
        reader = PickyReader()
        self.assertRaises(RuleNotFoundError, reader.register, 'invalid', {'foo':1})

    def test_read_message(self):
        reader = PickyReader()
        rule_mock = Mock()
        reader.rules = [rule_mock]
        reader.read('abc')
        rule_mock.analyze.assert_called_once_with('abc')

    def test_read_tagged_message(self):
        reader = PickyReader()
        rule_mock = Mock()
        reader.rules = [rule_mock]
        reader.read('[TAG] abc')
        rule_mock.analyze.assert_called_once_with('abc')
