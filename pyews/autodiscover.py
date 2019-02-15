import requests
from bs4 import BeautifulSoup
from userconfiguration import UserConfiguration
from exchangeversion import ExchangeVersion
#from pyews.userconfiguration import UserConfiguration

class Autodiscover(object):
    
    def __init__(self, credentials, exchangeVersion):
        if not credentials:
            raise AttributeError('Credentials object is required')
        else:
          self.credentials = credentials

        if not exchangeVersion:
            raise AttributeError('You must provide one of the following exchange versions: %s' % ExchangeVersion.EXCHANGE_VERSIONS)
        else:
            self.exchangeVersion = exchangeVersion

        self._determine_autodiscover_url()
        self.invoke_autodiscover()


    def _determine_autodiscover_url(self):
        if self.exchangeVersion in ExchangeVersion.EXCHANGE_VERSIONS:
            if self.exchangeVersion is 'Office365' or 'Exchange2016':
                self.exchangeVersion = 'Exchange2016'
                self.autodiscoverUrl = 'https://outlook.office365.com/autodiscover/autodiscover.svc'
            else:
                domain = self.credentials.domain
                self.autodiscoverUrl = ["https://%s/autodiscover/autodiscover.svc" % domain, "https://autodiscover.%s/autodiscover/autodiscover.svc" % domain]

    def invoke_autodiscover(self):
        soap_request = self._build_autodiscover_soap_request()
       # print(soap_request)
        headers = {'content-type': 'text/xml'}
        response = requests.post(
            self.autodiscoverUrl,
            data=soap_request, headers=headers, auth=(self.credentials.username, self.credentials.password)
            )
        parsed_response = BeautifulSoup(response.content, 'xml')
        self.usersettings = UserConfiguration(parsed_response)

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

