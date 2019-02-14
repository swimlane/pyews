# pyattck
A Python package to interact with the both on-premises and Office 365 Exchange Web Services

## Status
This package is currently under development and should be used internally only.

## Current Capabilities
Currently, this package has the following capabilities:

* Autodiscover: Limited testing but is able to be used to determine an EWS URL using Exchange Autodiscover
* GetSearchableMailboxes: Can retrieve a list of mailboxes to search 
* SearchMailboxes: Can search mailboxes based on either a GetSearchMailboxes object or your own list of mailbox Reference Ids

## Example Usage

```
import credentials
import autodiscover
import GetSearchableMailboxes
import exchangeversion
import xmltodict
import SearchMailboxes

# We first need to create a credential object
creds = credentials.Credentials('hackathon@swimlaneresearchdev.onmicrosoft.com', 'password')

# We provide that object to the Autodiscover service endpoint, which provides ewsurl and exchangeVersion attributes
# additonally, when using Autodiscover it will create a UserSettings object which has additional information used throughout
autodiscover = autodiscover.Autodiscover(credentials=creds)
print(autodiscover.usersettings.ExternalEwsUrl)

# as you can see the autodiscover.usersettings contains a CasVersion.  This is used to determine the exact ExchangeVersion needed for all SOAP request calls.
exchVer = exchangeVersion.ExchangeVersion(autodiscover.usersettings.CasVersion)
print(exchVer.exchangeVersion)

# We get can get all searchable mailboxes (automatically expanded) using the GetSearchableMailboxes endpoint
searchableMailboxes = GetSearchableMailboxes.GetSearchableMailboxes(credentials=creds, autodiscover=autodiscover)
for mailbox in searchableMailboxes.searchable_mailboxes:
    print(mailbox)

# We can also search all mailboxes by either providing a list of mailboxes ourselves or using the results from GetSearchableMailboxes.
# if you want to use Autodiscover then no need to provide a list of mailboxes, the SearchMailboxes class handles this.
mailbox_search = SearchMailboxes.SearchMailboxes('subject:Account', credentials=creds)
for results in mailbox_search.search_results:
    print(results)
```

## Notes
```yaml
   Name: pyews
   Created by: Josh Rickard
   Created Date: 02/14/2019
```