import requests
from bs4 import BeautifulSoup

from .serviceendpoint import ServiceEndpoint
from pyews.configuration.autodiscover import Autodiscover
from pyews.utils.exchangeversion import ExchangeVersion
from pyews.utils.exceptions import ObjectType, SoapResponseHasError, SoapAccessDeniedError


class GetSearchableMailboxes(ServiceEndpoint):
        '''Child class of ServiceEndpoint that identifies all searchable mailboxes based on the provided UserConfiguration object's permissions
        
    Example:
        To use any service class you must provide a :doc:`../configuration/userconfiguration` object first.
        Like all service classes, you can access formatted properties from the EWS endpoint using the `response` property.
        
        You can acquire 
            
        .. code-block:: python

           userConfig = UserConfiguration(
               'first.last@company.com',
               'mypassword123'
           )

           searchableMailboxes = GetSearchableMailboxes(userconfig)

        If you want to use a property from this object with another class then you can iterate through the list of of mailbox properties.
        For example, if used in conjunction with the :doc:`searchmailboxes` you first need to create a list of mailbox ReferenceIds.

        .. code-block:: python
        
           id_list = []
           for id in searchableMailboxes.response:
               id_list.append(id['ReferenceId'])
           searchResults = SearchMailboxes('subject:"Phishing Email Subject"', userConfig, id_list)

        
        Args:
        userconfiguration (UserConfiguration): A :doc:`../configuration/userconfiguration` object created using the :doc:`../configuration/userconfiguration` class
    Raises:
        SoapAccessDeniedError: Access is denied when attempting to use Exchange Web Services endpoint
        SoapResponseHasError: An error occurred when parsing the SOAP response
        ObjectType: An incorrect object type has been used
        '''

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