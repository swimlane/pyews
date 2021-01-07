import logging
from ..core import Core

__LOGGER__ = logging.getLogger(__name__)


class GetUserSettings(Core):
    '''Gets user settings based on the provided UserConfiguration object.  

    This class is used as an alternative to Autodiscover since
    GetUserSettings endpoint is a common endpoint across all versions
    of Microsoft Exchange & Office 365.

    Examples:
            
    To use any service class you must provide a UserConfiguration object first.
    Like all service classes, you can access formatted properties from the EWS endpoint using the `response` property.

    By passing in a UserConfiguration object we can 

    ```python
      userConfig = UserConfiguration(
          'first.last@company.com',
          'mypassword123'
      )
      print(GetUserSettings(userConfig).run())
      ```

    Args:
        userconfiguration (UserConfiguration): A UserConfiguration object created using the UserConfiguration class
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
            return_dict[self.camel_to_snake(item.Name.string)] = item.Value.string
        return return_dict

    def run(self, ews_url, exchange_version):
        self.raw_xml = self.invoke(self.soap(ews_url, exchange_version))
        return self.__parse_response(self.raw_xml)

    def soap(self, ews_url, exchange_version):
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
    <a:RequestedServerVersion>{version}</a:RequestedServerVersion>
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
    to=ews_url,
    version=exchange_version, 
    mailbox=self.userconfiguration.credentials.email_address)
