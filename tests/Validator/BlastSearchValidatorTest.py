import unittest

from BlastApi import BlastSearchValidator
from tests.Validator.TestCase import TestCase, _NOT_NONE_ERROR, _NOT_EMPTY_ERROR, _PROGRAMS, _INVALID_ERROR


class BlastSearchValidatorTest(TestCase):
    validator = BlastSearchValidator()

    def test_required_params(self):
        params = {'QUERY': 'test', 'DATABASE': 'test_db'}

        for program in _PROGRAMS:
            self._test_positive(params, 'PROGRAM', program)

        errors = self.validator.validate_params({'DATABASE': '', 'PROGRAM': _PROGRAMS[0]})
        self.assertEqual(len(errors), 2)
        self.assertIn(_NOT_EMPTY_ERROR.format('database'), errors)

        self.assertIn(_NOT_NONE_ERROR.format('query'), errors)
        errors = self.validator.validate_params({'QUERY': '', 'PROGRAM': _PROGRAMS[0]})
        self.assertEqual(len(errors), 2)
        self.assertIn(_NOT_EMPTY_ERROR.format('query'), errors)
        self.assertIn(_NOT_NONE_ERROR.format('database'), errors)

        errors = self.validator.validate_params({'QUERY': '', 'PROGRAM': 'xyz'})
        self.assertEqual(len(errors), 3)
        self.assertIn(_NOT_EMPTY_ERROR.format('query'), errors)
        self.assertIn(_NOT_NONE_ERROR.format('database'), errors)
        self.assertIn(_INVALID_ERROR.format('program'), errors)

    def test_filter(self):
        allowed_values = ['F', 'T', 'L', 'mT', 'mL']
        param_name = 'FILTER'
        params = dict(self.valid_required_params)

        for allowed_value in allowed_values:
            self._test_positive(params, param_name, allowed_value)

        self._test_positive(params, param_name, '')
        self._test_positive(params, param_name, None)

        self._test_negative(params, param_name, 'X', [_INVALID_ERROR.format('filter')])
        self._test_negative(params, param_name, 'test123', [_INVALID_ERROR.format('filter')])

    def test_format_type(self):
        allowed_values = ['HTML', 'Text', 'XML', 'XML2', 'JSON2', 'Tabular']
        param_name = 'FORMAT_TYPE'
        params = dict(self.valid_required_params)

        for allowed_value in allowed_values:
            self._test_positive(params, param_name, allowed_value)

        self._test_positive(params, param_name, None)
        self._test_positive(params, param_name, '')

        self._test_negative(params, param_name, 'X', [_INVALID_ERROR.format('format_type')])
        self._test_negative(params, param_name, 'Text2', [_INVALID_ERROR.format('format_type')])

    def test_expect(self):
        param_name = 'EXPECT'
        params = dict(self.valid_required_params)

        self._test_positive(params, param_name, 1)
        self._test_positive(params, param_name, 127)
        self._test_positive(params, param_name, None)

        self._test_negative(params, param_name, 0, [_INVALID_ERROR.format('expect')])
        self._test_negative(params, param_name, -1, [_INVALID_ERROR.format('expect')])
        self._test_negative(params, param_name, -53, [_INVALID_ERROR.format('expect')])

    def test_nucl_reward(self):
        param_name = 'NUCL_REWARD'
        params = dict(self.valid_required_params)

        self._test_positive(params, param_name, 1)
        self._test_positive(params, param_name, 127)
        self._test_positive(params, param_name, None)

        self._test_negative(params, param_name, 0, [_INVALID_ERROR.format('nucl_reward')])
        self._test_negative(params, param_name, -1, [_INVALID_ERROR.format('nucl_reward')])
        self._test_negative(params, param_name, -53, [_INVALID_ERROR.format('nucl_reward')])

    def test_nucl_penalty(self):
        param_name = 'NUCL_PENALTY'
        params = dict(self.valid_required_params)

        self._test_positive(params, param_name, -1)
        self._test_positive(params, param_name, -127)
        self._test_positive(params, param_name, None)

        self._test_negative(params, param_name, 0, [_INVALID_ERROR.format('nucl_penalty')])
        self._test_negative(params, param_name, 1, [_INVALID_ERROR.format('nucl_penalty')])
        self._test_negative(params, param_name, 53, [_INVALID_ERROR.format('nucl_penalty')])

    def test_gap_costs(self):
        param_name = 'GAPCOSTS'
        params = dict(self.valid_required_params)

        self._test_positive(params, param_name, '11 1')
        self._test_positive(params, param_name, '1 1')
        self._test_positive(params, param_name, '256 84713')

        self._test_negative(params, param_name, '-1 15', [_INVALID_ERROR.format('gapcosts')])
        self._test_negative(params, param_name, '0 15', [_INVALID_ERROR.format('gapcosts')])
        self._test_negative(params, param_name, '84 -5612', [_INVALID_ERROR.format('gapcosts')])
        self._test_negative(params, param_name, '84 8 5', [_INVALID_ERROR.format('gapcosts')])
        self._test_negative(params, param_name, '-621 -223487', [_INVALID_ERROR.format('gapcosts')])
        self._test_negative(params, param_name, '0 0', [_INVALID_ERROR.format('gapcosts')])

    def test_matrix(self):
        param_name = 'MATRIX'
        params = dict(self.valid_required_params)
        allowed_values = ['BLOSUM45', 'BLOSUM50', 'BLOSUM62', 'BLOSUM80', 'BLOSUM90', 'PAM250', 'PAM30', 'PAM70']

        for allowed_value in allowed_values:
            self._test_positive(params, param_name, allowed_value)

        self._test_positive(params, param_name, None)

        self._test_negative(params, param_name, 'test', [_INVALID_ERROR.format('matrix')])

    def test_hitlist_size(self):
        param_name = 'HITLIST_SIZE'
        params = dict(self.valid_required_params)

        self._test_positive(params, param_name, 1)
        self._test_positive(params, param_name, 265)
        self._test_positive(params, param_name, None)

        self._test_negative(params, param_name, 0, [_INVALID_ERROR.format('hitlist_size')])
        self._test_negative(params, param_name, -1, [_INVALID_ERROR.format('hitlist_size')])
        self._test_negative(params, param_name, -46, [_INVALID_ERROR.format('hitlist_size')])

    def test_descriptions(self):
        param_name = 'DESCRIPTIONS'
        params = dict(self.valid_required_params)

        self._test_positive(params, param_name, 1)
        self._test_positive(params, param_name, 32)
        self._test_positive(params, param_name, None)

        self._test_negative(params, param_name, 0, [_INVALID_ERROR.format('descriptions')])
        self._test_negative(params, param_name, -1, [_INVALID_ERROR.format('descriptions')])
        self._test_negative(params, param_name, -478, [_INVALID_ERROR.format('descriptions')])

    def test_alignments(self):
        param_name = 'ALIGNMENTS'
        params = dict(self.valid_required_params)

        self._test_positive(params, param_name, 1)
        self._test_positive(params, param_name, 45)
        self._test_positive(params, param_name, None)

        self._test_negative(params, param_name, 0, [_INVALID_ERROR.format('alignments')])
        self._test_negative(params, param_name, -1, [_INVALID_ERROR.format('alignments')])
        self._test_negative(params, param_name, -8, [_INVALID_ERROR.format('alignments')])

    def test_ncbi_gi(self):
        param_name = 'NCBI_GI'
        params = dict(self.valid_required_params)

        self._test_positive(params, param_name, 'T')
        self._test_positive(params, param_name, 'F')
        self._test_positive(params, param_name, None)

        self._test_negative(params, param_name, '', [_INVALID_ERROR.format('ncbi_gi')])
        self._test_negative(params, param_name, 'X', [_INVALID_ERROR.format('ncbi_gi')])
        self._test_negative(params, param_name, 'True', [_INVALID_ERROR.format('ncbi_gi')])
        self._test_negative(params, param_name, 'False', [_INVALID_ERROR.format('ncbi_gi')])
        self._test_negative(params, param_name, 'test123', [_INVALID_ERROR.format('ncbi_gi')])

    def test_threshold(self):
        param_name = 'THRESHOLD'
        params = dict(self.valid_required_params)

        self._test_positive(params, param_name, 1)
        self._test_positive(params, param_name, 62487)
        self._test_positive(params, param_name, None)

        self._test_negative(params, param_name, 0, [_INVALID_ERROR.format('threshold')])
        self._test_negative(params, param_name, -1, [_INVALID_ERROR.format('threshold')])
        self._test_negative(params, param_name, -6547, [_INVALID_ERROR.format('threshold')])

    def test_word_size(self):
        param_name = 'WORD_SIZE'
        params = dict(self.valid_required_params)

        self._test_positive(params, param_name, 1)
        self._test_positive(params, param_name, 234)
        self._test_positive(params, param_name, None)

        self._test_negative(params, param_name, 0, [_INVALID_ERROR.format('word_size')])
        self._test_negative(params, param_name, -1, [_INVALID_ERROR.format('word_size')])
        self._test_negative(params, param_name, -2, [_INVALID_ERROR.format('word_size')])

    def test_composition_based_statistics(self):
        param_name = 'COMPOSITION_BASED_STATISTICS'
        params = dict(self.valid_required_params)

        for allowed_value in range(4):
            self._test_positive(params, param_name, allowed_value)

        self._test_negative(params, param_name, 4, [_INVALID_ERROR.format('composition_based_statistics')])
        self._test_negative(params, param_name, 154, [_INVALID_ERROR.format('composition_based_statistics')])
        self._test_negative(params, param_name, -1, [_INVALID_ERROR.format('composition_based_statistics')])
        self._test_negative(params, param_name, -6481, [_INVALID_ERROR.format('composition_based_statistics')])

    def test_num_threads(self):
        param_name = 'NUM_THREADS'
        params = dict(self.valid_required_params)

        self._test_positive(params, param_name, 1)
        self._test_positive(params, param_name, 777)
        self._test_positive(params, param_name, None)

        self._test_negative(params, param_name, 0, [_INVALID_ERROR.format('num_threads')])
        self._test_negative(params, param_name, -1, [_INVALID_ERROR.format('num_threads')])
        self._test_negative(params, param_name, -5987, [_INVALID_ERROR.format('num_threads')])


if __name__ == '__main__':
    unittest.main()
