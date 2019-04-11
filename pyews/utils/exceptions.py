class IncorrectParameters(Exception):
    '''Raised when the incorrect configuration of parameters is passed into a Class'''
    pass

class SoapConnectionRefused(Exception):
    '''Raised when a connection is refused from the server'''
    pass

class SoapConnectionError(Exception):
    '''Raised when an error occurs attempting to connect to Exchange Web Services endpoint'''
    pass

class SoapResponseIsNoneError(Exception):
    '''Raised when a SOAP request response is None'''
    pass

class SoapResponseHasError(Exception):
    '''Raised when a SOAP request response contains an error'''
    pass

class SoapAccessDeniedError(Exception):
    '''Raised when a SOAP response message says Access Denied'''
    pass

class ExchangeVersionError(Exception):
    '''Raised when using an Exchange Version that is not supported'''
    pass

class ObjectType(Exception):
    '''Raised when the object type used is not the correct type'''
    pass

class DeleteTypeError(Exception):
    '''Incorrect DeleteType is used'''
    pass

class SearchScopeError(Exception):
    '''Incorrect SearchScope is used'''
    pass

class CredentialsError(Exception):
    '''Unable to create a credential object with the provided input'''
    pass

class UserConfigurationError(Exception):
    '''Unable to create or set a UserConfiguration Configuration property'''
    pass