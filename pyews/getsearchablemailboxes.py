import requests
from bs4 import BeautifulSoup
from .autodiscover import Autodiscover
from .exchangeversion import ExchangeVersion
from .serviceendpoint import ServiceEndpoint
from .userconfiguration import UserConfiguration

class GetSearchableMailboxes(ServiceEndpoint):

    def __init__(self, userconfiguration):

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
            for item in value.find_all('SearchableMailbox'):
                return_list.append({
                    'ReferenceId': item.ReferenceId.string,
                    'PrimarySmtpAddress': item.PrimarySmtpAddress.string,
                    'DisplayName': item.DisplayName.string,
                    'IsMembershipGroup': item.IsMembershipGroup.string,
                    'IsExternalMailbox': item.IsExternalMailbox.string,
                    'ExternalEmailAddress': item.ExternalEmailAddress.string,
                    'Guid': item.Guid.string
                })
        self._response = return_list

    def invoke(self):
        config = self.userconfiguration
        soap_payload = self.soap()
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
            raise AttributeError('Unable to parse response from GetSearchableMailboxes')

    def soap(self):
        return '''<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types"
               xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages">
   <soap:Header>
      <t:RequestServerVersion Version="%s" />
   </soap:Header>
   <soap:Body >
      <m:GetSearchableMailboxes>
         <m:ExpandGroupMembership>true</m:ExpandGroupMembership>
      </m:GetSearchableMailboxes>
   </soap:Body>
</soap:Envelope>''' % self.exchangeVersion


    def _parse_response(self, parsed_response):
        if parsed_response.find('ResponseCode').string == 'NoError':
            for item in parsed_response.find_all('SearchableMailbox'):
                self.results.append({
                    'ReferenceId': item.ReferenceId.string,
                    'PrimarySmtpAddress': item.PrimarySmtpAddress.string,
                    'DisplayName': item.DisplayName.string,
                    'IsMembershipGroup': item.IsMembershipGroup.string,
                    'IsExternalMailbox': item.IsExternalMailbox.string,
                    'ExternalEmailAddress': item.ExternalEmailAddress.string,
                    'Guid': item.Guid.string
                })

'''
        if credentials is None:
            raise AttributeError('Credentials object is required')
        else:
            self.credentials = credentials

        if exchangeVersion is not None:
            if exchangeVersion in ExchangeVersion.EXCHANGE_VERSIONS:
                self.exchangeVersion = exchangeVersion
            else:
                raise AttributeError('If you are not using Autodiscover then you must provide one of the following exchange versions: %s' % ExchangeVersion.EXCHANGE_VERSIONS)
        else:
            raise AttributeError('If you are not using Autodiscover then you must provide one of the following exchange versions: %s' % ExchangeVersion.EXCHANGE_VERSIONS)

        # setting default results list object
        self.results = []

        if autodiscover:
            self.autodiscover = Autodiscover(self.credentials, self.exchangeVersion)
            self.ewsurl = self.autodiscover.usersettings.ExternalEwsUrl
            self.exchangeVersion = self.autodiscover.usersettings.exchangeVersion
            self._get_searchable_mailboxes()
        else:
            if ewsurl is not None:
                self.ewsurl = ewsurl
            else:
                raise AttributeError('If you are not using Autodiscover then you must provide an ewsurl')
            
            self._get_searchable_mailboxes()

    
    def _get_searchable_mailboxes(self):
        soap_request = self._build_soap_request()
        response = requests.post(self.ewsurl, data=soap_request, headers=self.SOAP_REQUEST_HEADER, auth=(self.credentials.username, self.credentials.password))
        parsed_response = BeautifulSoup(response.content, 'xml')
        self.parse_response(parsed_response)
        
      
    def parse_response(self, parsed_response):
        if parsed_response.find('ResponseCode').string == 'NoError':
            for item in parsed_response.find_all('SearchableMailbox'):
                self.results.append({
                    'ReferenceId': item.ReferenceId.string,
                    'PrimarySmtpAddress': item.PrimarySmtpAddress.string,
                    'DisplayName': item.DisplayName.string,
                    'IsMembershipGroup': item.IsMembershipGroup.string,
                    'IsExternalMailbox': item.IsExternalMailbox.string,
                    'ExternalEmailAddress': item.ExternalEmailAddress.string,
                    'Guid': item.Guid.string
                })

'''
#    def _build_soap_request(self):
#        return '''<?xml version="1.0" encoding="UTF-8"?>
#<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
#               xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types"
#               xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages">
#   <soap:Header>
#      <t:RequestServerVersion Version="%s" />
#   </soap:Header>
#   <soap:Body >
#      <m:GetSearchableMailboxes>
#         <m:ExpandGroupMembership>true</m:ExpandGroupMembership>
#      </m:GetSearchableMailboxes>
#   </soap:Body>
#</soap:Envelope>''' % self.exchangeVersion
