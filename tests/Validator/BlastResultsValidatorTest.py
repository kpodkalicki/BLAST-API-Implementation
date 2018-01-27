from BlastApi.Validator.BlastResultsValidator import BlastResultsValidator
from tests.Validator.TestCase import TestCase, _INVALID_ERROR


class BlastResultsValidatorTest(TestCase):
    validator = BlastResultsValidator()

    def test_format_object(self):
        param_name = 'FORMAT_OBJECT'
        params = dict(self.valid_required_params)

        self._test_positive(params, param_name, 'Alignment')
        self._test_positive(params, param_name, None)
        self._test_negative(params, param_name, 'xyz', [_INVALID_ERROR.format('format_object')])
        self._test_negative(params, param_name, '', [_INVALID_ERROR.format('format_object')])
