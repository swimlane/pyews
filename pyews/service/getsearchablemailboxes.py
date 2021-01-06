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
           from pyews import UserConfiguration
           from pyews import GetSearchableMailboxes

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
    def __init__(self, userconfiguration):
        super(GetSearchableMailboxes, self).__init__(userconfiguration)

    def __parse_response(self, value):
        '''Creates and sets a response object

        Args:
            value (str): The raw response from a SOAP request
        '''
        return_list = []
        if value.find('ResponseCode').string == 'NoError':
            for item in value.find_all('SearchableMailbox'):
                return_list.append({
                    'reference_id': item.ReferenceId.string,
                    'primary_smtp_address': item.PrimarySmtpAddress.string,
                    'display_name': item.DisplayName.string,
                    'is_membership_group': item.IsMembershipGroup.string,
                    'is_external_mailbox': item.IsExternalMailbox.string,
                    'external_email_address': item.ExternalEmailAddress.string,
                    'guid': item.Guid.string
                })
        return return_list

    def run(self):
        self.raw_xml = self.invoke(self.soap())
        return self.__parse_response(self.raw_xml)

    def soap(self):
        '''Creates the SOAP XML message body

        Returns:
            str: Returns the SOAP XML request body
        '''
        if self.userconfiguration.impersonation:
            impersonation_header = self.userconfiguration.impersonation.header
        else:
            impersonation_header = ''

        return '''<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types"
               xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages">
   <soap:Header>
      <t:RequestServerVersion Version="{version}" />
      {header}
   </soap:Header>
   <soap:Body >
      <m:GetSearchableMailboxes>
         <m:ExpandGroupMembership>true</m:ExpandGroupMembership>
      </m:GetSearchableMailboxes>
   </soap:Body>
</soap:Envelope>'''.format(
    version=self.userconfiguration.exchange_version, 
    header=impersonation_header)
