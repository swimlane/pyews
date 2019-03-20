import requests, re
from .serviceendpoint import ServiceEndpoint
from .userconfiguration import UserConfiguration
from .exchangeversion import ExchangeVersion
from bs4 import BeautifulSoup


class DeleteItem(ServiceEndpoint):
    
    DELETE_TYPES = ['HardDelete', 'SoftDelete', 'MoveToDeletedItems']

    def __init__(self, item, userconfiguration, delete_type=DELETE_TYPES[2]):

        self.item = item

        if (isinstance(userconfiguration, UserConfiguration)):
            self.userconfiguration = userconfiguration
            self.ewsUrl = self.userconfiguration.ewsUrl
            self.exchangeVersion = self.userconfiguration.exchangeVersion
            super(ServiceEndpoint, self).__init__()
        else:
            raise AttributeError('Please provide a UserConfiguration object')

        if delete_type in self.DELETE_TYPES:
            self.delete_type = delete_type
        else:
            raise AttributeError('You must provide one of the following delete types: %s' % self.DELETE_TYPES)

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
        response_dict = {}
        if value.find('ResponseCode').string != 'NoError':
            for item in value.find_all('DeleteItemResponseMessage'):
                response_dict.append({
                    'MessageText': item.MessageText.string,
                    'ResponseCode': item.ResponseCode.string,
                    'DescriptiveLinkKey': item.DescriptiveLinkKey.string
                })
        else:
            response_dict.append({
                'MessageText': 'Succesfull'
            })
        self._response = response_dict      


    def invoke(self):
        config = self.userconfiguration
        soap_payload = self.soap(self.item)
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


    def soap(self, item):
        delete_item_soap_element = self._delete_item_soap_string(item)
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
</soap:Envelope>''' % (self.exchangeVersion, self.delete_type, delete_item_soap_element)
        

    def _delete_item_soap_string(self, item):
        item_soap_string = ''
        if (isinstance(item, list)):
            for i in item:
                item_soap_string += '''<t:ItemId Id="%s"/>''' % i
        else:
            item_soap_string = '''<t:ItemId Id="%s"/>''' % item
        return item_soap_string


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

   