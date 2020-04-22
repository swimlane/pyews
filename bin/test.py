
from pyews import UserConfiguration

# Example of using Autodiscover

userconfig = UserConfiguration(
   'first.last@dev.onmicrosoft.com',
   'password',
)

# you can print properties on the useconfig object if needed

#print(userconfig.autodiscover)
#print(userconfig.configuration)
#print(userconfig.credentials.password)
#print(userconfig.credentials.email_address)
#print(userconfig.ewsUrl)
#print(userconfig.exchangeVersion)
#print(userconfig.raw_soap)

# Example of NOT using Autodiscover
'''
userconfig = UserConfiguration(
   'first.last@dev.onmicrosoft.com',
   'password',
   autodiscover=False,
   ewsUrl='https://autodiscover-s.outlook.com/EWS/Exchange.asmx'
)
'''



# get searchable mailboxes based on your accounts permissions

from pyews import GetSearchableMailboxes

referenceid_list = []
for mailbox in GetSearchableMailboxes(userconfig).response:
    referenceid_list.append(mailbox['ReferenceId'])

#print(referenceid_list)

from pyews import SearchMailboxes
messages_found = []
for search in SearchMailboxes('subject:"OMG PHISHING EMAIL"', userconfig, referenceid_list).response:
    messages_found.append(search['MessageId'])
    # we can print the results first if we want
    print(search['Subject'])
    print(search['MessageId'])
    print(search['Sender'])
    print(search['ToRecipients'])
    print(search['CreatedTime'])
    print(search['ReceivedTime'])
    #etc.

#print(messages_found)


# if we wanted to now delete a specific message then we would call the DeleteItem class

#from pyews import DeleteItem
#deleted_message_response = DeleteItem(messages_found[0], userconfig).response

#print(deleted_message_response)

# once you have the mailboxes "referenceIds" (example in SearchMailboxes below) you need to loop through them and provide either a single referenceid or a list of them

#from pyews import SearchMailboxes
#mailboxSearch = SearchMailboxes('subject:account', userconfig, '/o=ExchangeLabs/ou=Exchange Administrative Group (FYDIBOHF23SPDLT)/cn=Recipients/cn=2ae3541cef834557aadf2fa434590af2-mailbox1').response
#print(mailboxSearch)

# We can get InboxRules as well

#from pyews import GetInboxRules
#mailboxRules = GetInboxRules('first.last@dev.onmicrosoft.com', userconfig).response