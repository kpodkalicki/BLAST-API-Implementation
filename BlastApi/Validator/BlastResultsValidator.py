from BlastApi.Validator import BlastValidator

_FORMAT_TYPE = "FORMAT_TYPE"
_HITLIST_SIZE = "HITLIST_SIZE"
_DESCRIPTIONS = "DESCRIPTIONS"
_ALIGNMENTS = "ALIGNMENTS"
_NCBI_GI = "NCBI_GI"
_FORMAT_OBJECT = "FORMAT_OBJECT"


class BlastResultsValidator(BlastValidator):
    def __init__(self):
        allowed_values = dict()
        super().__init__(allowed_values)

    def validate_params(self, params):
        r"""Validates parameters for retrieving results from NCBI. Validated parameters are: FORMAT_TYPE, HITLIST_SIZE,
                DESCRIPTIONS, ALIGNMENTS, NCBI_GI, FORMAT_OBJECT

        :param params: Parameters to be validated
        :return: List of potential errors
        """
        errors = []

        self._validate_format_type(params.get(_FORMAT_TYPE, None), errors)
        self._validate_grater_than_zero(params.get(_HITLIST_SIZE, None), _HITLIST_SIZE, errors)
        self._validate_grater_than_zero(params.get(_DESCRIPTIONS, None), _DESCRIPTIONS, errors)
        self._validate_grater_than_zero(params.get(_ALIGNMENTS, None), _ALIGNMENTS, errors)
        self._validate_ncbi_gi(params.get(_NCBI_GI, None), errors)
        self._validate_format_object(params.get(_FORMAT_OBJECT, None), errors)

        return errors

    def _validate_format_object(self, value, errors):
        if value is not None and value != 'Alignment':
            errors.append("Invalid 'format_object' parameter")
            return False
        return True
