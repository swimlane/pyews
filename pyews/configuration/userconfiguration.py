import logging
from ..core import Core
from .credentials import Credentials
from .autodiscover import Autodiscover
from .impersonation import Impersonation
from ..service.resolvenames import ResolveNames
from ..utils.exceptions import IncorrectParameters
from ..utils.exchangeversion import ExchangeVersion

__LOGGER__ = logging.getLogger(__name__)


class UserConfiguration(Core):
    '''UserConfiguration is the main class of pyews.

    It is used by all other ServiceEndpoint parent and child classes.  
    This class represents how you authorize communication with all other SOAP requests throughout this package.

    Examples:

    The UserConfiguration class is the main class used by all services, including the parent class of services called ServiceEndpoint. 

    A UserConfiguration object contains detailed information about how to communicate to Exchange Web Services, as well as additional properties

    The traditional UserConfiguration object can be created by just passing in a username and password.  This will attempt to connect using Autodiscover and will attempt every version of Exchange.

    ```python
    userConfig = UserConfiguration(
        'first.last@company.com',
        'mypassword123'
    )
    ```

    If you the know the Exchange version you want to communicate with you can provide this information:

    ```python
    userConfig = UserConfiguration(
        'first.last@company.com',
        'mypassword123',
        exchangeVersion='Office365'
    )
    ```

    If you do not wish to use Autodiscover then you can tell UserConfiguration to not use it by setting autodiscover to False and provide the ewsUrl instead

    ```python
    userConfig = UserConfiguration(
        'first.last@company.com',
        'mypassword123',
        autodiscover=False,
        ewsUrl='https://outlook.office365.com/EWS/Exchange.asmx'
    )
    ```

    If you would like to use impersonation, you first need to create an Impersonation object and pass that into the UserConfiguration class when creating a user configuration object.

    ```python
    impersonation = Impersonation(primarysmtpaddress='first.last@company.com')

    userConfig = UserConfiguration(
        'first.last@company.com',
        'mypassword123',
        autodiscover=False,
        ewsUrl='https://outlook.office365.com/EWS/Exchange.asmx',
        impersonation=impersonation
    )
    ```
    Args:
        username (str): An email address or username that you use to authenticate to Exchange Web Services
        password (str): The password that you use to authenticate to Exchange Web Services
        exchangeVersion (str, optional): Defaults to None. A string representation of the version of Exchange you are connecting to.  
                                            If no version is provided then we will attempt to use Autodiscover to determine this version from all approved versions
        ewsUrl (str, optional): Defaults to None. An alternative Exchange Web Services URL.
        autodiscover (bool, optional): Defaults to True. If you don't want to use Autodiscover then set this to False, but you must provide a ewsUrl.
        impersonation (bool, optional): Defaults to False. If your credentials have impersonation rights then you can set this value to True to impersonate another user
                                                            but you must provide either a principalname, sid, primarysmtpaddress, or smtpaddress to do so.
        principalname ([type], optional): Defaults to None. Only used when impersonation is set to True.  The PrincipalName of the account you want to impersonate
        sid ([type], optional): Defaults to None. Only used when impersonation is set to True.  The SID of the account you want to impersonate
        primarysmtpaddress ([type], optional): Defaults to None. Only used when impersonation is set to True.  The PrimarySmtpAddress of the account you want to impersonate
        smtpaddress ([type], optional): Defaults to None. Only used when impersonation is set to True.  The SmtpAddress of the account you want to impersonate

    Raises:
        IncorrectParameters: Provided an incorrect configuration of parameters to this class
    '''

    __config_properties = {}

    def __init__(self, username, password, exchange_version=None, ews_url= None, autodiscover=True, impersonation=None):
        self.username = username
        self.password = password
        self.credentials = Credentials(self.username, self.password)
        if not exchange_version:
            self.exchange_version = ExchangeVersion.EXCHANGE_VERSIONS
        else:
            self.exchange_version = exchange_version if not isinstance(exchange_version, list) else [exchange_version]
        self.ews_url = ews_url
        self.impersonation = impersonation
        self.autodiscover = autodiscover

        if self.autodiscover:
            self.__config_properties = Autodiscover(self).run()
            if self.__config_properties.get('external_ews_url'):
                self.ews_url = self.__config_properties['external_ews_url']
        else:
            if self.ews_url:
                    self.exchange_version = 'Exchange2010'
                    self.__config_properties = ResolveNames(self).run()
            else:
                raise IncorrectParameters('If you are not using Autodiscover then you must provide a ews_url and exchange_version.')

    @property
    def impersonation(self):
        return self._impersonation

    @impersonation.setter
    def impersonation(self, value):
        if isinstance(value, Impersonation):
            self._impersonation = value
        else:
            self._impersonation = None

    def get(self):
        self.__config_properties.update(self.__parse_properties())
        return self.__config_properties

    def __parse_properties(self):
        return_dict = {}
        temp = vars(self)
        for item in temp:
            if not item.startswith('_'):
                return_dict.update({
                    self.camel_to_snake(item): temp[item]
                })
        if self.__config_properties:
            for key,val in self.__config_properties.items():
                return_value = None
                if ', ' in val:
                    return_value = []
                    for v in val.split(','):
                        return_value.append(v)
                else:
                    return_value = val
                return_dict.update({
                    self.camel_to_snake(key): val
                })
        return return_dict
