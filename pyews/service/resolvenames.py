import requests
from bs4 import BeautifulSoup

from .serviceendpoint import ServiceEndpoint
from pyews.utils.exceptions import ObjectType, SoapResponseHasError, SoapAccessDeniedError


class ResolveNames(ServiceEndpoint):
    '''Child class of :doc:`serviceendpoint` that is used to resolve names based on the provided :doc:`../configuration/userconfiguration` object.  This class is used as an alternative to :doc:`../configuration/autodiscover`
        since ResolveNames endpoint is a common endpoint across all versions of Microsoft Exchange & Office 365.
        
        Examples:
            To use any service class you must provide a :doc:`../configuration/userconfiguration` object first.
            Like all service classes, you can access formatted properties from the EWS endpoint using the `response` property.
            
            By passing in a :doc:`../configuration/userconfiguration` object we can 
                
            .. code-block:: python

               userConfig = UserConfiguration(
                   'first.last@company.com',
                   'mypassword123'
               )
        
               messageId = 'AAMkAGZjOTlkOWExLTM2MDEtNGI3MS04ZDJiLTllNzgwNDQxMThmMABGAAAAAABdQG8UG7qjTKf0wCVbqLyMBwC6DuFzUH4qRojG/OZVoLCfAAAAAAEMAAC6DuFzUH4qRojG/OZVoLCfAAAu4Y9UAAA='
               deleteItem = DeleteItem(messageId, userConfig)

        Args:
            userconfiguration (UserConfiguration): A :doc:`../configuration/userconfiguration` object created using the :doc:`../configuration/userconfiguration` class
        
        Raises:
            ObjectType: An incorrect object type has been used
        '''

    def __init__(self, userconfiguration):

        super(ResolveNames, self).__init__(userconfiguration)
        
        self._soap_request = self.soap()
        self.invoke(self._soap_request)
        self.response = self.raw_soap

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
      <UnresolvedEntry>{email}</UnresolvedEntry>
    </ResolveNames>
  </soap:Body>
</soap:Envelope>
        '''.format(email=self.userconfiguration.credentials.email_address)