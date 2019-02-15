from credentials import Credentials
from autodiscover import Autodiscover
from GetSearchableMailboxes import GetSearchableMailboxes
from exchangeversion import ExchangeVersion
from SearchMailboxes import SearchMailboxes
from DeleteItem import DeleteItem

creds = Credentials('hackathon@swimlaneresearchdev.onmicrosoft.com', 'TWdrMHQUr7qNe!')
#autodiscover = autodiscover.Autodiscover(
#    credentials=creds,
#    exchangeVersion='Office365'
#)
#print(autodiscover.usersettings.ExternalEwsUrl)

#exchVer = exchangeVersion.ExchangeVersion(autodiscover.usersettings.CasVersion)
#print(exchVer.exchangeVersion)

#searchableMailboxes = GetSearchableMailboxes(credentials=creds, exchangeVersion='Office365')
#searchableMailboxes = GetSearchableMailboxes.GetSearchableMailboxes(credentials=creds, autodiscover=autodiscover)
#print(type(searchableMailboxes))
#for mailbox in searchableMailboxes.results:
#    print(mailbox['ReferenceId'])

mailbox_search = SearchMailboxes('subject:Account', credentials=creds, exchangeVersion='Office365')
#mailbox_search = SearchMailboxes.SearchMailboxes('subject:Account', credentials=creds, )
for results in mailbox_search.results:
    print(results['Id'])

delete_item_response = DeleteItem(
    'AAMkAGZjOTlkOWExLTM2MDEtNGI3MS04ZDJiLTllNzgwNDQxMThmMABGAAAAAABdQG8UG7qjTKf0wCVbqLyMBwC6DuFzUH4qRojG/OZVoLCfAAAAAAEbAAC6DuFzUH4qRojG/OZVoLCfAAAOh+uUAAA=',
    credentials=creds, exchangeVersion='Office365'
)