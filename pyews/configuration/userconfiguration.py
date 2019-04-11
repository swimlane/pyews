import logging
from bs4 import BeautifulSoup
import requests

from pyews.configuration.configuration import Configuration
from pyews.configuration.credentials import Credentials
from pyews.configuration.autodiscover import Autodiscover
from pyews.configuration.impersonation import Impersonation
import pyews.utils.exceptions

from pyews.utils.exceptions import ObjectType, IncorrectParameters, ExchangeVersionError, UserConfigurationError
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
        
        __LOGGER__.info('Hello')
            
        self.credentials = username, password
        
        if exchangeVersion:
            self._exchangeVersion = exchangeVersion
            self.exchangeVersion = self._exchangeVersion
        else:
            self._exchangeVersion = None

        if ewsUrl:
            self._ewsUrl = ewsUrl
            self.ewsUrl = self._ewsUrl
        else:
            self._ewsUrl = None

        if impersonation:
            self._impersonation = impersonation
            self.impersonation = self._impersonation
        else:
            self._impersonation = None

        if autodiscover:
            self._autodiscover = autodiscover
            self.autodiscover = self._autodiscover
        else:
            self._autodiscover = False

        if autodiscover:
            if exchangeVersion is None:
                try:
                    self.raw_soap = Autodiscover(self.credentials, create_endpoint_list=True).response
                    self.properties = self.raw_soap
                except:
                    __LOGGER__.error('Unable to create configuration from Autodiscover service.')
            elif exchangeVersion is not None:
                try:
                    self.raw_soap = Autodiscover(self.credentials, exchangeVersion=self.exchangeVersion).response
                    self.properties = self.raw_soap
                except:
                    __LOGGER__.error('Unable to create configuration from Autodiscover service.')
        else:
            if ewsUrl:
                self.raw_soap = pyews.service.ResolveNames(self).response
                self.properties = self.raw_soap
            else:
                raise IncorrectParameters('If you are not using Autodiscover then you must provide a ewsUrl and exchangeVersion.')


    @property
    def configuration(self):
        return Configuration(self)

    @configuration.setter
    def configuration(self):
        pass
        
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
        self._autodiscover = bool(boolean)

    @property
    def exchangeVersion(self):
        '''The Exchange Version used to connect to EWS

        Returns:
             str: The Exchange Version used to connect to EWS
        '''
        temp = self._exchangeVersion
        return temp

    @exchangeVersion.setter
    def exchangeVersion(self, value):
        '''Verifies and sets the ExchangeVersion for the UserConfiguration.
        This value is used in all ServiceEndpoints parent and child classes
        
        Args:
            value (str): A string value that represents the ExchangeVersion wanting to be used
        
        Raises:
            ExchangeVersionError: An error occured when attempting to verify taht the value passed in was a valid ExchangeVersion
        '''
        if value is not None:
            if ExchangeVersion.valid_version(value):
                if value is 'Office365' or 'Exchange2016':
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
            # Trying to determine if this is a response from a 
            # typical autodiscover response message
            if config.find('ErrorCode').string == 'NoError':
                for item in config.find_all('UserSetting'):
                    if (item.Name.string == 'CasVersion'):
                        self.exchangeVersion = pyews.utils.exchangeversion.ExchangeVersion(item.Value.string).exchangeVersion
                    elif (item.Name.string == 'ExternalEwsUrl'):
                        self.ewsUrl = item.Value.string
                    else:
                        setting_name = item.Name.string
                        setting_value = item.Value.string
                        setattr(self, setting_name, setting_value)
        except:
            try:
                # Trying to determine if this is a response from a
                # typical ResolveNames response message
                if config.find('ResponseCode').string == 'NoError':
                    temp = config.find('ServerVersionInfo')
                    ver = "%s.%s" % (
                        temp['MajorVersion'],
                        temp['MinorVersion']
                    )
                    self.exchangeVersion = pyews.utils.exchangeversion.ExchangeVersion(ver).exchangeVersion
                    for item in config.find('ResolutionSet'):
                        for i in item.find('Mailbox'):
                            setattr(self, i.name, i.string)
                    for item in config.find('ResolutionSet'):
                        for i in item.find('Contact'):
                            setattr(self, i.name, i.string)
            except:
                raise pyews.utils.exceptions.UserConfigurationError('Unable to process response message.')

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