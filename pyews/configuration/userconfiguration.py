import logging
from bs4 import BeautifulSoup
import requests

from .credentials import Credentials
from .autodiscover import Autodiscover
from .impersonation import Impersonation

from pyews.service.resolvenames import ResolveNames
from pyews.utils.exceptions import ObjectType, IncorrectParameters, ExchangeVersionError, UserConfigurationError, CredentialsError
from pyews.utils.exchangeversion import ExchangeVersion

__LOGGER__ = logging.getLogger(__name__)


class UserConfiguration(object):
    '''UserConfiguration is the main class of pyews.  It is used by all other ServiceEndpoint parent and child classes.  
    This class represents how you authorize communication with all other SOAP requests throughout this package.
        
    Examples:

        The UserConfiguration class is the main class used by all services, including the parent class of services called ServiceEndpoint. 

        A UserConfiguration object contains detailed information about how to communicate to Exchange Web Services, as well as additional properties

        The traditional UserConfiguration object can be created by just passing in a username and password.  This will attempt to connect using Autodiscover and will attempt every version of Exchange.

            .. code-block:: python
             
               userConfig = UserConfiguration(
                   'first.last@company.com',
                   'mypassword123'
               )

        If you the know the Exchange version you want to communicate with you can provide this information:
            
            .. code-block:: python
             
               userConfig = UserConfiguration(
                   'first.last@company.com',
                   'mypassword123',
                   exchangeVersion='Office365'
               )

        If you do not wish to use Autodiscover then you can tell UserConfiguration to not use it by setting autodiscover to False and provide the ewsUrl instead

            .. code-block:: python
             
               userConfig = UserConfiguration(
                   'first.last@company.com',
                   'mypassword123',
                   autodiscover=False,
                   ewsUrl='https://outlook.office365.com/EWS/Exchange.asmx'
               )

        If you would like to use impersonation, you first need to create an Impersonation object and pass that into the UserConfiguration class when creating a user configuration object.

            .. code-block:: python
             
               impersonation = Impersonation(primarysmtpaddress='first.last@company.com')

               userConfig = UserConfiguration(
                   'first.last@company.com',
                   'mypassword123',
                   autodiscover=False,
                   ewsUrl='https://outlook.office365.com/EWS/Exchange.asmx',
                   impersonation=impersonation
               )

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
    
    def __init__(self, username, password, exchangeVersion=None, ewsUrl= None, autodiscover=True, impersonation=None):
            
        self.credentials = username, password
        self.exchangeVersion = exchangeVersion
        self.ewsUrl = ewsUrl
        self.impersonation = impersonation

        if autodiscover:
            self.autodiscover = autodiscover
        else:
            if ewsUrl:
                self.raw_soap = ResolveNames(self).response
                self.properties = self.raw_soap
            else:
                raise IncorrectParameters('If you are not using Autodiscover then you must provide a ewsUrl and exchangeVersion.')
        
    @property
    def impersonation(self):
        return self._impersonation

    @impersonation.setter
    def impersonation(self, value):
        if isinstance(value, Impersonation):
            self._impersonation = value
        else:
            self._impersonation = None

    @property
    def credentials(self):
        '''Returns a Credentials object
        
        Returns:
            Credentials: A Credentials object made of your passed in username and password
        '''
        return self._credentials

    @credentials.setter
    def credentials(self, creds):
        '''Sets and creates a Credentials object
        
        Args:
            creds (list): A list that contains a username and password
        
        Raises:
            CredentialsError: Error when attempting to create a Credentials object
        '''
        username, password = creds
        try:
            self._credentials = Credentials(username, password)
        except:
            raise CredentialsError('Unable to create credential object using the provided username and password.')

    @property
    def autodiscover(self):
        '''Returns True if Autodiscover is used and False if it is not
        
        Returns:
            bool: Returns True of False
        '''
        return self._autodiscover

    @autodiscover.setter
    def autodiscover(self, boolean):
        '''Sets Autodiscover value to True or False
        
        Args:
            boolean (str): Sets Autodiscover to True or False
        '''
        if self.exchangeVersion:
            self.raw_soap = Autodiscover(self.credentials,exchangeVersion=self.exchangeVersion).response
            self.properties = self.raw_soap
        else:
            self.raw_soap = Autodiscover(self.credentials).response
            self.properties = self.raw_soap

        self._autodiscover = bool(boolean)

    @property
    def exchangeVersion(self):
        '''The Exchange Version used to connect to EWS

        Returns:
             str: The Exchange Version used to connect to EWS
        '''
        return self._exchangeVersion

    @exchangeVersion.setter
    def exchangeVersion(self, value):
        '''Verifies and sets the ExchangeVersion for the UserConfiguration.
        This value is used in all ServiceEndpoints parent and child classes
        
        Args:
            value (str): A string value that represents the ExchangeVersion wanting to be used
        
        Raises:
            ExchangeVersionError: An error occurred when attempting to verify that the value passed in was a valid ExchangeVersion
        '''
        if ExchangeVersion.valid_version(value):
            if value == 'Office365' or value == 'Exchange2016':
                self._exchangeVersion = 'Exchange2016'
            else:
                self._exchangeVersion = value
        else:
            self._exchangeVersion = None

    @property
    def ewsUrl(self):
        '''The EWS Url used to connect to EWS, if not using Autodiscover
        
        Returns:
            str: The EWS URL used to connect to EWS, if not using Autodiscover
        '''
        return self._ewsUrl

    @ewsUrl.setter
    def ewsUrl(self, url):
        '''Sets the EWS Url to use if not using Autodiscover
        
        Args:
            url (str): The EWS Url to use if not using Autodiscover
        '''
        self._ewsUrl = url

    @property
    def properties(self):
        '''Returns a dictionary containing all UserConfiguration properties and values
        
        Returns:
            dict: A dictionary containing all UserConfiguration properties and values
        '''
        return_dict = {}
        temp = vars(self)
        for item in temp:
            if not item.startswith('_'):
                return_dict.update({
                    item: temp[item]
                })
        return return_dict

    @properties.setter
    def properties(self, config):
        '''Takes a BeautifulSoup4 object created from the response of either AutoDiscover or ResolveNames to build a dictionary of UserConfiguration properties and values
        
        Args:
            config (BeautifulSoup): A BeautifulSoup object created from the response of either AutoDiscover or ResolveNames
        
        Raises:
            UserConfigurationError: An error occured when create the configuration object.  This is a critical error in pyews.
        '''
        try:
            if config.find('ErrorCode'):
                if config.find('ErrorCode').string == 'NoError':
                    if config.find('GetUserSettingsResponseMessage'):
                        self._parse_autodiscover_properties(config)
            if config.find('ResponseCode'):
                if config.find('ResponseCode').string == 'NoError':
                    if config.find('ResolveNamesResponse'):
                        self._parse_resolvenames_properties(config)
        except:
            __LOGGER__.warning("An error occurred attempting to parse SOAP response from Exchange Web Services.  Unable to create UserConfiguration properties.", exc_info=True)
         

    def _parse_autodiscover_properties(self, config):
        for item in config.find_all('UserSetting'):
            if (item.Name.string == 'CasVersion'):
                self.exchangeVersion = ExchangeVersion(item.Value.string).exchangeVersion
            elif (item.Name.string == 'ExternalEwsUrl'):
                self.ewsUrl = item.Value.string
            else:
                setattr(self, item.Name.string, item.Value.string)

    def _parse_resolvenames_properties(self, config):
        temp = config.find('ServerVersionInfo')
        ver = "{major}.{minor}".format(
            major=temp['MajorVersion'],
            minor=temp['MinorVersion']
        )
        self.exchangeVersion = ExchangeVersion(ver).exchangeVersion
        for item in config.find('ResolutionSet'):
            for i in item.find('Mailbox'):
                setattr(self, i.name, i.string)
            for i in item.find('Contact').descendants:
                if i.name == 'Entry' and i.string:
                    setattr(self, i['Key'], i.string)
                else:
                    if i.name and i.string:
                        setattr(self, i.name, i.string)

    @property
    def raw_soap(self):
        '''Returns the raw SOAP response
        
        Returns:
            str: Raw SOAP XML response
        '''
        return self._raw_soap

    @raw_soap.setter
    def raw_soap(self, value):
        '''Sets the raw soap response from a SOAP request
        
        Args:
            value (str): The response from a SOAP request
        '''
        self._raw_soap = value