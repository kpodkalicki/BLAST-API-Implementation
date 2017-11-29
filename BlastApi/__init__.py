import re

import requests

_API_URL = "https://blast.ncbi.nlm.nih.gov/Blast.cgi"


class BlastClient:
    def __init__(self):
        self.test = "test"

    def search(self, query, database, program, **params):
        r"""Sends search submission.

        :param query: Search query. Allowed values: ['Accession', 'GI', 'FASTA']
        :param database: Name of existing database or one uploaded to blastdb_custom
        :param program: BLAST Program. One of: ['blastn', 'megablast', 'blastp', 'blastx', 'tblastn', 'tblastx']
        :param params: (optional) Parameters for 'Put' method described in BLAST Documentation: https://ncbi.github.io/blast-cloud/dev/api.html
        :return: Tuple of request_id and estimated time in seconds until the search is completed
        """
        if not params:
            params = dict()
        params = dict(map(lambda key: (key.upper(), params[key]), params))
        params["CMD"] = "Put"
        params["QUERY"] = query
        params["DATABASE"] = database
        params["PROGRAM"] = program
        response = requests.get(_API_URL, params)
        qblast_info = self._crop_qblast_info(response.text)
        return qblast_info["RID"], qblast_info["RTOE"]

    def check_submission_status(self, request_id):
        response = requests.get(_API_URL, {"CMD": "Get", "FORMAT_OBJECT": "SearchInfo", "RID": request_id})
        return self._crop_qblast_info(response.text)

    def _crop_qblast_info(self, html):
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
