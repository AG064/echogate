import ast
from pathlib import Path
import secrets
import unittest
from unittest.mock import Mock

tree = ast.parse((Path(__file__).resolve().parents[1] / 'echogate.py').read_text())
functions = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in {'generate_digits', 'extract_digits', 'run_auth'}]
scope = {'secrets': secrets, 'LISTEN_DURATION': 1}
exec(compile(ast.Module(body=functions, type_ignores=[]), 'challenge-functions', 'exec'), scope)


class ChallengeTests(unittest.TestCase):
    def test_digit_normalization_and_challenge_shape(self):
        self.assertEqual(scope['extract_digits']('One 2 THREE'), '123')
        self.assertEqual(scope['extract_digits']('no digits here'), '')
        for _ in range(20):
            self.assertRegex(scope['generate_digits'](3), r'^\d{3}$')

    def test_matches_only_the_current_challenge(self):
        scope['generate_digits'] = lambda count: '123'
        scope['speak_digits'] = Mock()
        scope['listen_for_speech'] = lambda duration: 'one two three'
        self.assertTrue(scope['run_auth']())
        scope['listen_for_speech'] = lambda duration: 'one two four'
        self.assertFalse(scope['run_auth']())
        scope['listen_for_speech'] = lambda duration: ''
        self.assertFalse(scope['run_auth']())


if __name__ == '__main__':
    unittest.main()
