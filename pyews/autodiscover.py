import requests
from bs4 import BeautifulSoup

from .exchangeversion import ExchangeVersion

class Autodiscover(object):
    
    def __init__(self, credentials, endpoint=None, exchangeVersion=None, create_endpoint_list=False):
        self.credentials = credentials
        
        if endpoint:
            self._endpoint = endpoint
            self.endpoint = self._endpoint
        else:
            self._endpoint = None

        if exchangeVersion:
            self._exchangeVersion = exchangeVersion
            self.exchangeVersion = self._exchangeVersion
        else:
            self._exchangeVersion = None

        if exchangeVersion is not None and create_endpoint_list is False:
            if ExchangeVersion.valid_version(exchangeVersion):
                if exchangeVersion is 'Office365' or 'Exchange2016':
                    self.exchangeVersion = 'Exchange2016'
                    self.endpoint = 'https://outlook.office365.com/autodiscover/autodiscover.svc'
                else:
                    self.exchangeVersion = exchangeVersion
                    self.endpoint = self._autodiscover_endpoint_list(self.credentials.domain)
        elif exchangeVersion is not None and create_endpoint_list is True:
            if ExchangeVersion.valid_version(exchangeVersion):
                if exchangeVersion is 'Office365' or 'Exchange2016':
                    self.exchangeVersion = 'Exchange2016'
                else:
                    self.exchangeVersion = exchangeVersion
                    self.endpoint = self._autodiscover_endpoint_list(self.credentials.domain)
        elif exchangeVersion is None and create_endpoint_list is False:
            raise AttributeError('You must either provide an exchange_version or direct this class to create a URL list for you')
        elif exchangeVersion is None and create_endpoint_list is True:
            self.endpoint = self._autodiscover_endpoint_list(self.credentials.domain)
            self._exchangeVersion = ExchangeVersion.EXCHANGE_VERSIONS

        _response = self.invoke()
        if _response:
            self.response = _response
        else:
            raise AssertionError('Unable to determine autodiscover configuration.')

    @property
    def endpoint(self):
        return self._endpoint

    @endpoint.setter
    def endpoint(self, value):
        if isinstance(value, list):
            endpoint_list = []
            for item in value:
                endpoint_list.append(item)
            self._endpoint = endpoint_list
        else:
            self._endpoint = value

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, value):
        self._response = value

    @property
    def exchangeVersion(self):
        return self._exchangeVersion

    @exchangeVersion.setter
    def exchangeVersion(self, value):
        if isinstance(value, list):
            version_list = []
            for item in value:
                if ExchangeVersion.valid_version(item):
                    version_list.append(item)
            self._exchangeVersion = version_list
        if value is not None:
            if ExchangeVersion.valid_version(value):
                if value is 'Office365' or 'Exchange2016':
                    self._exchangeVersion = 'Exchange2016'
                else:
                    self._exchangeVersion = value
            else:
                raise AttributeError('You must provide one of the following exchange versions: %s' % ExchangeVersion.EXCHANGE_VERSIONS)


    def _autodiscover_endpoint_list(self, domain):
        endpoint_list = []
        endpoint_list.append('https://outlook.office365.com/autodiscover/autodiscover.svc')
        endpoint_list.append("https://%s/autodiscover/autodiscover.svc" % domain)
        endpoint_list.append("https://autodiscover.%s/autodiscover/autodiscover.svc" % domain)
        return endpoint_list

    def invoke(self):
        if isinstance(self.exchangeVersion, list):
            if isinstance(self.endpoint, list):
                for ver in self.exchangeVersion:
                    for endpoint in self.endpoint:
                        autodiscover_result = self._send_autodiscover_payload(endpoint, ver)
                        if autodiscover_result:
                            return autodiscover_result
            else:
                for ver in self.exchangeVersion:
                    autodiscover_result = self._send_autodiscover_payload(self.endpoint, ver)
                    if autodiscover_result:
                            return autodiscover_result
        else:
            if isinstance(self.endpoint, list):
                for endpoint in self.endpoint:
                    autodiscover_result = self._send_autodiscover_payload(endpoint, self.exchangeVersion)
                    if autodiscover_result:
                            return autodiscover_result
            else:
                autodiscover_result = self._send_autodiscover_payload(self.endpoint, self.exchangeVersion)
                if autodiscover_result:
                            return autodiscover_result

    def _send_autodiscover_payload(self, url, version):
        soap_request = self._build_autodiscover_soap_request(url, version)
       # print(soap_request)
        headers = {'content-type': 'text/xml'}
        response = requests.post(
            url,
            data=soap_request, headers=headers, auth=(self.credentials.email_address, self.credentials.password)
            )
        parsed_response = BeautifulSoup(response.content, 'xml')
        if parsed_response.find('ErrorCode').string == 'NoError':
            return parsed_response
        else:
            return False


    def _build_autodiscover_soap_request(self, url, version):
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
</soap:Envelope>''' % (version, url, self.credentials.email_address)

