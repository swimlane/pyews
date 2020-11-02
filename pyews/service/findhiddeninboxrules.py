import requests
from bs4 import BeautifulSoup

from .serviceendpoint import ServiceEndpoint
from pyews.utils.exceptions import ObjectType, SoapResponseHasError, SoapAccessDeniedError


class FindHiddenInboxRules (ServiceEndpoint):
    '''Child class of doc:`serviceendpoint` that retrieves hidden inbox (mailbox) rules for a users email address specificed by impersonation headers.
    
    Examples:
        To use any service class you must provide a :doc:`../configuration/userconfiguration` object first.
        Like all service classes, you can access formatted properties from the EWS endpoint using the `response` property.
        
        If you want to retrieve the inbox rules for a specific email address you must provide it when creating a GetInboxRules object.
            
        .. code-block:: python
           from pyews import UserConfiguration
           from pyews import GetInboxRules
           
           userConfig = UserConfiguration(
               'first.last@company.com',
               'mypassword123'
           )

           inboxRules = GetInboxRules('first.last@company.com', userConfig, hidden_rules=True)

    Args:
        userconfiguration (UserConfiguration): A :doc:`../configuration/userconfiguration` object created using the UserConfiguration class

    Raises:
        SoapAccessDeniedError: Access is denied when attempting to use Exchange Web Services endpoint
        SoapResponseHasError: An error occurred when parsing the SOAP response
        ObjectType: An incorrect object type has been used
    '''
    
    def __init__(self, userconfiguration):
        super(FindHiddenInboxRules, self).__init__(userconfiguration)
        self._soap_request = self.soap()
        self.invoke(self._soap_request)
        self.response = self.raw_soap

    def __process_rule_properties(self, item):
        if item:
            return_dict = {}
            for prop in item:
                if prop.name != 'Conditions' and prop.name != 'Actions':
                    if prop.name not in return_dict:
                        return_dict[prop.name] = prop.string
            for condition in item.find('Conditions'):
                if 'conditions' not in return_dict:
                    return_dict['conditions'] = []
                return_dict['conditions'].append({
                    condition.name: condition.string
                })
            for action in item.find('Actions'):
                if 'actions' not in return_dict:
                    return_dict['actions'] = []
                return_dict['actions'].append({
                    action.name: action.string
                })
            return return_dict

    @property
    def response(self):
        '''GetInboxRules SOAP response
        
        Returns:
            list: Returns a formatted list of dictionaries of a SOAP response
        '''
        return self._response

    @response.setter
    def response(self, value):
        '''Creates and sets a response object
        
        Args:
            value (str): The raw response from a SOAP request
        '''
        return_list = []
        if value.find('ResponseCode').string == 'NoError':
            for item in value.find('InboxRules'):
                if item.name == 'Rule' and item:
                    return_list.append(self.__process_rule_properties(item))
            self._response = return_list

    def soap(self):
        '''Creates the SOAP XML message body

        Returns:
            str: Returns the SOAP XML request body
        '''
        if (self.userconfiguration.impersonation):
            impersonation_header = self.userconfiguration.impersonation.header
        else:
            impersonation_header = ''

        return '''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages"
        xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types"
        xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Header>
    <t:RequestServerVersion Version="{version}" />
    {header}
  </soap:Header>
  <soap:Body>
    <m:FindItem Traversal="Shallow">
        <m:ItemShape>
            <t:BaseShape>IdOnly</t:BaseShape>
            <t:AdditionalProperties>
                <t:ExtendedFieldURI PropertyTag="0x65EC" PropertyType="String" />
                <t:ExtendedFieldURI PropertyTag="0x0E99" PropertyType="Binary" />
                <t:ExtendedFieldURI PropertyTag="0x0E9A" PropertyType="Binary" />
                <t:ExtendedFieldURI PropertyTag="0x65E9" PropertyType="Integer" />
                <t:ExtendedFieldURI PropertyTag="0x6800" PropertyType="String" />
                <t:ExtendedFieldURI PropertyTag="0x65EB" PropertyType="String" />
                <t:ExtendedFieldURI PropertyTag="0x3FEA" PropertyType="Boolean" />
                <t:ExtendedFieldURI PropertyTag="0x6645" PropertyType="Binary" />
            </t:AdditionalProperties>
        </m:ItemShape>
        <m:Restriction>
            <t:IsEqualTo>
                <t:FieldURI FieldURI="item:ItemClass" />
                <t:FieldURIOrConstant>
                    <t:Constant Value="IPM.Rule.Version2.Message" />
                </t:FieldURIOrConstant>
            </t:IsEqualTo>
      </m:Restriction>
    <m:ParentFolderIds>
        <t:DistinguishedFolderId Id="inbox" />
    </m:ParentFolderIds>
    </m:FindItem>
  </soap:Body>
</soap:Envelope>
        '''.format(version=self.userconfiguration.exchangeVersion, header=impersonation_header)