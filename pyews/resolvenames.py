from .serviceendpoint import ServiceEndpoint
#import userconfiguration as UserConfiguration
from .userconfiguration import UserConfiguration
from bs4 import BeautifulSoup
import requests


class ResolveNames(ServiceEndpoint):

    def __init__(self, userconfiguration):
        if (isinstance(userconfiguration, UserConfiguration)):
            self.userconfiguration = userconfiguration
            super(ServiceEndpoint, self).__init__()
        else:
            raise AttributeError('Please provide a UserConfiguration object')

        self._response = ''
        self.invoke()

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, value):
        self._response = value

    def invoke(self):
        config = self.userconfiguration
        soap_payload = self.soap(config.credentials.email_address)
        r = requests.post(
            config.ewsUrl,
            data=soap_payload, 
            headers=self.SOAP_REQUEST_HEADER, 
            auth=(config.credentials.email_address, config.credentials.password)
        )
        parsed_response = BeautifulSoup(r.content, 'xml')
        if parsed_response.find('ResponseCode').string == 'NoError':
            self.response = parsed_response
        else:
            return False

    def soap(self, email_address):
        return '''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:a="http://schemas.microsoft.com/exchange/2010/Autodiscover"      
               xmlns:wsa="http://www.w3.org/2005/08/addressing" 
               xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"      
               xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <ResolveNames xmlns="http://schemas.microsoft.com/exchange/services/2006/messages"
                  xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types"
                  ReturnFullContactData="true">
      <UnresolvedEntry>%s</UnresolvedEntry>
    </ResolveNames>
  </soap:Body>
</soap:Envelope>
        ''' % email_address