import re

import requests

_API_URL = "https://blast.ncbi.nlm.nih.gov/Blast.cgi"


class BlastClient:
    def __init__(self):
        self.test = "test"

    def get(self, request_id, *, format_type=None, hitlist_size=None, descriptions=None, alignments=None, ncbi_gi=None,
            format_object=None):
        response = requests.get(_API_URL, {"QUERY": "u00001", "DATABASE": "nt", "PROGRAM": "blastn", "CMD": "Put"})
        rid, estimated_time = self._crop_qblast_info(response.text)
        print(rid, estimated_time)

    def _crop_qblast_info(self, html):
        search_result = re.search('<!--QBlastInfoBegin(.*?)QBlastInfoEnd\n-->', html, flags=re.DOTALL)
        if search_result:
            lines = search_result.group(1).strip().split("\n")
            if len(lines) == 2:
                rid = lines[0].split(" = ")[1]
                estimated_time = lines[1].split(" = ")[1]
                return rid, int(estimated_time)
        return None

