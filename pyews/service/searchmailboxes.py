import requests, re
from bs4 import BeautifulSoup

from .serviceendpoint import ServiceEndpoint
from pyews.utils.exchangeversion import ExchangeVersion
from pyews.utils.exceptions import ObjectType, DeleteTypeError, SoapResponseHasError, SoapAccessDeniedError


class SearchMailboxes(ServiceEndpoint):
    
    def __init__(self, search_query, userconfiguration, mailbox_id, search_scope='All'):
        '''Child class of ServiceEndpoint that is used to search mailboxes based on a search query, UserConfiguration object, and a single or list of mailbox ReferenceId's.  
        
        Args:
            search_query (str): A EWS QueryString.  More information can be found at https://docs.microsoft.com/en-us/exchange/client-developer/web-service-reference/querystring-querystringtype
            userconfiguration (UserConfiguration): A UserConfiguration object created using the UserConfiguration class
            mailbox_id (str or list): A single or list of mailbox IDs to search.  This mailbox id is a ReferenceId
            search_scope (str, optional): Defaults to 'All'. The search scope for the provided mailbox ids.  The options are ['All', 'PrimaryOnly', 'ArchiveOnly']
        
        Raises:
            ObjectType: An incorrect object type has been used
            SearchScopeError: The provided search scope is not one of the following options: ['All', 'PrimaryOnly', 'ArchiveOnly']
        '''

        self.search_query = search_query
        
        super(SearchMailboxes, self).__init__(userconfiguration)

        self.mailbox_list = mailbox_id

        if (search_scope in ['All', 'PrimaryOnly', 'ArchiveOnly']):
            self.search_scope = search_scope
        else:
            raise SearchScopeError('Please use the default SearchScope of All or specify PrimaryOnly or ArchiveOnly')

        self.invoke()

        
    @property
    def raw_soap(self):
        '''Returns the raw SOAP response
        
        Returns:
            str: Raw SOAP XML response
        '''
        return self._raw_soap

    @raw_soap.setter
    def raw_soap(self, value):
        '''Sets the raw soap and response from a SOAP request
        
        Args:
            value (str): The response from a SOAP request
        '''
        self.response = value
        self._raw_soap = value

    @property
    def response(self):
        '''Formatted response from SearchMailboxes endpoint.  A list is returned of all identified messages matching search query.
        
        Returns:
            str: Returns the SearchMailboxes response
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
        '''Used to invoke a SearchMailboxes SOAP request
        
        Raises:
            SoapResponseHasError: Raises an error when unable to parse a SOAP response
        '''

        soap_payload = self.soap(self.mailbox_list)
        r = requests.post(
            self.userconfiguration.ewsUrl,
            data=soap_payload, 
            headers=self.SOAP_REQUEST_HEADER, 
            auth=(self.userconfiguration.credentials.email_address, self.userconfiguration.credentials.password)
        )
        parsed_response = BeautifulSoup(r.content, 'xml')
        if parsed_response.find('ResponseCode').string == 'NoError':
            self.raw_soap = parsed_response
        elif parsed_response.find('ResponseCode').string == 'ErrorAccessDenied':
            raise SoapAccessDeniedError('%s' % parsed_response.find('MessageText').string)
        else:
            raise SoapResponseHasError('Unable to parse response from SearchMailboxes')


    def soap(self, mailbox):
        '''Creates the SOAP XML message body

        Args:
            mailbox (str or list): A single or list of email mailbox ReferenceIds to search

        Returns:
            str: Returns the SOAP XML request body
        '''
        if (self.userconfiguration.impersonation):
            impersonation_header = self.userconfiguration.impersonation.header
        else:
            impersonation_header = ''

        mailbox_search_scope = self._mailbox_search_scope(mailbox)

        return '''<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types"
               xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages">
   <soap:Header>
      <t:RequestServerVersion Version="%s" />
      %s
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
</soap:Envelope>''' % (self.userconfiguration.exchangeVersion, impersonation_header, self.search_query, mailbox_search_scope)


    def _mailbox_search_scope(self,  mailbox):
        '''Creates a MailboxSearchScope XML element from a single or list of mailbox ReferenceIds

        Returns:
            str: Returns the MailboxSearchScope SOAP XML element(s)
        '''
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