import requests
from bs4 import BeautifulSoup

from .serviceendpoint import ServiceEndpoint
from pyews.configuration.autodiscover import Autodiscover
from pyews.utils.exchangeversion import ExchangeVersion
from pyews.utils.exceptions import ObjectType, SoapResponseHasError, SoapAccessDeniedError


class GetSearchableMailboxes(ServiceEndpoint):

    def __init__(self, userconfiguration):
        '''Child class of ServiceEndpoint that identifies all searchable mailboxes based on the provided UserConfiguration object's permissions
        
        Args:
            userconfiguration (UserConfiguration): A UserConfiguration object created using the UserConfiguration class
        
        Raises:
            ObjectType: An incorrect object type has been used
        '''
        super(GetSearchableMailboxes, self).__init__(userconfiguration)

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
        '''GetSearchableMailboxes SOAP response
        
        Returns:
            list: Returns a formatted list of one or more searchable mailboxes objects
        '''
        return self._response

    @response.setter
    def response(self, value):
        '''Creates and sets a response object

        Args:
            value (str): The raw response from a SOAP request
        '''
        return_list = []
        if value.find('ResponseCode').string == 'NoError':
            for item in value.find_all('SearchableMailbox'):
                return_list.append({
                    'ReferenceId': item.ReferenceId.string,
                    'PrimarySmtpAddress': item.PrimarySmtpAddress.string,
                    'DisplayName': item.DisplayName.string,
                    'IsMembershipGroup': item.IsMembershipGroup.string,
                    'IsExternalMailbox': item.IsExternalMailbox.string,
                    'ExternalEmailAddress': item.ExternalEmailAddress.string,
                    'Guid': item.Guid.string
                })
        self._response = return_list

    def invoke(self):
        '''Used to invoke an GetSearchableMailboxes SOAP request
        
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
            raise SoapResponseHasError('Unable to parse response from GetSearchableMailboxes')

    def soap(self):
        '''Creates the SOAP XML message body

        Returns:
            str: Returns the SOAP XML request body
        '''
        if (self.userconfiguration.impersonation):
            impersonation_header = self.userconfiguration.impersonation.header
        else:
            impersonation_header = ''

        return '''<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types"
               xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages">
   <soap:Header>
      <t:RequestServerVersion Version="%s" />
      %s
   </soap:Header>
   <soap:Body >
      <m:GetSearchableMailboxes>
         <m:ExpandGroupMembership>true</m:ExpandGroupMembership>
      </m:GetSearchableMailboxes>
   </soap:Body>
</soap:Envelope>''' % (self.userconfiguration.exchangeVersion, impersonation_header)