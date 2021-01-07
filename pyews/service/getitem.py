import uuid
import json
import xmltodict
from collections import OrderedDict
from ..core import Core
from pyews.utils.exceptions import ObjectType, SoapResponseHasError, SoapAccessDeniedError


class GetItem(Core):

    def __init__(self, userconfiguration):
        super(GetItem, self).__init__(userconfiguration)

    def __camel_to_snake(self, s):
        return ''.join(['_'+c.lower() if c.isupper() else c for c in s]).lstrip('_')

    def __process_keys(self, key):
        return_value = key.replace('t:','')
        if return_value.startswith('@'):
            return_value = return_value.lstrip('@')
        return self.__camel_to_snake(return_value)

    def __process_dict(self, obj):
        if isinstance(obj, dict):
            obj = {
                self.__process_keys(key): self.__process_dict(value) for key, value in obj.items()
                }
        return obj

    def __process_single_calendar_item(self, value):
        ordered_dict = xmltodict.parse(str(value))
        item_dict = json.loads(json.dumps(ordered_dict))
        return self.__process_dict(item_dict)

    def __parse_response(self, value):
        return_dict = {}
        if value.find('ResponseCode').string == 'NoError':
            for item_type in ['CalendarItem', 'Contact', 'Message', 'Item']:
                if value.find(item_type):
                    for item in getattr(value.find('Items'), item_type):
                        return_dict.update(self.__process_single_calendar_item(item))
                    return return_dict

    def run(self, item_id, change_key=None):
        return self.__parse_response(self.invoke(self.soap(item_id, change_key=change_key)))

    def soap(self, item_id, change_key=None):
        '''Creates the SOAP XML message body

        Args:
            email_address (str): A single email addresses you want to GetInboxRules for

        Returns:
            str: Returns the SOAP XML request body
        '''
        if self.userconfiguration.impersonation:
            impersonation_header = self.userconfiguration.impersonation.header
        else:
            impersonation_header = ''

        if change_key:
            item_id_string = '<t:ItemId Id="{item_id}" ChangeKey="{change_key}"/>'.format(
                item_id=item_id,
                change_key=change_key
            )
        else:
            item_id_string = '<t:ItemId Id="{item_id}"/>'.format(
                item_id=item_id
            )

        return '''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
               xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types"
               xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages">
    <soap:Header>
        <t:RequestServerVersion Version="{version}"/>
    </soap:Header>
    <soap:Body>
        <GetItem xmlns="http://schemas.microsoft.com/exchange/services/2006/messages">
            <ItemShape>
                <t:BaseShape>AllProperties</t:BaseShape>
                <t:IncludeMimeContent>true</t:IncludeMimeContent>
                <t:ConvertHtmlCodePageToUTF8>false</t:ConvertHtmlCodePageToUTF8>
            </ItemShape>
            <ItemIds>
                {item_id_string}
            </ItemIds>
        </GetItem>
    </soap:Body>
</soap:Envelope>'''.format(
    version=self.userconfiguration.exchange_version,
    item_id_string=item_id_string)

