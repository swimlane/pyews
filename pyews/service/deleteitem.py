import requests, re
from bs4 import BeautifulSoup

from .serviceendpoint import ServiceEndpoint
from pyews.utils.exchangeversion import ExchangeVersion
from pyews.utils.exceptions import ObjectType, DeleteTypeError, SoapResponseHasError, SoapAccessDeniedError


class DeleteItem(ServiceEndpoint):
    '''Child class of :doc:`serviceendpoint` which deletes items (typically email messages) from a users mailboxes.
    
    Examples:
        To use any service class you must provide a :doc:`../configuration/userconfiguration` object first.
        Like all service classes, you can access formatted properties from the EWS endpoint using the `response` property.

        If you want to move a single message to the `Deleted Items` folder then provide a string value of the message ID.  The default `delete_type` is to move a message to the `Deleted Items` folder.
        
        .. code-block:: python

           userConfig = UserConfiguration(
               'first.last@company.com',
               'mypassword123'
           )
        
           messageId = 'AAMkAGZjOTlkOWExLTM2MDEtNGI3MS04ZDJiLTllNzgwNDQxMThmMABGAAAAAABdQG8UG7qjTKf0wCVbqLyMBwC6DuFzUH4qRojG/OZVoLCfAAAAAAEMAAC6DuFzUH4qRojG/OZVoLCfAAAu4Y9UAAA='

           deleteItem = DeleteItem(messageId, userConfig)

        If you want to HardDelete a single message then provide a string value of the message ID and specify the `delete_type` as `HardDelete`:
            
        .. code-block:: python

           userConfig = UserConfiguration(
               'first.last@company.com',
               'mypassword123'
           )
        
           messageId = 'AAMkAGZjOTlkOWExLTM2MDEtNGI3MS04ZDJiLTllNzgwNDQxMThmMABGAAAAAABdQG8UG7qjTKf0wCVbqLyMBwC6DuFzUH4qRojG/OZVoLCfAAAAAAEMAAC6DuFzUH4qRojG/OZVoLCfAAAu4Y9UAAA='

           deleteItem = DeleteItem(messageId, userConfig, delete_type='HardDelete')
           
        Args:
        messageId (list or str): An email MessageId to delete
            userconfiguration (UserConfiguration): A UserConfiguration object created using the UserConfiguration class
            delete_type (str, optional): Defaults to MoveToDeletedItems. Specify the DeleteType.  Available options are ['HardDelete', 'SoftDelete', 'MoveToDeletedItems']
        
        Raises:
        SoapAccessDeniedError: Access is denied when attempting to use Exchange Web Services endpoint
        SoapResponseHasError: An error occurred when parsing the SOAP response
            ObjectType: An incorrect object type has been used
        '''

        self.item = item

        super(DeleteItem, self).__init__(userconfiguration)

        if delete_type in self.DELETE_TYPES:
            self.delete_type = delete_type
        else:
            raise DeleteTypeError('You must provide one of the following delete types: %s' % self.DELETE_TYPES)

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
        '''DeleteItem SOAP response dictionary
        
        Returns:
            list: Returns a formatted dictionary of a SOAP response
        '''
        return self._response

    @response.setter
    def response(self, value):
        '''Creates and sets a response object
        
        Args:
            value (str): The raw response from a SOAP request
        '''
        return_list = []
        if value.find('ResponseCode').string != 'NoError':
            for item in value.find_all('DeleteItemResponseMessage'):
                return_list.append({
                    'MessageText': item.MessageText.string,
                    'ResponseCode': item.ResponseCode.string,
                    'DescriptiveLinkKey': item.DescriptiveLinkKey.string
                })
        else:
            return_list.append({
                'MessageText': 'Succesfull'
            })
        self._response = return_list      


    def invoke(self):
        '''Used to invoke an Autodiscover SOAP request
        
        Raises:
            SoapResponseHasError: Raises an error when unable to parse a SOAP response
        '''

        soap_payload = self.soap(self.item)
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
            raise SoapResponseHasError('Unable to parse response from DeleteItem')


    def soap(self, item):
        '''Creates the SOAP XML message body

        Args:
            item (str or list): A single or list of message ids to delete

        Returns:
            str: Returns the SOAP XML request body
        '''
        if (self.userconfiguration.impersonation):
            impersonation_header = self.userconfiguration.impersonation.header
        else:
            impersonation_header = ''

        delete_item_soap_element = self._delete_item_soap_string(item)
        return '''<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types"
               xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages">
   <soap:Header>
      <t:RequestServerVersion Version="%s" />
      %s
   </soap:Header>
   <soap:Body >
    <DeleteItem DeleteType="%s" xmlns="http://schemas.microsoft.com/exchange/services/2006/messages">
      <ItemIds>
        %s
      </ItemIds>
    </DeleteItem>
  </soap:Body>
</soap:Envelope>''' % (self.userconfiguration.exchangeVersion, impersonation_header, self.delete_type, delete_item_soap_element)
        

    def _delete_item_soap_string(self, item):
        '''Creates a ItemId XML element from a single or list of items

        Returns:
            str: Returns the ItemId SOAP XML element(s)
        '''
        item_soap_string = ''
        if (isinstance(item, list)):
            for i in item:
                item_soap_string += '''<t:ItemId Id="%s"/>''' % i
        else:
            item_soap_string = '''<t:ItemId Id="%s"/>''' % item
        return item_soap_string