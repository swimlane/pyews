import requests
import xmltodict, json
from userconfiguration import UserConfiguration
#from pyews.userconfiguration import UserConfiguration

__EXCHANGE_VERSIONS__ = ['Office365','Exchange2016','Exchange2013_SP1', 'Exchange2013', 'Exchange2010_SP2', 'Exchange2010_SP1', 'Exchange2010']

class Autodiscover(object):
    
    def __init__(self, credentials=None, exchangeVersion='Office365'):
        if not credentials:
            raise AttributeError('Credentials object is required')
        self.credentials = credentials
        self._determine_autodiscover_url(exchangeVersion)
        self.invoke_autodiscover()


    def _determine_autodiscover_url(self, location):
        if location in __EXCHANGE_VERSIONS__:
            if location is 'Office365':
                self.exchangeVersion = 'Exchange2016'
                self.autodiscoverUrl = 'https://outlook.office365.com/autodiscover/autodiscover.svc'
            else:
                domain = self.credentials.domain
                self.exchangeVersion = location
                self.autodiscoverUrl = ["https://%s/autodiscover/autodiscover.svc" % domain, "https://autodiscover.%s/autodiscover/autodiscover.svc" % domain]

    def invoke_autodiscover(self):
        soap_request = self._build_autodiscover_soap_request()
       # print(soap_request)
        headers = {'content-type': 'text/xml'}
        response = requests.post(
            self.autodiscoverUrl,
            data=soap_request, headers=headers, auth=(self.credentials.username, self.credentials.password)
            )
        self.usersettings = self.configuration(response.content)

    def configuration(self, content):
        response_dict = xmltodict.parse(content)
        return UserConfiguration(response_dict)

    def _build_autodiscover_soap_request(self):
        return '''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:a="http://schemas.microsoft.com/exchange/2010/Autodiscover"      
               xmlns:wsa="http://www.w3.org/2005/08/addressing" 
               xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"      
               xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Header>
    <a:RequestedServerVersion>%s</a:RequestedServerVersion>
    <wsa:Action>http://schemas.microsoft.com/exchange/2010/Autodiscover/Autodiscover/GetUserSettings</wsa:Action>
    <wsa:To>%s</wsa:To>
  </soap:Header>
  <soap:Body>
    <a:GetUserSettingsRequestMessage xmlns:a="http://schemas.microsoft.com/exchange/2010/Autodiscover">
      <a:Request>
        <a:Users>
          <a:User>
            <a:Mailbox>%s</a:Mailbox>
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
</soap:Envelope>''' % (self.exchangeVersion, self.autodiscoverUrl, self.credentials.username)

