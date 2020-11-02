import requests, re
from bs4 import BeautifulSoup

from .serviceendpoint import ServiceEndpoint
from pyews.utils.exchangeversion import ExchangeVersion
from pyews.utils.exceptions import ObjectType, DeleteTypeError, SoapResponseHasError, SoapAccessDeniedError, SearchScopeError


class SearchMailboxes(ServiceEndpoint):
    '''Child class of :doc:`serviceendpoint` that is used to search mailboxes based on a search query, :doc:`../configuration/userconfiguration` object, and a single or list of mailbox ReferenceId's.  
        
        Examples:
            To use any service class you must provide a :doc:`../configuration/userconfiguration` object first.
            Like all service classes, you can access formatted properties from the EWS endpoint using the `response` property.
            
            The search query parameter takes a specific format, below are examples of different situations as well as comments that explain that situation:

            .. code-block:: guess
                   
                   # Searching for a keyword in a subject
                   # You can specify the word you are looking for as either `account` or `Account`
                   searchQuery = 'subject:account'

                   # Searching for an exact string in a subject
                   searchQuery = 'subject:"Your Account is about to expire"'

                   # Searching for a url in a email's body
                   searchQuery = 'body:"https://google.com"'

                   # You can combine your search query by adding grouping logical operators
                   # Here is an example of searching for two subject strings and a body string match
                   searchQuery = 'subject:(account OR phishing) AND body:"https://google.com"'

            For more information take a look at Microsoft's documentation for their= `Advanced Query Syntax (AQS) <https://docs.microsoft.com/en-us/exchange/client-developer/web-service-reference/querystring-querystringtype>`_

            
            By passing in a search_query, :doc:`../configuration/userconfiguration` object, and a mailbox_id we can search that specific mailbox or a list of mailbox referenceIds

            .. code-block:: python
               from pyews import UserConfiguration
               from pyews import SearchMailboxes

               userConfig = UserConfiguration(
                   'first.last@company.com',
                   'mypassword123'
               )
        
               referenceId = '/o=ExchangeLabs/ou=Exchange Administrative Group (FYDIBOHF23SPDLT)/cn=Recipients/cn=5341a4228e8c433ba81b4b4b6d75e100-last.first'
               searchResults = SearchMailboxes('subject:account', userConfig, referenceId)

        Args:
            search_query (str): A EWS QueryString.  More information can be found at https://docs.microsoft.com/en-us/exchange/client-developer/web-service-reference/querystring-querystringtype
            userconfiguration (UserConfiguration): A :doc:`../configuration/userconfiguration` object created using the :doc:`../configuration/userconfiguration` class
            mailbox_id (str or list): A single or list of mailbox IDs to search.  This mailbox id is a ReferenceId
            search_scope (str, optional): Defaults to 'All'. The search scope for the provided mailbox ids.  The options are ['All', 'PrimaryOnly', 'ArchiveOnly']
        
        Raises:
            ObjectType: An incorrect object type has been used
            SearchScopeError: The provided search scope is not one of the following options: ['All', 'PrimaryOnly', 'ArchiveOnly']
        '''

    def __init__(self, search_query, userconfiguration, mailbox_id, search_scope='All'):

        self.search_query = search_query
        
        super(SearchMailboxes, self).__init__(userconfiguration)

        self.mailbox_list = mailbox_id

        if (search_scope in ['All', 'PrimaryOnly', 'ArchiveOnly']):
            self.search_scope = search_scope
        else:
            raise SearchScopeError('Please use the default SearchScope of All or specify PrimaryOnly or ArchiveOnly')

        self._soap_request = self.soap(self.mailbox_list)
        self.invoke(self._soap_request)
        self.response = self.raw_soap

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
              

    def soap(self, mailbox):
        '''Creates the SOAP XML message body

        Args:
            mailbox (str or list): A single or list of email mailbox ReferenceIds to search

        Returns:
            str: Returns the SOAP XML request body
        '''
        if self.userconfiguration.impersonation:
            impersonation_header = self.userconfiguration.impersonation.header
        else:
            impersonation_header = ''

        mailbox_search_scope = self._mailbox_search_scope(mailbox)

        return '''<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types"
               xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages">
   <soap:Header>
      <t:RequestServerVersion Version="{version}" />
      {header}
   </soap:Header>
   <soap:Body >
      <m:SearchMailboxes>
         <m:SearchQueries>
            <t:MailboxQuery>
               <t:Query>{query}</t:Query>
               <t:MailboxSearchScopes>
                  {scope}
               </t:MailboxSearchScopes>
            </t:MailboxQuery>
         </m:SearchQueries>
         <m:ResultType>PreviewOnly</m:ResultType>
      </m:SearchMailboxes>
   </soap:Body>
</soap:Envelope>'''.format(version=self.userconfiguration.exchangeVersion, header=impersonation_header, query=self.search_query, scope=mailbox_search_scope)


    def _mailbox_search_scope(self,  mailbox):
        '''Creates a MailboxSearchScope XML element from a single or list of mailbox ReferenceIds

        Returns:
            str: Returns the MailboxSearchScope SOAP XML element(s)
        '''
        mailbox_soap_element = ''
        if isinstance(mailbox, list):
            for item in mailbox:
                mailbox_soap_element += '''<t:MailboxSearchScope>
        <t:Mailbox>{mailbox}</t:Mailbox>
        <t:SearchScope>{scope}</t:SearchScope>
    </t:MailboxSearchScope>'''.format(mailbox=item, scope=self.search_scope)
        else:
            mailbox_soap_element = '''<t:MailboxSearchScope>
        <t:Mailbox>{mailbox}</t:Mailbox>
        <t:SearchScope>{scope}</t:SearchScope>
    </t:MailboxSearchScope>'''.format(mailbox=mailbox, scope=self.search_scope)

        return mailbox_soap_element