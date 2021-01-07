import re
import xmltodict
import json

from ..core import Core
from .getitem import GetItem
from pyews.utils.exchangeversion import ExchangeVersion
from pyews.utils.exceptions import ObjectType, DeleteTypeError, SoapResponseHasError, SoapAccessDeniedError, SearchScopeError


class SearchMailboxes(Core):
    '''Search mailboxes based on a search query.  
        
    Examples:
            
    To use any service class you must provide a UserConfiguration object first.
    Like all service classes, you can access formatted properties from the EWS endpoint using the `response` property.
    
    The search query parameter takes a specific format, below are examples of different situations
    as well as comments that explain that situation:

    ```python
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
    ```

    For more information take a look at Microsoft's documentation for their= `Advanced Query Syntax (AQS) <https://docs.microsoft.com/en-us/exchange/client-developer/web-service-reference/querystring-querystringtype>`_

    
    By passing in a search_query, UserConfiguration object, and a mailbox_id we can search that specific mailbox or a list of mailbox referenceIds

    ```python
    from pyews import UserConfiguration
    from pyews import SearchMailboxes

    userConfig = UserConfiguration(
        'first.last@company.com',
        'mypassword123'
    )

    referenceId = '/o=ExchangeLabs/ou=Exchange Administrative Group (FYDIBOHF23SPDLT)/cn=Recipients/cn=5341a4228e8c433ba81b4b4b6d75e100-last.first'
    searchResults = SearchMailboxes(userConfig).run('subject:account', referenceId)
    ```

    Args:
        search_query (str): A EWS QueryString.  More information can be found at https://docs.microsoft.com/en-us/exchange/client-developer/web-service-reference/querystring-querystringtype
        userconfiguration (UserConfiguration): A UserConfiguration object created using the UserConfiguration class
        mailbox_id (str or list): A single or list of mailbox IDs to search.  This mailbox id is a ReferenceId
        search_scope (str, optional): Defaults to 'All'. The search scope for the provided mailbox ids.  The options are ['All', 'PrimaryOnly', 'ArchiveOnly']
    
    Raises:
        ObjectType: An incorrect object type has been used
        SearchScopeError: The provided search scope is not one of the following options: ['All', 'PrimaryOnly', 'ArchiveOnly']
    '''

    def __init__(self, userconfiguration):
        super(SearchMailboxes, self).__init__(userconfiguration)
        self.__get_item = GetItem(userconfiguration)

    def __process_keys(self, key):
        return_value = key.replace('t:','')
        if return_value.startswith('@'):
            return_value = return_value.lstrip('@')
        return self.camel_to_snake(return_value)

    def __process_dict(self, obj):
        if isinstance(obj, dict):
            obj = {
                self.__process_keys(key): self.__process_dict(value) for key, value in obj.items()
                }
        return obj

    def __process_single_change(self, value):
        ordered_dict = xmltodict.parse(str(value))
        item_dict = json.loads(json.dumps(ordered_dict))
        return self.__process_dict(item_dict)

    def __parse_response(self, value):
        '''Creates and sets a response object
        
        Args:
            value (str): The raw response from a SOAP request
        '''
        return_list = []
        if value.find('ResponseCode').string == 'NoError':
            for item in value.find_all('SearchPreviewItem'):
                new_dict = self.__process_single_change(item).pop('search_preview_item')
                if new_dict.get('id'):
                    try:
                        new_dict.update(self.__get_item.run(new_dict['id'].get('id')))
                    except:
                        pass
                return_list.append(new_dict)
        return return_list

    def run(self, search_query, mailbox_list, search_scope='All'):
        self.search_query = search_query
        if search_scope in ['All', 'PrimaryOnly', 'ArchiveOnly']:
            self.search_scope = search_scope
        else:
            raise SearchScopeError('Please use the default SearchScope of All or specify PrimaryOnly or ArchiveOnly')
        self.raw_xml = self.invoke(self.soap(mailbox_list))
        return self.__parse_response(self.raw_xml)

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
</soap:Envelope>'''.format(
    version=self.userconfiguration.exchange_version, 
    header=impersonation_header, 
    query=self.search_query, 
    scope=mailbox_search_scope)

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
