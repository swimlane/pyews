import requests
from bs4 import BeautifulSoup

from .serviceendpoint import ServiceEndpoint
from pyews.utils.exceptions import ObjectType, SoapResponseHasError, SoapAccessDeniedError


class ResolveNames(ServiceEndpoint):

    def __init__(self, userconfiguration):
        '''Child class of ServiceEndpoint that is used to resolve names based on the provided UserConfiguration object.  This class is used as an alternative to Autodiscover
        since ResolveNames endpoint is a common endpoint across all versions of Microsoft Exchange & Office 365.
        
        Args:
            userconfiguration (UserConfiguration): A UserConfiguration object created using the UserConfiguration class
        
        Raises:
            ObjectType: An incorrect object type has been used
        '''

        super(ResolveNames, self).__init__(userconfiguration)
        
        self._response = ''
        self.invoke()

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
        self.response = value
        self._raw_soap = value

    @property
    def response(self):
        '''ResolveNames SOAP response
        
        Returns:
            str: Returns the ResolveNames response
        '''
        return self._response

    @response.setter
    def response(self, value):
        '''Creates and sets a response object

        Args:
            value (str): The raw response from a SOAP request
        '''
        self._response = value

    def invoke(self):
        '''Used to invoke an ResolveNames SOAP request
        
        Raises:
            SoapResponseHasError: Raises an error when unable to parse a SOAP response
        '''

        soap_payload = self.soap()
        r = requests.post(
            self.userconfiguration.ewsUrl,
            data=soap_payload, 
            headers=self.SOAP_REQUEST_HEADER, 
            auth=(self.userconfiguration.credentials.email_address, self.userconfiguration.credentials.password)
        )
        parsed_response = BeautifulSoup(r.content, 'xml')
        if parsed_response.find('ResponseCode').string == 'NoError':
            self.raw_soap = parsed_response
        elif parsed_response.find('ResponseCode').string == 'ErrorAccessDenied':
            raise SoapAccessDeniedError('%s' % parsed_response.find('MessageText').string)
        else:
            raise SoapResponseHasError('Unable to parse response from ResolveNames')

    def soap(self):
        '''Creates the SOAP XML message body

        Returns:
            str: Returns the SOAP XML request body
        '''
        return '''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:a="http://schemas.microsoft.com/exchange/2010/Autodiscover"      
               xmlns:wsa="http://www.w3.org/2005/08/addressing" 
               xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"      
               xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <ResolveNames xmlns="http://schemas.microsoft.com/exchange/services/2006/messages"
                  xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types"
                  ReturnFullContactData="true">
      <UnresolvedEntry>%s</UnresolvedEntry>
    </ResolveNames>
  </soap:Body>
</soap:Envelope>
        ''' % self.userconfiguration.credentials.email_address