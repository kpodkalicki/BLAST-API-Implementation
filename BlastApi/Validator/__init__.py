__FORMAT_TYPES__ = {'HTML', 'Text', 'XML', 'XML2', 'JSON2', 'Tabular'}


class BlastValidator:
    def __init__(self, allowed_values):
        self.allowed_values = allowed_values

    def __validate_not_none__(self, param_name, value, errors,):
        if value is None:
            errors.append("'" + param_name + "' must be specified")

    def __validate_value__(self, param_name, value, errors, *, validate_not_none=False):
        if validate_not_none:
            self.__validate_not_none__(param_name, value, errors)
            return
        if value is None or value in self.allowed_values[param_name]:
            return
        errors.append("Invalid '" + param_name + "' parameter")

    def __validate_format_type__(self, format_type, errors):
        if format_type is None or format_type in __FORMAT_TYPES__:
            return True
        errors.append("Invalid 'FORMAT_TYPE' parameter")

    def __validate_grater_than_zero__(self, value, parameter_name, errors):
        if value is None or value > 0:
            return True
        errors.append("Invalid '" + parameter_name + "' parameter")

    def __validate_less_than_zero__(self, value, parameter_name, errors):
        if value is None or value < 0:
            return True
        errors.append("Invalid '" + parameter_name + "' parameter")

    def __validate_ncbi_gi__(self, ncbi_gi, errors):
        if ncbi_gi is None or (ncbi_gi == "F" or ncbi_gi == "T"):
            return True
        errors.append("Invalid 'NCBI_GI' parameter")
