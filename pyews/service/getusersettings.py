import logging
from .serviceendpoint import ServiceEndpoint
from ..utils.exceptions import ObjectType, SoapResponseHasError, SoapAccessDeniedError
from ..utils.exchangeversion import ExchangeVersion

__LOGGER__ = logging.getLogger(__name__)


class GetUserSettings(ServiceEndpoint):
    '''Child class of :doc:`serviceendpoint` that is used to resolve names based on the provided
       :doc:`../configuration/userconfiguration` object.  
       
       This class is used as an alternative to :doc:`../configuration/autodiscover` since
       GetUserSettings endpoint is a common endpoint across all versions of Microsoft Exchange & Office 365.

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
               deleteItem = DeleteItem(messageId, userConfig

        Args:
            userconfiguration (UserConfiguration): A :doc:`../configuration/userconfiguration` object created using the :doc:`../configuration/userconfiguration` class

        Raises:
            ObjectType: An incorrect object type has been used
        '''

    def __init__(self, userconfiguration):
        super(GetUserSettings, self).__init__(userconfiguration)

    def __parse_response(self, value):
        '''Creates and sets a response object

        Args:
            value (str): The raw response from a SOAP request
        '''
        return_dict = {}
        for item in value.find_all('UserSetting'):
            if item.Name.string == 'CasVersion':
                return_dict['CasVersion'] = item.Value.string
            elif (item.Name.string == 'ExternalEwsUrl'):
                return_dict['ExternalEwsUrl'] = item.Value.string
            else:
                return_dict[item.Name.string] = item.Value.string
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
<soap:Envelope xmlns:a="http://schemas.microsoft.com/exchange/2010/Autodiscover"      
               xmlns:wsa="http://www.w3.org/2005/08/addressing" 
               xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"      
               xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Header>
    <a:RequestedServerVersion>Exchange2010</a:RequestedServerVersion>
    <wsa:Action>http://schemas.microsoft.com/exchange/2010/Autodiscover/Autodiscover/GetUserSettings</wsa:Action>
    <wsa:To>{to}</wsa:To>
  </soap:Header>
  <soap:Body>
    <a:GetUserSettingsRequestMessage xmlns:a="http://schemas.microsoft.com/exchange/2010/Autodiscover">
      <a:Request>
        <a:Users>
          <a:User>
            <a:Mailbox>{mailbox}</a:Mailbox>
          </a:User>
        </a:Users>
        <a:RequestedSettings>
          <a:Setting>InternalEwsUrl</a:Setting>
          <a:Setting>ExternalEwsUrl</a:Setting>
          <a:Setting>UserDisplayName</a:Setting>
          <a:Setting>UserDN</a:Setting>
          <a:Setting>UserDeploymentId</a:Setting>
          <a:Setting>InternalMailboxServer</a:Setting>
          <a:Setting>MailboxDN</a:Setting>
          <a:Setting>ActiveDirectoryServer</a:Setting>
          <a:Setting>CasVersion</a:Setting>
          <a:Setting>EwsSupportedSchemas</a:Setting>
        </a:RequestedSettings>
      </a:Request>
    </a:GetUserSettingsRequestMessage>
  </soap:Body>
</soap:Envelope>'''.format(
    to=self.userconfiguration.ews_url, 
    mailbox=self.userconfiguration.credentials.email_address)
