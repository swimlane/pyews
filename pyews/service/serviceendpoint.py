from bs4 import BeautifulSoup
import requests, re

from pyews.utils.exceptions import SoapResponseHasError, SoapAccessDeniedError

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

    @property
    def raw_soap(self):
        '''Returns the raw SOAP response
        
        Returns:
            str: Raw SOAP XML response
        '''
        return self._raw_soap

    @raw_soap.setter
    def raw_soap(self, value):
        '''Sets the raw soap and response from a SOAP request
        
        Args:
            value (str): The response from a SOAP request
        '''
        self._raw_soap = value

    def invoke(self, soap_request):
        '''Used to invoke an Autodiscover SOAP request
        
        Args:
            soap_request (str): A formatted SOAP XML request body string
            userconfiguration (UserConfiguration): A UserConfiguration object created using the UserConfiguration class

        Raises:
            SoapResponseHasError: Raises an error when unable to parse a SOAP response
        '''
        r = requests.post(
            self.userconfiguration.ewsUrl,
            data=soap_request,
            headers=self.SOAP_REQUEST_HEADER, 
            auth=(self.userconfiguration.credentials.email_address, self.userconfiguration.credentials.password)
        )
        parsed_response = BeautifulSoup(r.content, 'xml')
        if parsed_response.find('ResponseCode').string == 'NoError':
            self.raw_soap = parsed_response
        elif parsed_response.find('ResponseCode').string == 'ErrorAccessDenied':
            raise SoapAccessDeniedError('%s' % parsed_response.find('MessageText').string)
        else:
            raise SoapResponseHasError('Unable to parse response from DeleteItem')