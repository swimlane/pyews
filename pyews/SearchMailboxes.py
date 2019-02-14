import requests, re
from xml.etree import ElementTree
from GetSearchableMailboxes import GetSearchableMailboxes
from autodiscover import Autodiscover
import xmltodict, json
from xml.sax.saxutils import escape

from bs4 import BeautifulSoup

__SEARCHABLE_EMAIL_PROPERTIES__ = ['attachmentnames:', 'bcc:', 'cc:', 'from:', 'hasattachment:', 'isread:', 'kind:', 'participants:', 'received:', 'recipients:', 'sent:', 'size:', 'to:']
__SEARCHABLE_SENSITIVE_DATA_TYPES__ = ['']

class SearchMailboxes(object):
    
    ENDPOINT_NAME = 'SearchMailboxes'
    _illegal_xml_chars_RE = re.compile(u'[\x00-\x08\x0b\x0c\x0e-\x1F\uD800-\uDFFF\uFFFE\uFFFF]')
    escape_xml_pattern = re.compile(ur'[^\x09\x0A\x0D\x20-\x7E\x85\xA0-\xFF\u0100-\uD7FF\uE000-\uFDCF\uFDE0-\uFFFD]')

    def __init__(self, search_query, mailbox_list=None, credentials=None, autodiscover=True, exchangeVersion=None, ewsurl=None):
        if not credentials:
            raise AttributeError('Credentials object is required')
        else:
            self.credentials = credentials

        if not search_query:
            raise AttributeError('Please provide a search query')
        else:
            self.search_query = search_query

        
        if autodiscover:
            autodiscover = Autodiscover(credentials=credentials)
            mailbox_list = GetSearchableMailboxes(credentials=credentials).searchable_mailboxes
            self.ewsurl = autodiscover.usersettings.ExternalEwsUrl
            self.exchangeVersion = autodiscover.usersettings.exchangeVersion
        elif ewsurl:
            mailbox_list = GetSearchableMailboxes(credentials=credentials, ews_url=ewsurl).searchable_mailboxes
            self.ewsurl = ewsurl
            self.exchangeVersion = exchangeVersion
        else:
            raise AttributeError('You must either use Autodiscover or provide a EWS Url')

        if mailbox_list is None:
            raise AttributeError('You must provide mailboxes to search or use the default action of Autodiscover and use GetSearchableMailboxes')

        self.search_results = []
        self._search_mailboxes(mailbox_list, credentials)
       

    def _search_mailboxes(self, mailboxes, credentials):
        headers = {'content-type': 'text/xml; charset=UTF-8'}
        soap_request = self._build_soap_request(mailboxes, self.exchangeVersion)
        response = requests.post(self.ewsurl, data=soap_request, headers=headers, auth=(credentials.username, credentials.password))
        parsed_response = BeautifulSoup(response.content, 'xml')
        self.parse_response(parsed_response)

    def get_property_name(self, prop):
        return "%sprop" % self.ENDPOINT_NAME

    def parse_response(self, parsed_response):
        if parsed_response.find('ResponseCode').string == 'NoError':
            for item in parsed_response.find_all('SearchPreviewItem'):
                self.search_results.append({
                    'Id': item.Id.string,
                    'MailboxId': item.Mailbox.MailboxId.string,
                    'PrimarySmtpAddress': item.Mailbox.PrimarySmtpAddress.string,
                    'UniqueHash': item.UniqueHash.string,
                    'OwaLink': item.OwaLink.string,
                    'Sender': item.Sender.string,
                    'ToRecipients': item.ToRecipients.string,
                    'CreatedTime': item.CreatedTime.string,
                    'ReceivedTime': item.ReceivedTime.string,
                    'SentTime': item.SentTime.string,
                    'Subject': item.Subject.string,
                    'Size': item.Size.string,
                    'Read': item.Read.string,
                    'HasAttachment': item.HasAttachment.string
                })


    def _build_soap_request(self, mailboxes, exchangeVersion):
        mailbox_soap_element = ''
        for mailbox in mailboxes:
            mailbox_soap_element += self._build_mailboxes_soap_element(mailbox['ReferenceId'])
                

        return '''<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types"
               xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages">
   <soap:Header>
      <t:RequestServerVersion Version="%s" />
   </soap:Header>
   <soap:Body >
      <m:SearchMailboxes>
         <m:SearchQueries>
            <t:MailboxQuery>
               <t:Query>%s</t:Query>
               <t:MailboxSearchScopes>
                  %s
               </t:MailboxSearchScopes>
            </t:MailboxQuery>
         </m:SearchQueries>
         <m:ResultType>PreviewOnly</m:ResultType>
      </m:SearchMailboxes>
   </soap:Body>
</soap:Envelope>''' % (exchangeVersion, self.search_query, mailbox_soap_element)

    def _build_mailboxes_soap_element(self, mailbox):
        return '''<t:MailboxSearchScope>
    <t:Mailbox>%s</t:Mailbox>
    <t:SearchScope>All</t:SearchScope>
</t:MailboxSearchScope>''' % mailbox