from .serviceendpoint import ServiceEndpoint
from ..utils.exceptions import ObjectType, SoapResponseHasError, SoapAccessDeniedError
from ..utils.exchangeversion import ExchangeVersion


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

    def __parse_response(self, value):
        '''Creates and sets a response object

        Args:
            value (str): The raw response from a SOAP request
        '''
        return_dict = {}
        if value.find('ResolveNamesResponse'):
            temp = value.find('ServerVersionInfo')
            return_dict['server_version_info'] = temp
            ver = "{major}.{minor}".format(
                major=temp['MajorVersion'],
                minor=temp['MinorVersion']
            )
            self.exchange_version = ExchangeVersion(ver).exchangeVersion
            for item in value.find('ResolutionSet'):
                if item.find('Mailbox'):
                    for i in item.find('Mailbox'):
                        return_dict[i.name] = i.string
                if item.find('Contact'):
                    for i in item.find('Contact').descendants:
                        if i.name == 'Entry' and i.string:
                            return_dict[i.name] = i.string
                        else:
                            if i.name and i.string:
                                return_dict[i.name] = i.string
        return return_dict

    def run(self):
        self.raw_xml = self.invoke(self.soap())
        return self.__parse_response(self.raw_xml)

    def soap(self):
        '''Creates the SOAP XML message body

        Returns:
            str: Returns the SOAP XML request body
        '''
        return '''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types"
               xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages">
<soap:Header>
      <t:RequestServerVersion Version="{version}" />
   </soap:Header>
  <soap:Body>
    <ResolveNames xmlns="http://schemas.microsoft.com/exchange/services/2006/messages"
                  xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types"
                  ReturnFullContactData="true">
      <UnresolvedEntry>{email}</UnresolvedEntry>
    </ResolveNames>
  </soap:Body>
</soap:Envelope>
        '''.format(
            version=self.userconfiguration.exchange_version, 
            email=self.userconfiguration.credentials.email_address)
