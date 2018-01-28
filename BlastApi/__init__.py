import collections
import inspect
import re
import shutil
import time

import requests

from BlastApi.Validator.BlastResultsValidator import BlastResultsValidator
from BlastApi.Validator.BlastSearchValidator import BlastSearchValidator

_API_URL = "https://blast.ncbi.nlm.nih.gov/Blast.cgi"


class BlastClient:
    def __init__(self):
        self.search_validator = BlastSearchValidator()
        self.result_validator = BlastResultsValidator()

    def search(self, query, database, program, *, filter=None, format_type=None, expect=None, nucl_reward=None,
               nucl_penalty=None, gapcosts=None, matrix=None, hitlist_size=None, descriptions=None, alignments=None,
               ncbi_gi=None, threshold=None, word_size=None, composition_based_statistics=None, num_threads=None):
        r"""Sends search submission to NCBI-BLAST Common URL API.

        :param query: Search query.
        :param database: Name of existing database or one uploaded to blastdb_custom
        :param program: BLAST Program. One of: ['blastn', 'megablast', 'blastp', 'blastx', 'tblastn', 'tblastx']
        :param filter: Low complexity filtering. F to disable. T or L to enable. Prepend “m” for mask at lookup (e.g., mL)
        :param format_type: Report type. One of: ['HTML', 'Text', 'XML', 'XML2', 'JSON2', 'Tabular']. Default: 'HTML'.
        :param expect: Expect value. Number greater than zero.
        :param nucl_reward: Reward for matching bases (BLASTN and megaBLAST). Integer greater than zero.
        :param gapcosts: Gap existence and extension costs. Pair of positive integers separated by a space.
        :param matrix: Scoring matrix name. One of: ['BLOSUM45', 'BLOSUM50', 'BLOSUM62', 'BLOSUM80', 'BLOSUM90', 'PAM250',
                'PAM30' or 'PAM70']. Default: 'BLOSUM62'
        :param hitlist_size: Number of databases sequences to keep. Integer greater than zero.
        :param descriptions: Number of descriptions to print (applies to HTML and Text). Integer greater than zero.
        :param alignments: Number of alignments to print (applies to HTML and Text). Integer greater than zero.
        :param ncbi_gi: Show NCBI GIs in report. 'T' or 'F'
        :param threshold: Neighboring score for initial words. Positive integer (BLASTP default is 11). Does not apply
                to BLASTN or MegaBLAST).
        :param word_size: Size of word for initial matches. Positive integer.
        :param composition_based_statistics: Composition based statistics algorithm to use. One of [0, 1, 2, 3]. See
                comp_based_stats in https://www.ncbi.nlm.nih.gov/books/NBK279684/ for details.
        :param num_threads: Number of virtual CPUs to use. 	Integer greater than zero (default is 1). Supported only
            on the cloud
        :return: Tuple of request_id and estimated time in seconds until the search is completed
        """

        frame = inspect.currentframe()
        params = self._get_params(frame)
        params["CMD"] = "Put"

        errors = self.search_validator.validate_params(params)
        if errors:
            raise AttributeError(errors)

        response = requests.get(_API_URL, params)
        qblast_info = self.__cropp_qblast_info__(response.text)
        return qblast_info["RID"], qblast_info["RTOE"]

    def check_submission_status(self, request_id):
        r"""Checks submission status.

        :param request_id: ID of requested submission
        :return: Status of submission. 'WAITING', 'UNKNOWN' or 'READY'
        """

        response = requests.get(_API_URL, {"CMD": "Get", "FORMAT_OBJECT": "SearchInfo", "RID": request_id})
        return self.__cropp_qblast_info__(response.text)['Status']

    def get_results(self, request_id, *, format_type='HTML', hitlist_size=None, descriptions=None, alignments=None,
                    ncbi_gi=None, format_object=None, results_file_path='results.zip'):
        r"""Retrieves results from NCBI.

        :param request_id: ID of requested submission
        :param format_type: Report type. One of: ['HTML', 'Text', 'XML', 'XML2', 'JSON2', 'Tabular']. Default: 'HTML'.
        :param hitlist_size: Number of databases sequences to keep. Integer greater than zero.
        :param descriptions: Number of descriptions to print (applies to HTML and Text). Integer greater than zero.
        :param alignments: Number of alignments to print (applies to HTML and Text). Integer greater than zero.
        :param ncbi_gi: Show NCBI GIs in report. 'T' or 'F'
        :param format_object: Object type. SearchInfo (status check) or Alignment (report formatting). Only Alignment is
                valid for retrieving results.
        :param results_file_path: Results relative file path (applies to XML2 and JSON2).
        :return: Results or relative path to results file
        """
        frame = inspect.currentframe()
        params = self._get_params(frame)
        params['CMD'] = 'Get'

        errors = self.result_validator.validate_params(params)
        if errors:
            raise AttributeError(errors)

        if format_type == 'XML2' or format_type == 'JSON2':
            response = requests.get(_API_URL, params, stream=True)
            with open(results_file_path, 'wb') as file:
                shutil.copyfileobj(response.raw, file)
            return results_file_path
        else:
            response = requests.get(_API_URL, params)
            results = response.text

        return results

    def wait_for_results(self, request_id, estimated_time=15, *, format_type='HTML', hitlist_size=None,
                         descriptions=None, alignments=None, ncbi_gi=None, format_object=None,
                         results_file_path='results.zip'):
        r"""Waits for availability of results and retrieves it.

        :param request_id: ID of requested submission
        :param estimated_time: estimated time in seconds until the search is completed
        :param format_type: Report type. One of: ['HTML', 'Text', 'XML', 'XML2', 'JSON2', 'Tabular']. Default: 'HTML'.
        :param hitlist_size: Number of databases sequences to keep. Integer greater than zero.
        :param descriptions: Number of descriptions to print (applies to HTML and Text). Integer greater than zero.
        :param alignments: Number of alignments to print (applies to HTML and Text). Integer greater than zero.
        :param ncbi_gi: Show NCBI GIs in report. 'T' or 'F'
        :param format_object: Object type. SearchInfo (status check) or Alignment (report formatting). Only Alignment is
                valid for retrieving results.
        :param results_file_path: Results relative file path (applies to XML2 and JSON2).
        :return: Results or relative path to results file
        """
        time.sleep(int(estimated_time))
        status = self.check_submission_status(request_id)
        print('Submission status: ' + status)
        while status == 'WAITING':
            time.sleep(2)
            status = self.check_submission_status(request_id)
            print('Submission status: ' + status)

        if status == 'UNKNOWN':
            raise ValueError("NCBI returned 'UNKNOWN' submition state")

        return self.get_results(request_id, format_type=format_type, hitlist_size=hitlist_size,
                                descriptions=descriptions, alignments=alignments, ncbi_gi=ncbi_gi,
                                format_object=format_object, results_file_path=results_file_path)

    def __cropp_qblast_info__(self, html):
        search_results = re.findall('QBlastInfoBegin(.*?)QBlastInfoEnd', html, flags=re.DOTALL)
        if search_results:
            result_dict = dict()
            for search_result in search_results:
                search_result = search_result.strip()
                entries = search_result.split("\n")
                for entry in entries:
                    key_value_pair = entry.split('=')
                    if len(key_value_pair) > 0:
                        key = key_value_pair[0].strip()
                        value = None
                        if len(key_value_pair) > 1:
                            value = key_value_pair[1].strip()
                        result_dict[key] = value
            return result_dict
        return dict()

    def _get_params(self, frame):
        arg_names, _, _, values = inspect.getargvalues(frame)
        arg_names.remove("self")
        params = {arg_name.upper(): values[arg_name] for arg_name in arg_names if values[arg_name]}
        if 'REQUEST_ID' in params:
            params['RID'] = params['REQUEST_ID']
            del params['REQUEST_ID']
        if 'GAPCOSTS' in params and isinstance(params['GAPCOSTS'], collections.Iterable):
            params['GAPCOSTS'] = ' '.join(map(lambda x: str(x), params['GAPCOSTS']))

        return params
