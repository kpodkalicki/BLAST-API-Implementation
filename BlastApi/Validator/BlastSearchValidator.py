import re

from BlastApi.Validator import BlastValidator

_FILTER_PATTERN = re.compile("^F|m?[TL]$")
_AVAILABLE_PROGRAMS = {'blastn', 'megablast', 'blastp', 'blastx', 'tblastn', 'tblastx'}
_MATRICES = {'BLOSUM45', 'BLOSUM50', 'BLOSUM62', 'BLOSUM80', 'BLOSUM90', 'PAM250', 'PAM30', 'PAM70'}
_STATISTICS_VALUES = {0, 1, 2, 3}

_QUERY = "QUERY"
_DATABASE = "DATABASE"
_PROGRAM = "PROGRAM"
_FILTER = "FILTER"
_FORMAT_TYPE = "FORMAT_TYPE"
_EXPECT = "EXPECT"
_NUCL_REWARD = "NUCL_REWARD"
_NUCL_PENALTY = "NUCL_PENALTY"
_GAP_COSTS = "GAPCOSTS"
_MATRIX = "MATRIX"
_HITLIST_SIZE = "HITLIST_SIZE"
_DESCRIPTIONS = "DESCRIPTIONS"
_ALIGNMENTS = "ALIGNMENTS"
_NCBI_GI = "NCBI_GI"
_THRESHOLD = "THRESHOLD"
_WORD_SIZE = "WORD_SIZE"
_COMPOSITION_BASED_STATISTICS = "COMPOSITION_BASED_STATISTICS"
_NUM_THREADS = "NUM_THREADS"


class BlastSearchValidator(BlastValidator):
    def __init__(self):
        allowed_values = {_PROGRAM: _AVAILABLE_PROGRAMS, _MATRIX: _MATRICES,
                          _COMPOSITION_BASED_STATISTICS: _STATISTICS_VALUES}
        super().__init__(allowed_values)

    def validate_params(self, params):
        r"""Validates parameters for search submits to NCBI. Validated parameters are: QUERY, DATABASE, PROGRAM, FILTER,
            FORMAT_TYPE, EXPECT, NUCL_REWARD, NUCL_PENALTY, GAPCOSTS, MATRIX, HITLIST_SIZE, DESCRIPTIONS, ALIGNMENTS,
            NCBI_GI, THRESHOLD, WORD_SIZE, COMPOSITION_BASED_STATISTICS, NUM_THREADS

        :param params: Parameters to be validated
        :return: List of potential errors
        """

        errors = []
        self._validate_not_none(_QUERY, params.get(_QUERY, None), errors)
        self._validate_not_empty(_QUERY, params.get(_QUERY, None), errors)
        self._validate_not_none(_DATABASE, params.get(_DATABASE, None), errors)
        self._validate_not_empty(_DATABASE, params.get(_DATABASE, None), errors)
        self._validate_value(_PROGRAM, params.get(_PROGRAM, None), errors, not_none=True)
        self._validate_filtering(params.get(_FILTER, None), errors)
        self._validate_format_type(params.get(_FORMAT_TYPE, None), errors)
        self._validate_grater_than_zero(params.get(_EXPECT, None), _EXPECT, errors)
        self._validate_grater_than_zero(params.get(_NUCL_REWARD, None), _NUCL_REWARD, errors)
        self._validate_less_than_zero(params.get(_NUCL_PENALTY, None), _NUCL_PENALTY, errors)
        self._validate_gap_costs(params.get(_GAP_COSTS, None), errors)
        self._validate_value(_MATRIX, params.get(_MATRIX, None), errors)
        self._validate_grater_than_zero(params.get(_HITLIST_SIZE, None), _HITLIST_SIZE, errors)
        self._validate_grater_than_zero(params.get(_DESCRIPTIONS, None), _DESCRIPTIONS, errors)
        self._validate_grater_than_zero(params.get(_ALIGNMENTS, None), _ALIGNMENTS, errors)
        self._validate_ncbi_gi(params.get(_NCBI_GI, None), errors)
        self._validate_grater_than_zero(params.get(_THRESHOLD, None), _THRESHOLD, errors)
        self._validate_grater_than_zero(params.get(_WORD_SIZE, None), _WORD_SIZE, errors)
        self._validate_value(_COMPOSITION_BASED_STATISTICS, params.get(_COMPOSITION_BASED_STATISTICS, None), errors)
        self._validate_grater_than_zero(params.get(_NUM_THREADS, None), _NUM_THREADS, errors)

        return errors

    def _validate_filtering(self, filtering, errors):
        if filtering is None or not len(filtering) or _FILTER_PATTERN.match(filtering):
            return True
        errors.append("Invalid 'filter' parameter")

    def _validate_gap_costs(self, gap_costs, errors):
        if gap_costs is None:
            return True
        else:
            pair = gap_costs.split(" ")
            if len(pair) == 2:
                value1 = int(pair[0])
                value2 = int(pair[1])
                if value1 > 0 and value2 > 0:
                    return True
        errors.append("Invalid 'gapcosts' parameter")
