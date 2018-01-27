import abc

__FORMAT_TYPES__ = {'HTML', 'Text', 'XML', 'XML2', 'JSON2', 'Tabular'}


class BlastValidator:
    def __init__(self, allowed_values):
        self.allowed_values = allowed_values

    @abc.abstractclassmethod
    def validate_params(self, params):
        """ Validates given params """

    def _validate_not_none(self, param_name, value, errors):
        if value is None:
            errors.append("Parameter '" + param_name.lower() + "' must be specified")
            return False
        return True

    def _validate_not_empty(self, param_name, value, errors):
        if value is not None and len(value) == 0:
            errors.append("Parameter '" + param_name.lower() + "' cannot be empty")
            return False
        return True

    def _validate_value(self, param_name, value, errors, *, not_none=False):
        not_none_result = True
        if not_none:
            not_none_result = self._validate_not_none(param_name, value, errors)

        if value not in self.allowed_values[param_name] and value is not None:
            errors.append("Invalid '" + param_name.lower() + "' parameter")
            return False

        return not_none_result

    def _validate_format_type(self, format_type, errors):
        if format_type is None or len(format_type) == 0 or format_type in __FORMAT_TYPES__:
            return True
        errors.append("Invalid 'format_type' parameter")

    def _validate_grater_than_zero(self, value, parameter_name, errors):
        if value is None or value > 0:
            return True
        errors.append("Invalid '" + parameter_name.lower() + "' parameter")

    def _validate_less_than_zero(self, value, parameter_name, errors):
        if value is None or value < 0:
            return True
        errors.append("Invalid '" + parameter_name.lower() + "' parameter")

    def _validate_ncbi_gi(self, ncbi_gi, errors):
        if ncbi_gi is None or (ncbi_gi == "F" or ncbi_gi == "T"):
            return True
        errors.append("Invalid 'ncbi_gi' parameter")
