from oauthlib.oauth2.rfc6749.errors import InvalidGrantError
import requests
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from oauthlib.oauth2 import LegacyApplicationClient
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session


class OAuth2Connector:
    """OAuth2Connector is the main authentication mechanism for Microsoft Graph OAuth2 Authentication
    """
    AUTH_MAP = {
        'v1': {
            'authorize_url': 'https://login.microsoftonline.com/{tenant_id}/oauth2/authorize',
            'token_url': 'https://login.microsoftonline.com/{tenant_id}/oauth2/token',
            'resource': 'https://outlook.office365.com' 
        },
        'v2': {
            'authorize_url': 'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize',
            'token_url': 'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token',
            'scope': 'https://outlook.office365.com/EWS.AccessAsUser.All'
        }
    }

    def __init__(self, endpoint_version='v1'):
        """OAuth2Connector is the base (parent) class of both Search and Delete classes.  It is used to perform either delegated authentication flows
        like: (Single-Page, Web Apps, Mobile & Native Apps - Grant Auth Flow) or you can use it in the application authentication auth flows like: (Client Credentials Grant Auth Flow)

        
        Args:
            client_id (str): Your Azure AD Application client ID
            client_secret (str): Your Azure AD Application client secret
            tenant_id (str): Your Azure AD tenant ID
            username (str, optional): A username used to authenticate to Azure or Office 365. Defaults to None. If provided, will use delegated authentication flows
            password (str, optional): The password used to authenticate to Azure or Office 365. Defaults to None. If provided, will use delegated authentication flows
            scopes (list, optional): A list of scopes defined during your Azure AD application registration. Defaults to ['https://graph.microsoft.com/.default'].
            verify_ssl (bool, optional): Whether to verify SSL or not. Defaults to True.
        """
        from .authentication import Authentication
        self.endpoint_version = endpoint_version
        self.verify = True
        self.username = Authentication.credentials[0]
        self.password = Authentication.credentials[1]
        self.client_id = Authentication.client_id
        self.client_secret = Authentication.client_secret
        self.tenant_id = Authentication.tenant_id
        self.access_token = Authentication.access_token
        self.redirect_uri = Authentication.redirect_uri
        self.authorize_url = self.AUTH_MAP.get(endpoint_version).get('authorize_url').format(tenant_id=self.tenant_id)
        self.token_url = self.AUTH_MAP.get(endpoint_version).get('token_url').format(tenant_id=self.tenant_id)
        if endpoint_version == 'v1':
            self.resource = self.AUTH_MAP.get(endpoint_version).get('resource')
        else:
            self.resource = None
        if not Authentication.oauth2_scope:
            if endpoint_version == 'v2':
                self.scope = [self.AUTH_MAP.get(endpoint_version).get('scope')]
            else:
                self.scope = None
        else:
            self.scope = Authentication.oauth2_scope
        self.session = requests.Session()
        self.session.headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        self.session.verify = self.verify
        self.expiration = None

    def __prompt_user(self, url, full_response=False):
        print('Please go here and authorize: ', url)
        response = input('Paste the full redirect URL here:')
        if full_response:
            return response
        if 'code=' in response:
            return response.split('code=')[-1].split('&')[0]
        elif 'id_token=' in response:
            return response.split('id_token=')[-1].split('&')[0]

    def __build_query_param_url(self, url, params):
        url_parse = urlparse(url)
        query = url_parse.query
        url_dict = dict(parse_qsl(query))
        url_dict.update(params)
        url_new_query = urlencode(url_dict)
        url_parse = url_parse._replace(query=url_new_query)
        return urlunparse(url_parse)

    def auth_code_grant(self):
        """Authorization Code Flow Grant
        Reference: https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow
        """
        param = {
                'response_type': 'code',
                'client_id': self.client_id,
                'redirect_uri': self.redirect_uri,
                'state': '1234'
            }
        url = self.__build_query_param_url(self.authorize_url, param)
        authorization_code = self.__prompt_user(url)
        body = f'''
grant_type=authorization_code
&code={authorization_code}
&client_id={self.client_id}
&client_secret={self.client_secret}
&scope={self.scope}
&redirect_uri={self.redirect_uri} 
'''
        response = self.session.request('POST', self.token_url, data=body)
        return response.json().get('access_token')

    def client_credentials_grant(self):
        """Client Credentials Code Flow Grant
        Reference: https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-client-creds-grant-flow
        """
        if self.resource:
            body = {
                'resource' : self.resource,
                'client_id' : self.client_id,
                'client_secret' : self.client_secret,
                'grant_type' : 'client_credentials'
            }
        else:
            body = {
                'scope' : self.scope,
                'client_id' : self.client_id,
                'client_secret' : self.client_secret,
                'grant_type' : 'client_credentials'
            }
        response = self.session.request('POST', self.token_url, data=body).json()
        return response['access_token']

    def implicit_grant_flow(self):
        """Implicit Grant Flow
        Reference: https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-implicit-grant-flow
        """
        params = {
            'client_id': self.client_id,
            'response_type': 'id_token',
            'redirect_uri': self.redirect_uri,
            'scope': 'openid',
            'response_mode': 'fragment',
            'state': 1234,
            'nonce': 678910
        }
        url = self.__build_query_param_url(self.authorize_url, params)
        return self.__prompt_user(url)

    def web_application_flow(self):
        oauth = OAuth2Session(
            client_id=self.client_id,
            redirect_uri=self.redirect_uri,
            scope=self.scope
            )
        authorization_url, state = oauth.authorization_url(self.authorize_url)
        token = oauth.fetch_token(
            self.authority_url,
            client_secret=self.client_secret,
            authorization_response=self.__prompt_user(authorization_url, full_response=True)
        )
        return token

    def legacy_app_flow(self):
        """Resource Ownwer Password Credentials Grant Flow
        Reference: https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth-ropc
        """
        oauth = OAuth2Session(client=LegacyApplicationClient(client_id=self.client_id))
        try:
            if self.endpoint_version == 'v1':
                token = oauth.fetch_token(
                    token_url=self.token_url, 
                    username=self.username,
                    password=self.password, 
                    client_id=self.client_id,
                    client_secret=self.client_secret, 
                    resource=self.resource,
                    verify=self.verify
                )
            else:
                token = oauth.fetch_token(
                    token_url=self.token_url, 
                    username=self.username,
                    password=self.password, 
                    client_id=self.client_id,
                    client_secret=self.client_secret, 
                    scope=self.scope,
                    verify=self.verify
                )
        except InvalidGrantError as e:
            print(e)
            raise Exception('Please use another authorization method. I suggest trying the auth_code_grant() method.') 
        return token['access_token']

    def backend_app_flow(self):
        client = BackendApplicationClient(client_id=self.client_id)
        oauth = OAuth2Session(client=client)
        if self.endpoint_version == 'v1':
            token = oauth.fetch_token(
                token_url=self.token_url, 
                client_id=self.client_id, 
                client_secret=self.client_secret,
                resource=self.resource
            )
        else:
            token = oauth.fetch_token(
                token_url=self.token_url, 
                client_id=self.client_id, 
                client_secret=self.client_secret,
                scope=self.scope
            )
        return token['access_token']
