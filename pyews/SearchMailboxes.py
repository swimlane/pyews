import requests, re
from .getsearchablemailboxes import GetSearchableMailboxes
from .exchangeversion import ExchangeVersion
from .autodiscover import Autodiscover
from bs4 import BeautifulSoup

class SearchMailboxes(object):
    
    SOAP_REQUEST_HEADER = {'content-type': 'text/xml; charset=UTF-8'}

    def __init__(self, search_query, credentials=None, autodiscover=True, mailbox_list=None, exchangeVersion=None, ewsurl=None):
        if credentials is None:
            raise AttributeError('Credentials object is required')
        else:
            self.credentials = credentials

        if exchangeVersion is None:
            raise AttributeError('At this time you must supply a value to exchangeVersion')
        else:
            if exchangeVersion in ExchangeVersion.EXCHANGE_VERSIONS:
                self.exchangeVersion = exchangeVersion
            else:
                raise AttributeError('You must provide one of the following exchange versions: %s' % ExchangeVersion.EXCHANGE_VERSIONS)

        if search_query:
            self.search_query = search_query
        else:
            raise AttributeError('You must provife a search query')
        
         # setting default results list object
        self.results = []

        if mailbox_list is None:
            if autodiscover:
                self.autodiscover = Autodiscover(self.credentials, self.exchangeVersion)
                self.ewsurl = self.autodiscover.usersettings.ExternalEwsUrl
                if self.exchangeVersion is not self.autodiscover.usersettings.exchangeVersion:
                    self.exchangeVersion = self.autodiscover.usersettings.exchangeVersion
                self.mailbox_list = GetSearchableMailboxes(credentials=self.credentials, exchangeVersion=self.exchangeVersion)
            elif ewsurl is not None:
                    self.ewsurl = ewsurl
                    self.mailbox_list = GetSearchableMailboxes(credentials=self.credentials, ewsurl=self.ewsurl)
            else:
                raise AttributeError('You must either use autodiscover or provide a mailbox_list')
        else:
            self.mailbox_list = mailbox_list
            if ewsurl is not None:
                self.ewsurl = ewsurl
            else:
                raise AttributeError('You must either use Autodiscover or provide a EWS Url')
            
        self._search_mailboxes()
       

    def _search_mailboxes(self):
        headers = {'content-type': 'text/xml; charset=UTF-8'}
        soap_request = self._build_soap_request()
        response = requests.post(self.ewsurl, data=soap_request, headers=headers, auth=(self.credentials.username, self.credentials.password))
        parsed_response = BeautifulSoup(response.content, 'xml')
        self.parse_response(parsed_response)


    def parse_response(self, parsed_response):
       # print(parsed_response)
        if parsed_response.find('ResponseCode').string == 'NoError':
            for item in parsed_response.find_all('SearchPreviewItem'):
                #print(item)
                self.results.append({
                    'Id': item.Id['Id'],
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


    def _build_soap_request(self):
        mailbox_soap_element = ''
        if isinstance(self.mailbox_list, GetSearchableMailboxes):
            for mailbox in self.mailbox_list.results:
                mailbox_soap_element += self._build_mailboxes_soap_element(mailbox['ReferenceId'])
        else:
            for mailbox in self.mailbox_list:
                mailbox_soap_element += self._build_mailboxes_soap_element(mailbox)
                

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
</soap:Envelope>''' % (self.exchangeVersion, self.search_query, mailbox_soap_element)

    def _build_mailboxes_soap_element(self, mailbox):
        return '''<t:MailboxSearchScope>
    <t:Mailbox>%s</t:Mailbox>
    <t:SearchScope>All</t:SearchScope>
</t:MailboxSearchScope>''' % mailbox