from bs4 import BeautifulSoup
import requests, logging
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from pyews.utils.exceptions import SoapResponseHasError, SoapAccessDeniedError, SoapConnectionError

__LOGGER__ = logging.getLogger(__name__)


class ServiceEndpoint:
    
    SOAP_REQUEST_HEADER = {'content-type': 'text/xml; charset=UTF-8'}

    def __init__(self, userconfiguration):
        '''Parent class of all endpoints implemented within pyews
        
        Args:
            userconfiguration (UserConfiguration): A UserConfiguration object created using the UserConfiguration class
        '''
        self.userconfiguration = userconfiguration

    @property
    def userconfiguration(self):
        '''Returns a UserConfiguration object
        
        Returns:
            UserConfiguration: Returns a UserConfiguration object
        '''
        return self._userconfiguration

    @userconfiguration.setter
    def userconfiguration(self, config):
        '''Sets a UserConfiguration object from a child class
        
        Args:
            config (UserConfiguration): A UserConfiguration object created using the UserConfiguration class
        '''
        from ..configuration.userconfiguration import UserConfiguration
        if isinstance(config, UserConfiguration):
            self._userconfiguration = config

    def invoke(self, soap_request):
        '''Used to invoke an Autodiscover SOAP request
        
        Args:
            soap_request (str): A formatted SOAP XML request body string
            userconfiguration (UserConfiguration): A UserConfiguration object created using the UserConfiguration class

        Raises:
            SoapResponseHasError: Raises an error when unable to parse a SOAP response
        '''
        try:
            response = requests.post(
                url=self.userconfiguration.ews_url,
                data=soap_request,
                headers=self.SOAP_REQUEST_HEADER,
                auth=(self.userconfiguration.credentials.email_address, self.userconfiguration.credentials.password),
                verify=False
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            return "An Http Error occurred attempting to connect to {ep}:".format(ep=self.userconfiguration.ews_url) + repr(errh)
        except requests.exceptions.ConnectionError as errc:
            return "An Error Connecting to the API occurred attempting to connect to {ep}:".format(ep=self.userconfiguration.ews_url) + repr(errc)
        except requests.exceptions.Timeout as errt:
            return "A Timeout Error occurred attempting to connect to {ep}:".format(ep=self.userconfiguration.ews_url) + repr(errt)
        except requests.exceptions.RequestException as err:
            return "An Unknown Error occurred attempting to connect to {ep}:".format(ep=self.userconfiguration.ews_url) + repr(err)

        parsed_response = BeautifulSoup(response.content, 'xml')
        try:
            if parsed_response.find('ResponseCode').string == 'NoError':
                return parsed_response
        except:
            if parsed_response.find('ErrorCode').string == 'NoError':
                return parsed_response
        if parsed_response.find('ResponseCode').string == 'ErrorAccessDenied':
            raise SoapAccessDeniedError('{}'.format(parsed_response.find('MessageText').string))
        raise SoapResponseHasError('Unable to parse response from {current}'.format(current=self.__class__.__name__))
