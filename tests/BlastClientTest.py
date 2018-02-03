import sys
import unittest

import time

from tests import toggle_params

sys.modules['requests'] = __import__('tests.__init__')
from tests.ResultsValidatorMock import ResultsValidatorMock
from tests.SearchValidatorMock import SearchValidatorMock
from BlastApi import BlastClient


class BlastClientTest(unittest.TestCase):
    sv = SearchValidatorMock()
    rv = ResultsValidatorMock()
    bc = BlastClient()
    bc.search_validator = sv
    bc.result_validator = rv

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.maxDiff = 2048

    def test_search_params(self):
        search_params = {'filter': 'filter_value', 'format_type': 'format_type_value', 'expect': 'expect_value',
                         'nucl_reward': 'nucl_reward_value', 'nucl_penalty': 'nucl_penalty_value',
                         'gapcosts': (1, 11), 'matrix': 'martix_value', 'hitlist_size': 'hitlist_value',
                         'descriptions': 'descriptions_value', 'alignments': 'alignments_value',
                         'ncbi_gi': 'ncbi_gi_value',
                         'threshold': 'treshold_value', 'word_size': 'word_size_value',
                         'composition_based_statistics': 'stats_value', 'num_threads': 'threads_value'}

        self.assertFalse(self.sv.validator_was_called())
        self.bc.search('test123', 'test_db', 'test_prog', **search_params)
        passed_search_params = toggle_params()
        expected_search_params = {key.upper(): value for key, value in search_params.items()}
        expected_search_params['CMD'] = 'Put'
        expected_search_params['QUERY'] = 'test123'
        expected_search_params['DATABASE'] = 'test_db'
        expected_search_params['PROGRAM'] = 'test_prog'
        expected_search_params['GAPCOSTS'] = '1 11'
        self.assertEqual(passed_search_params, expected_search_params)
        self.assertTrue(self.sv.validator_was_called())

        search_params = {'filter': 'filter_value', 'nucl_penalty': 'nucl_penalty_value',
                         'descriptions': 'descriptions_value', 'alignments': 'alignments_value',
                         'ncbi_gi': 'ncbi_gi_value',
                         'composition_based_statistics': 'stats_value'}

        self.assertFalse(self.sv.validator_was_called())
        self.bc.search('test456', 'test_db2', 'test_prog2', **search_params)
        passed_search_params = toggle_params()
        expected_search_params = {key.upper(): value for key, value in search_params.items()}
        expected_search_params['CMD'] = 'Put'
        expected_search_params['QUERY'] = 'test456'
        expected_search_params['DATABASE'] = 'test_db2'
        expected_search_params['PROGRAM'] = 'test_prog2'
        self.assertEqual(passed_search_params, expected_search_params)
        self.assertTrue(self.sv.validator_was_called())

        self.assertFalse(self.sv.validator_was_called())
        self.bc.search('test789', 'test_db3', 'test_prog3')
        passed_search_params = toggle_params()
        expected_search_params = {'CMD': 'Put', 'QUERY': 'test789', 'DATABASE': 'test_db3', 'PROGRAM': 'test_prog3'}
        self.assertEqual(passed_search_params, expected_search_params)
        self.assertTrue(self.sv.validator_was_called())

    def test_results_params(self):
        results_params = {'format_type': 'HTML', 'hitlist_size': 'hitlist_value',
                          'descriptions': 'descriptions_value', 'alignments': 'alignments_value',
                          'ncbi_gi': 'nvbi_gi_value', 'format_object': 'None', 'results_file_path': 'results.zip'}

        self.assertFalse(self.rv.validator_was_called())
        self.bc.get_results('4875', **results_params)
        passed_results_params = toggle_params()
        expected_results_params = {key.upper(): value for key, value in results_params.items()}
        expected_results_params['CMD'] = 'Get'
        expected_results_params['RID'] = '4875'
        self.assertEqual(passed_results_params, expected_results_params)
        self.assertTrue(self.rv.validator_was_called())

        results_params = {'format_type': 'JSON', 'descriptions': 'descriptions_value',
                          'ncbi_gi': 'nvbi_gi_value', 'results_file_path': 'results.zip'}

        self.assertFalse(self.rv.validator_was_called())
        self.bc.get_results('15468', **results_params)
        passed_results_params = toggle_params()
        expected_results_params = {key.upper(): value for key, value in results_params.items()}
        expected_results_params['CMD'] = 'Get'
        expected_results_params['RID'] = '15468'
        self.assertEqual(passed_results_params, expected_results_params)
        self.assertTrue(self.rv.validator_was_called())

        self.assertFalse(self.rv.validator_was_called())
        self.bc.get_results('15468')
        passed_results_params = toggle_params()
        expected_results_params = {'CMD': 'Get', 'RID': '15468', 'FORMAT_TYPE': 'HTML',
                                   'RESULTS_FILE_PATH': 'results.zip'}
        self.assertEqual(passed_results_params, expected_results_params)
        self.assertTrue(self.rv.validator_was_called())

    def test_search_response(self):
        rid, rtoe = self.bc.search('test456', 'test_db2', 'test_prog2')
        self.assertEqual(rid, '1337')
        self.assertEqual(rtoe, '17')

    def test_results_response(self):
        content = self.bc.get_results('126848')
        self.assertEqual(content, 'HTML_RESPONSE')

        content = self.bc.get_results('126848', format_type='HTML')
        self.assertEqual(content, 'HTML_RESPONSE')

        content = self.bc.get_results('126848', format_type='Text')
        self.assertEqual(content, 'Text_RESPONSE')

        content = self.bc.get_results('126848', format_type='XML')
        self.assertEqual(content, 'XML_RESPONSE')

        content = self.bc.get_results('126848', format_type='JSON')
        self.assertEqual(content, 'JSON_RESPONSE')

        content = self.bc.get_results('126848', format_type='Tabular')
        self.assertEqual(content, 'Tabular_RESPONSE')

    def test_check_status(self):
        response = self.bc.check_submission_status('123')
        self.assertEqual(response, 'WAITING')

        response = self.bc.check_submission_status('123')
        self.assertEqual(response, 'READY')

    def test_wait_for_resutls(self):
        results_params = {'format_type': 'JSON', 'hitlist_size': 'hitlist_value',
                          'descriptions': 'descriptions_value', 'alignments': 'alignments_value',
                          'ncbi_gi': 'nvbi_gi_value', 'format_object': 'None', 'results_file_path': 'results.zip'}

        expected_results_params = {key.upper(): value for key, value in results_params.items()}
        expected_results_params['CMD'] = 'Get'
        expected_results_params['RID'] = '65847'
        start = time.time()
        content = self.bc.wait_for_results('65847', 23, **results_params)
        passed_results_params = toggle_params()
        stop = time.time()
        self.assertEqual(passed_results_params, expected_results_params)
        self.assertTrue(self.rv.validator_was_called())
        self.assertTrue((stop - start) >= 23)
        self.assertEqual(content, 'JSON_RESPONSE')

    if __name__ == '__main__':
        unittest.main()
