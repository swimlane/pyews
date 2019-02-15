import requests
from bs4 import BeautifulSoup
from autodiscover import Autodiscover
from exchangeversion import ExchangeVersion

class GetSearchableMailboxes(object):
    
    SOAP_REQUEST_HEADER = {'content-type': 'text/xml; charset=UTF-8'}

    def __init__(self, credentials=None, autodiscover=True, exchangeVersion=None, ewsurl=None):
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


    def _build_soap_request(self):
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

    