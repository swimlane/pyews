from os import access
from .exchangeversion import ExchangeVersion
from .core import Core
from .oauth2connector import OAuth2Connector


class AuthenticationProperties(type):

    def __set_initial_property_values(cls):
        if isinstance(cls._credentials, tuple):
            cls.domain = cls._credentials[0]
            if cls.impersonate_as != '':
                cls.auth_header = cls._credentials[0]
            else:
                cls.auth_header = None
            cls.ews_url = None
            cls.exchange_versions = None
            if cls.tenant_id and cls.client_id and cls.client_secret:
                if not cls.oauth2_authorization_type:
                    print('Please provide an OAuth2 Authorization Types before continuing')
                else:
                    try:
                        cls.access_token = getattr(OAuth2Connector(), cls.oauth2_authorization_type)()
                    except:
                        cls.access_token = getattr(OAuth2Connector(endpoint_version='v2'), cls.oauth2_authorization_type)()

    @property
    def oauth2_authorization_type(cls):
        return cls._oauth2_authorization_type

    @oauth2_authorization_type.setter
    def oauth2_authorization_type(cls, value):
        if value in ['legacy_app_flow', 'auth_code_grant', 'client_credentials_grant', 'backend_app_flow', 'web_application_flow', 'implicit_grant_flow']:
            cls._oauth2_authorization_type = value
            cls.__set_initial_property_values()

    @property
    def client_id(cls):
        return cls._client_id

    @client_id.setter
    def client_id(cls, value):
        cls._client_id = value

    @property
    def client_secret(cls):
        return cls._client_secret

    @client_secret.setter
    def client_secret(cls, value):
        cls._client_secret = value

    @property
    def tenant_id(cls):
        return cls._tenant_id

    @tenant_id.setter
    def tenant_id(cls, value):
        cls._tenant_id = value

    @property
    def access_token(cls):
        return cls._access_token

    @access_token.setter
    def access_token(cls, value):
        cls._access_token = value

    @property
    def redirect_uri(cls):
        return cls._redirect_uri

    @redirect_uri.setter
    def redirect_uri(cls, value):
        cls._redirect_uri = value

    @property
    def oauth2_scope(cls):
        return cls._oauth2_scope

    @oauth2_scope.setter
    def oauth2_scope(cls, value):
        cls._oauth2_scope = value

    @property
    def auth_header(cls):
        cls.__set_initial_property_values()
        if cls.access_token:
            cls._auth_header.update({
                'Authorization': 'Bearer {}'.format(cls.access_token)
            })
        return cls._auth_header

    @auth_header.setter
    def auth_header(cls, value):
        if value:
            cls._auth_header = {
                'X-AnchorMailbox': value
            }
        elif cls.impersonate_as != '':
            cls._auth_header = {
                'X-AnchorMailbox': cls.impersonate_as
            }
        else:
            cls._auth_header = {}

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
    def ews_url(cls):
        return cls._ews_url

    @ews_url.setter
    def ews_url(cls, value):
        if not value:
            from .endpoints import Endpoints
            cls._ews_url = Endpoints(cls._domain).get()
        elif not isinstance(value, list):
            cls._ews_url = [value]
        else:
            cls._ews_url = value

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

    _auth_header = {}
    _oauth2_authorization_type = None
    _oauth2_scope = None
    _client_id = None
    _client_secret = None
    _tenant_id = None
    _access_token = None
    _impersonate_as = None
    _credentials = tuple()
    _exchange_versions = []
    _ews_url = []
    _domain = None
    _redirect_uri = 'https://google.com'
