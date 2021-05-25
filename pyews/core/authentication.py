from .exchangeversion import ExchangeVersion
from .core import Core


class AuthenticationProperties(type):

    def __set_initial_property_values(cls):
        if isinstance(cls._credentials, tuple):
            cls.domain = cls._credentials[0]
            cls.endpoints = None
            cls.exchange_versions = None

    @property
    def impersonate_as(cls):
        if not cls._impersonate_as:
            cls._impersonate_as = ''
        return cls._impersonate_as
    
    @impersonate_as.setter
    def impersonate_as(cls, value):
        if not value:
            cls._impersonate_as = ''
        else:
            cls._impersonate_as = value

    @property
    def credentials(cls):
        return cls._credentials

    @credentials.setter
    def credentials(cls, value):
        if isinstance(value, tuple):
            cls._credentials = value
            cls.__set_initial_property_values()
        else:
            raise AttributeError('Please provide both a username and password')

    @property
    def exchange_versions(cls):
        return cls._exchange_versions

    @exchange_versions.setter
    def exchange_versions(cls, value):
        if not value:
            from .exchangeversion import ExchangeVersion
            value = ExchangeVersion.EXCHANGE_VERSIONS
        if not isinstance(value, list):
            value = [value]
        cls._exchange_versions = value

    @property
    def endpoints(cls):
        return cls._endpoints

    @endpoints.setter
    def endpoints(cls, value):
        if not value:
            from .endpoints import Endpoints
            cls._endpoints = Endpoints(cls._domain).get()
        elif not isinstance(value, list):
            cls._endpoints = [value]
        else:
            cls._endpoints = value

    @property
    def domain(cls):
        return cls._domain

    @domain.setter
    def domain(cls, value):
        temp_val = None
        if '@' in value:
            local, _, domain = value.partition('@')
            temp_val = domain
        elif value:
            temp_val = value
        else:
            temp_val = None
        cls._domain = temp_val


class Authentication(object, metaclass=AuthenticationProperties):

    _impersonate_as = None
    _credentials = tuple()
    _exchange_versions = []
    _endpoints = []
    _domain = None
