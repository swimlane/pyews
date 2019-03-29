
'''
from bs4 import BeautifulSoup
'''
text ='''<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types"
               xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages">
   <soap:Header>
      <t:RequestServerVersion Version="%s" />
   </soap:Header>
   <soap:Body >
      <m:GetSearchableMailboxes>
         <m:ExpandGroupMembership>true</m:ExpandGroupMembership>
      </m:GetSearchableMailboxes>
   </soap:Body>
</soap:Envelope>''' % 'Exchange2016'



impersonation = '''<t:ExchangeImpersonation xmlns:t='http://schemas.microsoft.com/exchange/services/2006/types'>
      <t:ConnectingSID>
        <t:PrincipalName />
        <t:SID />
        <t:PrimarySmtpAddress>josh.rickard@swimlane.com</t:PrimarySmtpAddress>
        <t:SmtpAddress />
      </t:ConnectingSID>
    </t:ExchangeImpersonation>'''



'''
def set_impersonation(self, bs_data, principalName=None, SID=None, primarySmtpAddress=None, smtpAddress=None)
    if principalName is not None:
        return self._new_impersonation_header(bs_data, 'PrincipalName')
    elif SID is not None:
        return self._new_impersonation_header(bs_data, 'SID')
    elif primarySmtpAddress is not None:
        return self._new_impersonation_header(bs_data, 'PrimarySmtpAddress')
    elif smtpAddress is not None:
        return self._new_impersonation_header(bs_data, 'SmtpAddress')

    
def _new_impersonation_header(self, bs_data, method, value):
    impersonation_header = bs_data.new_tag('ExchangeImpersonation', namespace='http://schemas.microsoft.com/exchange/services/2006/types', nsprefix='t')
    connectingSID = bs_data.new_tag('ConnectingSID', namespace='http://schemas.microsoft.com/exchange/services/2006/types', nsprefix='t')
    impersonation_method = bs_data.new_tag('%s' % method, namespace='http://schemas.microsoft.com/exchange/services/2006/types', nsprefix='t')

    connectingSID.append(impersonation_method)
    impersonation_header.append(connectingSID)
    header = bs_data.find('soap:Header')
    header.append(impersonation_header)

    # setting new impersonation header value
    bs_data.Envelope.Header.ExchangeImpersonation.ConnectingSID.method.string = value
    return bs_data

'''

'''
* UserConfiguration
** Credentials (services need this)
** Autodiscover ( or not) (services need this)
** impersonation settings (or not) (services needs this)
** Exchange version information (services needs this)

* ServiceConfiguration
** 

# Design Pattern

Credentials are needed to authenticate
User configuration has credentials
'''
from pyews.configuration import UserConfiguration


import pyews.service as SERVICE
#from pyews import GetSearchableMailboxes
#from pyews import GetInboxRules
#from pyews import SearchMailboxes
#from pyews import DeleteItem

#creds = Credentials('hackathon@swimlaneresearchdev.onmicrosoft.com', 'TWdrMHQUr7qNe!')

# Example of not using Autodiscover
'''
userconfig = UserConfiguration(
   'hackathon@swimlaneresearchdev.onmicrosoft.com',
   'TWdrMHQUr7qNe!',
   )

userconfig.update()


print(userconfig.UserDisplayName)
print(userconfig.UserDN)
print(userconfig.UserDeploymentId)
print(userconfig.CasVersion)
print(userconfig.EwsSupportedSchemas)
print(userconfig.InternalMailboxServer)
print(userconfig.MailboxDN)
print(userconfig.ExternalEwsUrl)
'''

userconfig = UserConfiguration(
   'hackathon@swimlaneresearchdev.onmicrosoft.com',
   'TWdrMHQUr7qNe!',
   exchangeVersion='Office365'
)


#print(userconfig.autodiscover)
#print(userconfig.configuration)
#print(userconfig.credentials.password)
#print(userconfig.credentials.email_address)
#print(userconfig.ewsUrl)
#print(userconfig.exchangeVersion)
#print(userconfig.raw_soap)

'''
userconfig = UserConfiguration(
   'hackathon@swimlaneresearchdev.onmicrosoft.com',
   'TWdrMHQUr7qNe!',
   autodiscover=False,
   ewsUrl='https://autodiscover-s.outlook.com/EWS/Exchange.asmx'
)
'''



# get searchable mailboxes based on your accounts permissions
referenceid_list = []
for mailbox in SERVICE.GetSearchableMailboxes(userconfig).response:
    referenceid_list.append(mailbox['ReferenceId'])

messages_found = []
for search in SERVICE.SearchMailboxes('subject:account', userconfig, referenceid_list).response:
    messages_found.append(search['MessageId'])
    # we can print the results first if we want
    #print(search['Subject'])
    #print(search['MessageId'])
    #print(search['Sender'])
    #print(search['ToRecipients'])
    #print(search['CreatedTime'])
    #print(search['ReceivedTime'])
    #etc.

# if we wanted to now delete a specific message then we would call the DeleteItem class
deleted_message_response = SERVICE.DeleteItem(messages_found[2], userconfig).response

#print(deleted_message_response)

# once you have the mailboxes "referenceIds" (example in SearchMailboxes below) you need to loop through them and provide either a single referenceid or a list of them
#print(SearchMailboxes('subject:account', userconfig, '/o=ExchangeLabs/ou=Exchange Administrative Group (FYDIBOHF23SPDLT)/cn=Recipients/cn=2ae3541cef834557aadf2fa434590af2-mailbox1').response)
#print(GetInboxRules('hackathon@swimlaneresearchdev.onmicrosoft.com', userconfig).response)
#(print(GetSearchableMailboxes(userconfig).response))

#print(temp_userconfig.ewsUrl)
#print(userconfig.update(temp_userconfig))
#print(userconfig.configuration)


# if a user chooses to not use Autodiscover, then they must provide a exchange_version and ews_url
#userconfig = UserConfiguration(
#   'hackathon@swimlaneresearchdev.onmicrosoft.com',
#   'TWdrMHQUr7qNe!',
#   autodiscover=False,
#   ews_url='https://outlook.office365.com/EWS/Exchange.asmx'
#)


#UserConfiguration()

'''
UserConfiguration()

UserConfiguration(
   username,
   password,
   autodiscover=True,

   creds = Credentials('hackathon@swimlaneresearchdev.onmicrosoft.com', 'TWdrMHQUr7qNe!')

# We provide that object to the Autodiscover service endpoint, which provides ewsurl and exchangeVersion attributes
# additonally, when using Autodiscover it will create a UserSettings object which has additional information used throughout
autodiscover = Autodiscover(credentials=creds, exchangeVersion='Office365')
print("External EWS Url: %s" % autodiscover.usersettings.ExternalEwsUrl)

# as you can see the autodiscover.usersettings contains a CasVersion.  This is used to determine the exact ExchangeVersion needed for all SOAP request calls.
exchVer = ExchangeVersion(autodiscover.usersettings.CasVersion)
)


ServiceConfiguration(userConfig).GetSearchableMailboxes()
'''