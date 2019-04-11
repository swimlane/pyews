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

        self._soap_request = self.soap(self.email_address)
        self.invoke(self._soap_request)
        self.response = self.raw_soap

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