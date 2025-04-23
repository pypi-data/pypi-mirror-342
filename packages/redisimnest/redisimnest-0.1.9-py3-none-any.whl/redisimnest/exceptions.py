class MissingParameterError(Exception):
    pass

class InvalidPrefixTemplateError(Exception):
    pass

class ParameterValidationError(ValueError): 
    pass

class KeyTypeValidationError(TypeError):
    pass

