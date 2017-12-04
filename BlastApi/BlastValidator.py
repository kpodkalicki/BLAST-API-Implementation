import re

__FILTER_PATTERN__ = re.compile("^m?[FTL]$")
__AVAILABLE_PROGRAMS__ = {'blastn', 'megablast', 'blastp', 'blastx', 'tblastn', 'tblastx'}
__FORMAT_TYPES__ = {'HTML', 'Text', 'XML', 'XML2', 'JSON2', 'Tabular'}
__MATRICES__ = {'BLOSUM45', 'BLOSUM50', 'BLOSUM62', 'BLOSUM80', 'BLOSUM90', 'PAM250', 'PAM30', 'PAM70'}
__STATISTICS_VALUES__ = {0, 1, 2, 3}
__FORMAT_OBJECTS__ = {'SearchInfo', 'Alignment'}


class BlastValidator:
    def validate_search_params(self, *, program, filtering=None, format_type=None, expect=None, nucl_reward=None,
                               nucl_penalty=None, gap_costs=None, matrix=None, hitlist_size=None, descriptions=None,
                               alignments=None, ncbi_gi=None, threshold=None, word_size=None,
                               composition_based_statistics=None, num_threads=None):
        pass

    def __validate_program__(self, program):
        if program in __AVAILABLE_PROGRAMS__:
            return True
        raise AttributeError("Invalid 'PROGRAM' parameter")

    def __validate_filtering__(self, filtering):
        if filtering is None or __FILTER_PATTERN__.match(filtering):
            return True
        raise AttributeError("Invalid 'FILTER' parameter")

    def __validate_format_type__(self, format_type):
        if format_type is None or format_type in __FORMAT_TYPES__:
            return True
        raise AttributeError("Invalid 'FORMAT_TYPE' parameter")

    def __validate_grater_than_zero__(self, value, parameter_name):
        if value is None or value > 0:
            return True
        raise AttributeError("Invalid '" + parameter_name + "' parameter")

    def __validate_less_than_zero__(self, value, parameter_name):
        if value is None or value < 0:
            return True
        raise AttributeError("Invalid '" + parameter_name + "' parameter")

    def __validate_gap_costs__(self, gap_costs):
        if gap_costs is None:
            return True
        else:
            pair = gap_costs.split(" ")
            if len(pair) == 2:
                value1 = int(pair[0])
                value2 = int(pair[1])
                if value1 >= 0 and value2 >= 0:
                    return True
        raise AttributeError("Invalid 'GAPCOSTS' parameter")

    def __validate_matrix__(self, matrix):
        if matrix is None or matrix in __MATRICES__:
            return True
        raise AttributeError("Invalid 'MATRIX' parameter")

    def __validate_ncbi_gi__(self, ncbi_gi):
        if ncbi_gi is None or (ncbi_gi == "F" or ncbi_gi == "T"):
            return True
        raise AttributeError("Invalid 'NCBI_GI' parameter")

    def __validate_composition_based_statistics__(self, composition_based_statistics):
        if composition_based_statistics is None or composition_based_statistics in __STATISTICS_VALUES__:
            return True
        raise AttributeError("Invalid 'COMPOSITION_BASED_STATISTICS' parameter")

    def __validate_format_object__(self, format_object):
        if format_object is None or format_object in __FORMAT_OBJECTS__:
            return True
        raise AttributeError("Invalid 'FORMAT_OBJECT' parameter")