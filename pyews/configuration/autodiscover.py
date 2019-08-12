import requests, logging
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from bs4 import BeautifulSoup

from pyews.configuration.endpoint import Endpoint
from pyews.utils.exchangeversion import ExchangeVersion
from pyews.utils.exceptions import IncorrectParameters, ExchangeVersionError, SoapResponseHasError, SoapResponseIsNoneError, SoapConnectionRefused, SoapConnectionError

__LOGGER__ = logging.getLogger(__name__)


class Autodiscover(object):
    '''A class used to connect to Exchange Web Services using the Autodiscover service endpoint
    
    The Autodiscover class can be used with both Office 365 and on-premises Exchange 2010 to 2019.
    Currently, it has been thoroughly tested with Office 365 but not so much with the on-premises versions of Exchange.
    
    Example:
        There two typical methods of using the Autodiscover class.  These behave slightly differently depending on your needs.
            1. If you know the Autodiscover URL for your on-premises or Office 365 Exchange Autodiscover service then you can provide this directly
            
            .. code-block:: python

               Autodiscover(
                   credentialObj, 
                   endpoint='https://outlook.office365.com/autodiscover/autodiscover.svc',
                   exchangeVersion='Office365'
               )

            2. If you do not know the Autodiscover URL then you can set create_endpoint_list to True to have the Autodiscover class attempt to generate URL endpoints for you
            
            .. code-block:: python

               Autodiscover(
                   credentialObj,
                   create_endpoint_list=True
               )

    Args:
        credentials (Credentials): An object created using the Credentials class
        endpoint (str, optional): Defaults to None. If you want to specify a different Autodiscover endpoint then provide the url here
        exchangeVersion (str, optional): Defaults to None. An exchange version string
        create_endpoint_list (bool, optional): Defaults to False. If you want the Autodiscover class to generate a list of endpoints to try based on a users email address
    
    Raises:
        IncorrectParameters: An error occurred by not passing the correct parameters into this class
        ExchangeVersionError: An error occurred when passing in an exchange version that is not supported
        SoapResponseHasError: An error occurred when parsing the SOAP response

    '''

    def __init__(self, credentials, endpoint=None, exchangeVersion=None):

        self.credentials = credentials
        
        if exchangeVersion:
            self.exchangeVersion = exchangeVersion
        else:
            self.exchangeVersion = ExchangeVersion.EXCHANGE_VERSIONS

        if endpoint:
            self.endpoint = endpoint
        else:
            self.endpoint = Endpoint(self.exchangeVersion, domain=self.credentials.domain).endpoint

        _response = self.invoke()
        if _response:
            self.response = _response
        else:
            raise SoapResponseIsNoneError('Unable to determine autodiscover configuration.')

    @property
    def endpoint(self):
        '''The Autodiscover endpoint used when connecting to EWS
        
        Returns:
            :obj:`list` of :obj:`str`: Autodiscover endpoint URL used to connect with EWS
        '''
        return self._endpoint

    @endpoint.setter
    def endpoint(self, value):
        endpoint_list = []
        if isinstance(value, list):
            for item in value:
                endpoint_list.append(item)
        else:
            endpoint_list.append(value)
        self._endpoint = endpoint_list

    @property
    def response(self):
        '''Autodiscover service response
        
        Returns:
            str: Response message from the Autodiscover service
        '''
        return self._response

    @response.setter
    def response(self, value):
        self._response = value

    @property
    def exchangeVersion(self):
        '''The Exchange Version used to connect to the Autodiscover service
        
        Returns:
            str: The Exchange Version used to connect to the Autodiscover service
        '''
        return self._exchangeVersion

    @exchangeVersion.setter
    def exchangeVersion(self, value):
        return_list = []
        if isinstance(value, list):
            for item in value:
                if ExchangeVersion.valid_version(item):
                    if item is 'Office365' or 'Exchange2016':
                        return_list.append('Exchange2016')
                    else:
                        return_list.append(value)
        else:
            if ExchangeVersion.valid_version(value):
                if value is 'Office365' or 'Exchange2016':
                    return_list.append('Exchange2016')
                else:
                    return_list.append(value)

        self._exchangeVersion = return_list

    def invoke(self):
        '''Used to invoke an Autodiscover SOAP request
        
        Returns:
            str: Returns response from SOAP request
        '''
        soap_list = []
        for ver in self.exchangeVersion:
            for endpoint in self.endpoint:
                __LOGGER__.debug("Determining if Exchange Version of {ver} and {ep} is a valid endpoint".format(ver=ver,ep=endpoint))
                try:
                    requests.get(endpoint)
                    soap_request = self._soap_request(endpoint, ver)
                    autodiscover_result = self._send_autodiscover_payload(endpoint, soap_request)
                    __LOGGER__.debug(autodiscover_result)
                    if autodiscover_result:
                        return autodiscover_result
                except requests.RequestException as e:
                    __LOGGER__.debug(
                        "An Error {err} occurred when checking if Exchange Version {ver} and Autodiscover endpoint of {ep} is accessible.".format(
                            err=e.__class__.__name__,
                            ver=ver,
                            ep=endpoint
                        )
                    )
                    continue


    def _send_autodiscover_payload(self, endpoint, soap_body):
        '''Used to send and retrieve response from EWS
        
        Args:
            url (str): Autodiscover URL for requests
            version (str): Exchange version used in SOAP request body
        '''
        headers = {'content-type': 'text/xml'}
        try:
            response = requests.post(
                endpoint,
                data=soap_body,
                headers=headers,
                auth=(self.credentials.email_address, self.credentials.password),
                stream=True
            )
        except requests.exceptions.RequestException as e:
            __LOGGER__.warning(
                "An {err} occurred connecting to autodiscover endpoint: {ep}".format(
                    err=e.__class__.__name__,
                    ep=endpoint
                ),
                exc_info=True
            )

        __LOGGER__.debug('Raw Resposne from Requests is {}'.format(response.text))
        parsed_response = BeautifulSoup(response.content, 'xml')
        __LOGGER__.debug('Parsed Response is {}'.format(parsed_response))
        if parsed_response.find('ErrorCode').string == 'NoError':
            return parsed_response
        
        raise SoapResponseHasError('The Autodiscover Parsed Response contains an error')


    def _soap_request(self, url, version):
        '''Builds XML SOAP request
        
        Args:
            url (str): Autodiscover URL for requests
            version (str): Exchange version used in SOAP request body
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
</soap:Envelope>'''.format(version=version, to=url, mailbox=self.credentials.email_address)