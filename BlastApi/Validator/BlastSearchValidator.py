import re

from BlastApi.Validator import BlastValidator

__FILTER_PATTERN__ = re.compile("^m?[FTL]$")
__AVAILABLE_PROGRAMS__ = {'blastn', 'megablast', 'blastp', 'blastx', 'tblastn', 'tblastx'}
__MATRICES__ = {'BLOSUM45', 'BLOSUM50', 'BLOSUM62', 'BLOSUM80', 'BLOSUM90', 'PAM250', 'PAM30', 'PAM70'}
__STATISTICS_VALUES__ = {0, 1, 2, 3}
__QUERIES__ = {"Accession", "GI", "FASTA"}

__QUERY__ = "QUERY"
__DATABASE__ = "DATABASE"
__PROGRAM__ = "PROGRAM"
__FILTER__ = "FILTER"
__FORMAT_TYPE__ = "FORMAT_TYPE"
__EXPECT__ = "EXPECT"
__NUCL_REWARD__ = "NUCL_REWARD"
__NUCL_PENALTY__ = "NUCL_PENALTY"
__GAP_COSTS__ = "GAPCOSTS"
__MATRIX__ = "MATRIX"
__HITLIST_SIZE__ = "HITLIST_SIZE"
__DESCRIPTIONS__ = "DESCRIPTIONS"
__ALIGNMENTS__ = "ALIGNMENTS"
__NCBI_GI__ = "NCBI_GI"
__THRESHOLD__ = "THRESHOLD"
__WORD_SIZE__ = "WORD_SIZE"
__COMPOSITION_BASED_STATISTICS__ = "COMPOSITION_BASED_STATISTICS"
__NUM_THREADS__ = "NUM_THREADS"


class BlastSearchValidator(BlastValidator):
    def __init__(self):
        allowed_values = {__QUERY__: __QUERIES__, __PROGRAM__: __AVAILABLE_PROGRAMS__, __MATRIX__: __MATRICES__,
                          __COMPOSITION_BASED_STATISTICS__: __STATISTICS_VALUES__}
        super().__init__(allowed_values)

    def validate_params(self, params):
        errors = []
        self.__validate_value__(__QUERY__, params.get(__QUERY__, None), errors, validate_not_none=True)
        self.__validate_not_none__(__DATABASE__, params.get(__DATABASE__, None), errors)
        self.__validate_value__(__PROGRAM__, params.get(__PROGRAM__, None), errors, validate_not_none=True)
        self.__validate_filtering__(params.get(__FILTER__, None), errors)
        self.__validate_format_type__(params.get(__FORMAT_TYPE__, None), errors)
        self.__validate_grater_than_zero__(params.get(__EXPECT__, None), __EXPECT__, errors)
        self.__validate_grater_than_zero__(params.get(__NUCL_REWARD__, None), __NUCL_REWARD__, errors)
        self.__validate_less_than_zero__(params.get(__NUCL_PENALTY__, None), __NUCL_PENALTY__, errors)
        self.__validate_gap_costs__(params.get(__GAP_COSTS__, None), errors)
        self.__validate_value__(__MATRIX__, params.get(__MATRIX__, None), errors)
        self.__validate_grater_than_zero__(params.get(__HITLIST_SIZE__, None), __HITLIST_SIZE__, errors)
        self.__validate_grater_than_zero__(params.get(__DESCRIPTIONS__, None), __DESCRIPTIONS__, errors)
        self.__validate_grater_than_zero__(params.get(__ALIGNMENTS__, None), __ALIGNMENTS__, errors)
        self.__validate_ncbi_gi__(params.get(__NCBI_GI__, None), errors)
        self.__validate_grater_than_zero__(params.get(__THRESHOLD__, None), __THRESHOLD__, errors)
        self.__validate_grater_than_zero__(params.get(__WORD_SIZE__, None), __WORD_SIZE__, errors)
        self.__validate_value__(__COMPOSITION_BASED_STATISTICS__, params.get(__COMPOSITION_BASED_STATISTICS__, None),
                                errors)
        self.__validate_grater_than_zero__(params.get(__NUM_THREADS__, None), __NUM_THREADS__, errors)

        return errors

    def __validate_filtering__(self, filtering, errors):
        if filtering is None or __FILTER_PATTERN__.match(filtering):
            return True
        errors.append("Invalid 'FILTER' parameter")

    def __validate_gap_costs__(self, gap_costs, errors):
        if gap_costs is None:
            return True
        else:
            pair = gap_costs.split(" ")
            if len(pair) == 2:
                value1 = int(pair[0])
                value2 = int(pair[1])
                if value1 >= 0 and value2 >= 0:
                    return True
        errors.append("Invalid 'GAPCOSTS' parameter")

        # def __validate_program__(self, program, errors):
        #     if program in __AVAILABLE_PROGRAMS__:
        #         return True
        #     errors.append("Invalid 'PROGRAM' parameter")

        # def __validate_matrix__(self, matrix, errors):
        #     if matrix is None or matrix in __MATRICES__:
        #         return True
        #     errors.append("Invalid 'MATRIX' parameter")

        # def __validate_composition_based_statistics__(self, composition_based_statistics, errors):
        #     if composition_based_statistics is None or composition_based_statistics in __STATISTICS_VALUES__:
        #         return True
        #     errors.append("Invalid 'COMPOSITION_BASED_STATISTICS' parameter")

        # def __validate_format_object__(self, format_object, errors):
        #     if format_object is None or format_object in __FORMAT_OBJECTS__:
        #         return True
        #     errors.append("Invalid 'FORMAT_OBJECT' parameter")
