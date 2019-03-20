#from userconfiguration import UserConfiguration
#from pyews.userconfiguration import UserConfiguration
#from .userconfiguration import UserConfiguration
#from .userconfiguration import UserConfiguration as UC
#import userconfiguration as UserConfiguration
#import userconfiguration as UC
#import userconfiguration as UC

from pyews import userconfiguration as UC
#print(UC)
from bs4 import BeautifulSoup

class ServiceEndpoint(object):
    
    SOAP_REQUEST_HEADER = {'content-type': 'text/xml; charset=UTF-8'}

    def __init__(self, userconfiguration):
        self.userconfiguration = userconfiguration

        self.results = []
        
    @property
    def userconfiguration(self):
        return self._userconfiguration

    @userconfiguration.setter
    def userconfiguration(self, config):
        if isinstance(config, UC.UserConfiguration):
            self._userconfiguration = config


    def invoke_soap_request(self, soap_request, url, username, password):
        try:
            _response = requests.post(
                url, 
                data=soap_request, 
                headers=self.SOAP_REQUEST_HEADER, 
                auth=(username, password)
            )
        except:
            raise AttributeError('Unable to make SOAP request')

        self.response = _response

    @property
    def response(self):
        return BeautifulSoup(self.response.content, 'xml')

    @response.setter
    def response(self):
        raise NotImplementedError()

    def parse_response(self, scope, keys, error_key, error_value):
        parsed_response = self.get_response()

        if parsed_response.find(error_key).string == error_value:
            return parsed_response.find_all(scope)
   