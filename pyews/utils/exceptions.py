class UknownValueError(ValueError):
    """Raised when the provided value is unkown or is not 
    in a specified list or dictionary map
    """
    def __init__(self, provided_value=None, known_values=None):
        if provided_value and known_values:
            if isinstance(known_values, list):
                super().__init__("The provided value {} is unknown. Please provide one of the following values: '{}'".format(
                    provided_value,
                    ','.join([x for x in known_values])
                ))
        else:
            pass