from .exchangeversion import ExchangeVersion
from .core import Core


class classproperty(property):
    def __get__(self, obj, objtype=None):
        return super(classproperty, self).__get__(objtype)
    def __set__(self, obj, value):
        super(classproperty, self).__set__(type(obj), value)
    def __delete__(self, obj):
        super(classproperty, self).__delete__(type(obj))


class Authentication(Core):

    def __init__(cls, username, password, ews_url=None, exchange_version=ExchangeVersion.EXCHANGE_VERSIONS, impersonate_as=None):
        cls.impersonate_as = impersonate_as
        cls.exchange_versions = exchange_version
        cls.credentials = (username, password)
        cls.domain = username
        cls.endpoints = ews_url

    @classproperty
    def impersonate_as(cls):
        return cls.__impersonate_as

    @impersonate_as.setter
    def impersonate_as(cls, value):
        if not value:
            cls.__impersonate_as = ''
        else:
            cls.__impersonate_as = value

    @classproperty
    def credentials(cls):
        return cls._credentials

    @credentials.setter
    def credentials(cls, value):
        if isinstance(value, tuple):
            cls.domain = value[0]
            cls._credentials = value
        else:
            raise AttributeError('Please provide both a username and password')

    @classproperty
    def exchange_versions(cls):
        return cls._exchange_versions

    @exchange_versions.setter
    def exchange_versions(cls, value):
        from .exchangeversion import ExchangeVersion
        if not value:
            cls._exchange_versions = ExchangeVersion.EXCHANGE_VERSIONS
        elif not isinstance(value, list):
            cls._exchange_versions = [value]
        else:
            cls._exchange_versions = value

    @classproperty
    def endpoints(cls):
        return cls._endpoints

    @endpoints.setter
    def endpoints(cls, value):
        from .endpoints import Endpoints
        if not value:
            cls._endpoints = Endpoints(cls.domain).get()
        elif not isinstance(value, list):
            cls._endpoints = [value]
        else:
            cls._endpoints = value

    @classproperty
    def domain(cls):
        return cls._domain

    @domain.setter
    def domain(cls, value):
        '''Splits the domain from an email address
        
        Returns:
            str: Returns the split domain from an email address
        '''
        local, _, domain = value.partition('@')
        cls._domain = domain
