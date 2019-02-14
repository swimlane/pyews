import requests
from xml.etree import ElementTree
import xmltodict, json
from autodiscover import Autodiscover

class GetSearchableMailboxes(object):
    
    def __init__(self, credentials=None, autodiscover=True, exchangeVersion='Office365', ews_url=None):
        if not credentials:
            raise AttributeError('Credentials object is required')
        if autodiscover:
            autodiscover = Autodiscover(credentials=credentials, exchangeVersion=exchangeVersion)
            self._get_searchable_mailboxes(autodiscover, credentials)
        elif ews_url is not None:
            self._get_searchable_mailboxes(credentials=credentials, ewsurl=ews_url)
        else:
            raise AttributeError('You must provide either an Autodiscover object or a ews_url')


    def _get_searchable_mailboxes(self, autodiscover, credentials, exchangeVersion=None, ewsurl=None,):
        if ewsurl is None:
            ewsurl = autodiscover.usersettings.ExternalEwsUrl

        if exchangeVersion is None:
            exchangeVersion = autodiscover.usersettings.exchangeVersion

        headers = {'content-type': 'text/xml; charset=UTF-8'}
        soap_request = self._build_soap_request(exchangeVersion)
        response = requests.post(ewsurl, data=soap_request, headers=headers, auth=(credentials.username, credentials.password))
        self.parse_response(response.content)
      
    def parse_response(self, content):
        self.searchable_mailboxes = []
        response_dict = xmltodict.parse(content)
        if response_dict['s:Envelope']['s:Body']['GetSearchableMailboxesResponse']['ResponseCode'] == 'NoError':
            for mailboxes in response_dict['s:Envelope']['s:Body']['GetSearchableMailboxesResponse']['SearchableMailboxes']['SearchableMailbox']:
                self.searchable_mailboxes.append({
                    'ReferenceId': mailboxes['ReferenceId'],
                    'PrimarySmtpAddress': mailboxes['PrimarySmtpAddress'],
                    'DisplayName': mailboxes['DisplayName'],
                    'IsMembershipGroup': mailboxes['IsMembershipGroup'],
                    'IsExternalMailbox': mailboxes['IsExternalMailbox'],
                    'ExternalEmailAddress': mailboxes['ExternalEmailAddress'],
                    'Guid': mailboxes['Guid']
                })
                


    def _build_soap_request(self, exchangeVersion):
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
</soap:Envelope>''' % exchangeVersion

    