import logging
from bs4 import BeautifulSoup
from .exchangeversion import ExchangeVersion
from .credentials import Credentials
from .autodiscover import Autodiscover
from .resolvenames import ResolveNames
import requests


__LOGGER__ = logging.getLogger(__name__)

class UserConfiguration(object):

    def __init__(self, username, password, exchangeVersion=None, ewsUrl= None, autodiscover=True, impersonation=False, principalname=None, sid=None, primarysmtpaddress=None, smtpaddress=None):
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

        if autodiscover:
            self._autodiscover = autodiscover
            self.autodiscover = self._autodiscover
        else:
            self._autodiscover = False


        if autodiscover:
            if exchangeVersion is None:
                try:
                    self.raw_soap = Autodiscover(self.credentials, create_endpoint_list=True).response
                    self.configuration = self.raw_soap
                except:
                    __LOGGER__.error('Unable to create configuration from Autodiscover service.', exec_info=True)
            elif exchangeVersion is not None:
                try:
                    self.raw_soap = Autodiscover(self.credentials, exchangeVersion=self.exchangeVersion).response
                    self.configuration = self.raw_soap
                except:
                    __LOGGER__.error('Unable to create configuration from Autodiscover service.', exec_info=True)
        else:
            if ewsUrl:
                self.raw_soap = ResolveNames(self).response
                self.configuration = self.raw_soap
            else:
                raise AttributeError('If you are not using Autodiscover then you must provide a ewsUrl and exchangeVersion.')


        if impersonation:
            if principalname is not None:
                self.impersonation_type = 'PrincipalName'
                self.impersonation_value = principalname
            if sid is not None:
                self.impersonation_type = 'SID'
                self.impersonation_value = sid
            if primarysmtpaddress is not None:
                self.impersonation_type = 'PrimarySmtpAddress'
                self.impersonation_value = primarysmtpaddress
            if smtpaddress is not None:
                self.impersonation_type = 'SmtpAddress'
                self.impersonation_value = smtpaddress

    @property
    def credentials(self):
        return self._credentials

    @credentials.setter
    def credentials(self, creds):
        username, password = creds
        try:
            self._credentials = Credentials(username, password)
        except:
            raise AttributeError('Unable to create credential object using the provided username and password.')

    @property
    def autodiscover(self):
        return self._autodiscover

    @autodiscover.setter
    def autodiscover(self, boolean):
        self._autodiscover = bool(boolean)

    @property
    def exchangeVersion(self):
        return self._exchangeVersion

    @exchangeVersion.setter
    def exchangeVersion(self, value):
        if value is not None:
            if ExchangeVersion.valid_version(value):
                if value is 'Office365' or 'Exchange2016':
                    self._exchangeVersion = 'Exchange2016'
                else:
                    self._exchangeVersion = value
            else:
                raise AttributeError('You must provide one of the following exchange versions: %s' % ExchangeVersion.EXCHANGE_VERSIONS)

    @property
    def ewsUrl(self):
        return self._ewsUrl

    @ewsUrl.setter
    def ewsUrl(self, url):
        self._ewsUrl = url

    @property
    def configuration(self):
        return_dict = {}
        temp = vars(self)
        for item in temp:
            if not item.startswith('_'):
                return_dict.update({
                    item: temp[item]
                })
        return return_dict

    @configuration.setter
    def configuration(self, config):
        #print(config)
        print(config.find('ServerVersionInfo')['MajorVersion'])
        try:
            # Trying to determine if this is a response from a 
            # typical autodiscover response message
            if config.find('ErrorCode').string == 'NoError':
                for item in config.find_all('UserSetting'):
                    print(item.Name.string)
                    if (item.Name.string == 'CasVersion'):
                        self.exchangeVersion = ExchangeVersion(item.Value.string).exchangeVersion
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
                    self.exchangeVersion = ExchangeVersion(ver).exchangeVersion
                    for item in config.find('ResolutionSet'):
                        for i in item.find('Mailbox'):
                      #      print(i.name)
                      #     print(i.string)
                            setattr(self, i.name, i.string)
                    for item in config.find('ResolutionSet'):
                        for i in item.find('Contact'):
                            setattr(self, i.name, i.string)
            except:
                raise AttributeError('Unable to process response message.')

    @property
    def raw_soap(self):
        return self._raw_soap

    @raw_soap.setter
    def raw_soap(self, value):
        self._raw_soap = value