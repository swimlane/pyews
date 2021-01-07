import logging
import requests
import xmltodict
import json
from bs4 import BeautifulSoup

__LOGGER__ = logging.getLogger(__name__)


class Core:

    SOAP_REQUEST_HEADER = {'content-type': 'text/xml; charset=UTF-8'}

    def __init__(self, userconfiguration):
        '''Parent class of all endpoints implemented within pyews
        
        Args:
            userconfiguration (UserConfiguration): A UserConfiguration object created using the UserConfiguration class
        '''
        self.userconfiguration = userconfiguration

    def camel_to_snake(self, s):
        if s != 'UserDN':
            return ''.join(['_'+c.lower() if c.isupper() else c for c in s]).lstrip('_')
        else:
            return 'user_dn'

    def invoke(self, soap_body):
        '''Used to invoke an Autodiscover SOAP request
        
        Args:
            soap_request (str): A formatted SOAP XML request body string
            userconfiguration (UserConfiguration): A UserConfiguration object created using the UserConfiguration class

        Raises:
            SoapResponseHasError: Raises an error when unable to parse a SOAP response
        '''
        endpoint = self.userconfiguration.ews_url
        try:
            response = requests.post(
                url=endpoint,
                data=soap_body,
                headers=self.SOAP_REQUEST_HEADER,
                auth=(self.userconfiguration.credentials.email_address, self.userconfiguration.credentials.password),
                verify=True
            )
            parsed_response = BeautifulSoup(response.content, 'xml')
            try:
                if parsed_response.find('ResponseCode').string == 'ErrorAccessDenied':
                    __LOGGER__.info('{}'.format(parsed_response.find('MessageText').string))
                if parsed_response.find('ResponseCode').string == 'NoError':
                    return parsed_response
            except:
                if parsed_response.find('ErrorCode').string == 'NoError':
                    return parsed_response
        except requests.exceptions.HTTPError as errh:
            __LOGGER__.info("An Http Error occurred attempting to connect to {ep}:".format(ep=endpoint) + repr(errh))
        except requests.exceptions.ConnectionError as errc:
            __LOGGER__.info("An Error Connecting to the API occurred attempting to connect to {ep}:".format(ep=endpoint) + repr(errc))
        except requests.exceptions.Timeout as errt:
            __LOGGER__.info("A Timeout Error occurred attempting to connect to {ep}:".format(ep=endpoint) + repr(errt))
        except requests.exceptions.RequestException as err:
            __LOGGER__.info("An Unknown Error occurred attempting to connect to {ep}:".format(ep=endpoint) + repr(err))
        __LOGGER__.warning('Unable to parse response from {current}'.format(current=self.__class__.__name__))
        return None