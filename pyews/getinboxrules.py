from pyews.serviceendpoint import ServiceEndpoint
from .userconfiguration import UserConfiguration
from bs4 import BeautifulSoup
import requests

class GetInboxRules (ServiceEndpoint):

    def __init__(self, smtp_address, userconfiguration):

        self.email_address = smtp_address

        if (isinstance(userconfiguration, UserConfiguration)):
            self.userconfiguration = userconfiguration
            super(ServiceEndpoint, self).__init__()
        else:
            raise AttributeError('Please provide a UserConfiguration object')
            
        self.ewsUrl = self.userconfiguration.ewsUrl
        self.exchangeVersion = self.userconfiguration.exchangeVersion

        self.invoke()

    @property
    def raw_soap(self):
        return self._raw_soap

    @raw_soap.setter
    def raw_soap(self, value):
        self.response = value
        self._raw_soap = value

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, value):
        return_list = []
        if value.find('ResponseCode').string == 'NoError':
            for item in value.find('Rule'):
                return_dict = {}
                if (item.name == 'Conditions'):
                    for child in item.descendants:
                        if (child.name is not None and child.string is not None):
                            return_dict.update({
                                child.name: child.string
                            })
                if (item.name == 'Actions'):
                    for child in item.descendants:
                        if (child.name is not None and child.string is not None):
                            return_dict.update({
                                child.name: child.string
                            })
                else:
                    return_dict.update({
                        item.name: item.string
                    })
                    
                return_list.append(return_dict)
            self._response = return_list
               

    def invoke(self):
        config = self.userconfiguration
        soap_payload = self.soap(self.email_address)
        r = requests.post(
            self.ewsUrl,
            data=soap_payload, 
            headers=self.SOAP_REQUEST_HEADER, 
            auth=(config.credentials.email_address, config.credentials.password)
        )
        parsed_response = BeautifulSoup(r.content, 'xml')
        if parsed_response.find('ResponseCode').string == 'NoError':
            self.raw_soap = parsed_response
        else:
            raise AttributeError('Unable to parse response from GetInboxRules')


    def soap(self, email_address):
        return '''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages"
        xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types"
        xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Header>
    <t:RequestServerVersion Version="%s" />
  </soap:Header>
  <soap:Body>
    <m:GetInboxRules>
      <m:MailboxSmtpAddress>%s</m:MailboxSmtpAddress>
    </m:GetInboxRules>
  </soap:Body>
</soap:Envelope>
        ''' % (self.exchangeVersion, email_address)