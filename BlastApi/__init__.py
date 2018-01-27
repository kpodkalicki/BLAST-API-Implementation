import collections
import inspect
import re
import shutil

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
        r"""Sends search submission.

        :param query: Search query. Allowed values: ['Accession', 'GI', 'FASTA']
        :param database: Name of existing database or one uploaded to blastdb_custom
        :param program: BLAST Program. One of: ['blastn', 'megablast', 'blastp', 'blastx', 'tblastn', 'tblastx']
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
        response = requests.get(_API_URL, {"CMD": "Get", "FORMAT_OBJECT": "SearchInfo", "RID": request_id})
        return self.__cropp_qblast_info__(response.text)['Status']

    def get_results(self, request_id, *, format_type='HTML', hitlist_size=None, descriptions=None, alignments=None,
                    ncbi_gi=None, format_object=None, results_file_path='response.zip'):
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
            results = open(results_file_path, 'w')
        else:
            response = requests.get(_API_URL, params)
            results = response.text

        return results

    def __cropp_qblast_info__(self, html):
        search_results = re.findall('QBlastInfoBegin(.*?)QBlastInfoEnd', html, flags=re.DOTALL)
        if search_results:
            result_dict = dict()
            for search_result in search_results:
                search_result = search_result.strip()
                entries = search_result.split("\n")
                for entry in entries:
                    key_value_pair = entry.split("=")
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

