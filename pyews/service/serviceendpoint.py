#from pyews.configuration.userconfiguration import UserConfiguration
#import pyews.configuration.userconfiguration
from bs4 import BeautifulSoup

class ServiceEndpoint(object):
    
    SOAP_REQUEST_HEADER = {'content-type': 'text/xml; charset=UTF-8'}

    def __init__(self, userconfiguration):
        '''Parent class of all endpoints implemented within pyews
        
        Args:
            userconfiguration (UserConfiguration): A UserConfiguration object created using the UserConfiguration class
        '''

        self.userconfiguration = userconfiguration


        self.results = []


    @property
    def userconfiguration(self):
        '''Returns a UserConfiguration object
        
        Returns:
            UserConfiguration: Returns a UserConfiguration object
        '''
        return self._userconfiguration

    @userconfiguration.setter
    def userconfiguration(self, config):
        '''Sets a UserConfiguration object from a child class
        
        Args:
            config (UserConfiguration): A UserConfiguration object created using the UserConfiguration class
        '''

        # deferring importing of userconfiguration until now.
        # This definitely feels hacky but for now 
        # we are going to do this until we have a better solution

        from ..configuration.userconfiguration import UserConfiguration

        if isinstance(config, UserConfiguration):
            self._userconfiguration = config