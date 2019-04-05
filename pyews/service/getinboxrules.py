import requests
from bs4 import BeautifulSoup

from .serviceendpoint import ServiceEndpoint
from pyews.utils.exceptions import ObjectType, SoapResponseHasError, SoapAccessDeniedError


class GetInboxRules (ServiceEndpoint):
    '''Child class of doc:`serviceendpoint` that retrieves inbox (mailbox) rules for a specified email address.

    Examples:
        To use any service class you must provide a :doc:`../configuration/userconfiguration` object first.
        Like all service classes, you can access formatted properties from the EWS endpoint using the `response` property.
        
        If you want to retrieve the inbox rules for a specific email address you must provide it when creating a GetInboxRules object.
            
        .. code-block:: python

           userConfig = UserConfiguration(
               'first.last@company.com',
               'mypassword123'
           )

           inboxRules = GetInboxRules('first.last@company.com', userConfig)

        Args:
            smtp_address (str): The email address you want to get inbox rules for
        userconfiguration (UserConfiguration): A :doc:`../configuration/userconfiguration` object created using the UserConfiguration class
        
        Raises:
        SoapAccessDeniedError: Access is denied when attempting to use Exchange Web Services endpoint
        SoapResponseHasError: An error occurred when parsing the SOAP response
            ObjectType: An incorrect object type has been used
        '''

    def __init__(self, smtp_address, userconfiguration):

        self.email_address = smtp_address

        super(GetInboxRules, self).__init__(userconfiguration)

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
        '''GetInboxRules SOAP response
        
        Returns:
            list: Returns a formatted list of dictionaries of a SOAP response
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
            for item in value.find('Rule'):
                return_dict = {}
                if (item.name == 'Conditions'):
                    for child in item.descendants:
                        if (child.name is not None and child.string is not None):
                            return_dict.update({
                                child.name: child.string
                            })
                if (item.name == 'Actions'):
                    for child in item.descendants:
                        if (child.name is not None and child.string is not None):
                            return_dict.update({
                                child.name: child.string
                            })
                else:
                    return_dict.update({
                        item.name: item.string
                    })
                    
                return_list.append(return_dict)
            self._response = return_list
               

    def invoke(self):
        '''Used to invoke an GetInboxRules SOAP request
        
        Raises:
            SoapResponseHasError: Raises an error when unable to parse a SOAP response
        '''

        soap_payload = self.soap(self.email_address)
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
            raise SoapResponseHasError('Unable to parse response from GetInboxRules')


    def soap(self, email_address):
        '''Creates the SOAP XML message body

        Args:
            email_address (str): A single email addresses you want to GetInboxRules for

        Returns:
            str: Returns the SOAP XML request body
        '''
        if (self.userconfiguration.impersonation):
            impersonation_header = self.userconfiguration.impersonation.header
        else:
            impersonation_header = ''

        return '''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages"
        xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types"
        xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Header>
    <t:RequestServerVersion Version="%s" />
    %s
  </soap:Header>
  <soap:Body>
    <m:GetInboxRules>
      <m:MailboxSmtpAddress>%s</m:MailboxSmtpAddress>
    </m:GetInboxRules>
  </soap:Body>
</soap:Envelope>
        ''' % (self.userconfiguration.exchangeVersion, impersonation_header, email_address)