import requests, re
from .exchangeversion import ExchangeVersion
from .serviceendpoint import ServiceEndpoint
from .userconfiguration import UserConfiguration
from bs4 import BeautifulSoup

class SearchMailboxes(ServiceEndpoint):
    
    SOAP_REQUEST_HEADER = {'content-type': 'text/xml; charset=UTF-8'}

    def __init__(self, search_query, userconfiguration, mailbox_id, search_scope='All'): #credentials=None, autodiscover=True, mailbox_list=None, exchangeVersion=None, ewsurl=None):
        
        self.search_query = search_query

        if (isinstance(userconfiguration, UserConfiguration)):
            self.userconfiguration = userconfiguration
            self.ewsUrl = self.userconfiguration.ewsUrl
            self.exchangeVersion = self.userconfiguration.exchangeVersion
            super(ServiceEndpoint, self).__init__()
        else:
            raise AttributeError('Please provide a UserConfiguration object')

        self.mailbox_list = mailbox_id

        if (search_scope in ['All', 'PrimaryOnly', 'ArchiveOnly']):
            self.search_scope = search_scope
        else:
            raise AttributeError('Please use the default SearchScope of All or specify PrimaryOnly or ArchiveOnly')

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
            for item in value.find_all('SearchPreviewItem'):
                return_dict = {}
                for i in item:
                    if (i.name == 'Id'):
                        return_dict.update({'MessageId': i['Id']})
                    elif (i.name is not None and i.string is not None):
                        return_dict.update({
                            i.name: i.string
                        })
                return_list.append(return_dict)
            self._response = return_list
              

    def invoke(self):
        config = self.userconfiguration
        soap_payload = self.soap(self.mailbox_list)
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
            raise AttributeError('Unable to parse response from SearchMailboxes')


    def soap(self, mailbox):
        mailbox_search_scope = self._mailbox_search_scope(mailbox)
        

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
</soap:Envelope>''' % (self.exchangeVersion, self.search_query, mailbox_search_scope)


    def _mailbox_search_scope(self,  mailbox):
        mailbox_soap_element = ''
        if (isinstance(mailbox, list)):
            for item in mailbox:
                mailbox_soap_element += '''<t:MailboxSearchScope>
        <t:Mailbox>%s</t:Mailbox>
        <t:SearchScope>%s</t:SearchScope>
    </t:MailboxSearchScope>''' % (item, self.search_scope)
        else:
            mailbox_soap_element = '''<t:MailboxSearchScope>
        <t:Mailbox>%s</t:Mailbox>
        <t:SearchScope>%s</t:SearchScope>
    </t:MailboxSearchScope>''' % (mailbox, self.search_scope)

        return mailbox_soap_element



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