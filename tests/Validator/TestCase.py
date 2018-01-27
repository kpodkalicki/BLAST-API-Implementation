import unittest

_PROGRAMS = ['blastn', 'megablast', 'blastp', 'blastx', 'tblastn', 'tblastx']
_NOT_EMPTY_ERROR = "Parameter '{0}' cannot be empty"
_NOT_NONE_ERROR = "Parameter '{0}' must be specified"
_INVALID_ERROR = "Invalid '{0}' parameter"


class TestCase(unittest.TestCase):
    valid_required_params = {'QUERY': 'test', 'DATABASE': 'test_db', 'PROGRAM': _PROGRAMS[0]}
    validator = None

    def _test_positive(self, params, param_name, test_value):
        params[param_name] = test_value
        errors = self.validator.validate_params(params)
        self.assertEqual(len(errors), 0)

    def _test_negative(self, params, param_name, test_value, expected_errors):
        params[param_name] = test_value
        errors = self.validator.validate_params(params)
        self.assertEqual(errors, expected_errors)
