import requests, re
from GetSearchableMailboxes import GetSearchableMailboxes
from exchangeversion import ExchangeVersion
from autodiscover import Autodiscover
from bs4 import BeautifulSoup


class DeleteItem(object):
    
    DELETE_TYPES = ['HardDelete', 'SoftDelete', 'MoveToDeletedItems']
    SOAP_REQUEST_HEADER = {'content-type': 'text/xml; charset=UTF-8'}

    def __init__(self, item, delete_type=DELETE_TYPES[2], credentials=None, autodiscover=True, exchangeVersion=None, ewsurl=None):
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

        if item:
            self.item = item
        else:
            raise AttributeError('You must provide an item to delete.')
        
         # setting default results list object
        self.results = []

        if autodiscover:
            self.autodiscover = Autodiscover(self.credentials, self.exchangeVersion)
            self.ewsurl = self.autodiscover.usersettings.ExternalEwsUrl
            if self.exchangeVersion is not self.autodiscover.usersettings.exchangeVersion:
                self.exchangeVersion = self.autodiscover.usersettings.exchangeVersion
        elif ewsurl is not None:
                self.ewsurl = ewsurl
        else:
            raise AttributeError('You must either use autodiscover or provide a mailbox_list')
            
        if delete_type in self.DELETE_TYPES:
            self.delete_type = delete_type
        else:
            raise AttributeError('You must provide one of the following delete types: %s' % self.DELETE_TYPES)

        self._delete_item()
       
    def _delete_item(self):
        soap_request = self._build_soap_request()
        response = requests.post(self.ewsurl, data=soap_request, headers=self.SOAP_REQUEST_HEADER, auth=(self.credentials.username, self.credentials.password))
        parsed_response = BeautifulSoup(response.content, 'xml')
        self.parse_response(parsed_response)


    def parse_response(self, parsed_response):
        if parsed_response.find('ResponseCode').string != 'NoError':
            for item in parsed_response.find_all('DeleteItemResponseMessage'):
                self.results.append({
                    'MessageText': item.MessageText.string,
                    'ResponseCode': item.ResponseCode.string,
                    'DescriptiveLinkKey': item.DescriptiveLinkKey.string
                })
        else:
            self.results.append({
                'MessageText': 'Succesfull'
            })

    def _build_soap_request(self):
        item_soap_element = ''
        if isinstance(self.item, basestring):
            item_soap_element = self._build_item_soap_element(self.item)
        else:
            for one in self.item:
                print(one)
                item_soap_element += self._build_item_soap_element(one)

        return '''<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types"
               xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages">
   <soap:Header>
      <t:RequestServerVersion Version="%s" />
   </soap:Header>
   <soap:Body >
    <DeleteItem DeleteType="%s" xmlns="http://schemas.microsoft.com/exchange/services/2006/messages">
      <ItemIds>
        %s
      </ItemIds>
    </DeleteItem>
  </soap:Body>
</soap:Envelope>''' % (self.exchangeVersion, self.delete_type, item_soap_element)

    def _build_item_soap_element(self, item):
        return '''<t:ItemId Id="%s"/>''' % item