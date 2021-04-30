# Welcome to py-ews's documentation!


```

    .______   ____    ____       ___________    __    ____   _______.
    |   _  \  \   \  /   /      |   ____\   \  /  \  /   /  /       |
    |  |_)  |  \   \/   / ______|  |__   \   \/    \/   /  |   (----`
    |   ___/    \_    _/ |______|   __|   \            /    \   \    
    |  |          |  |          |  |____   \    /\    / .----)   |   
    | _|          |__|          |_______|   \__/  \__/  |_______/    
                                                                 


    A Python package to interact with Exchange Web Services
```


**py-ews** is a cross platform python package to interact with both Exchange 2010 to 2019 on-premises and Exchange Online (Office 365). 

> This package will wrap all Exchange Web Service endpoints, but currently is focused on providing eDiscovery endpoints. 


## Features

**py-ews** has the following notable features in it's current release:

* Autodiscover support
* Delegation support
* Impersonation support
* Retrieve all mailboxes that can be searched based on credentials provided
* Search a list of (or single) mailboxes in your Exchange environment using all supported search attributes
* Delete email items from mailboxes in your Exchange environment
* Retrieve mailbox inbox rules for a specific account
* Find additional hidden inbox rules for a specified account
* Plus more supported endpoints

Currently this package supports the following endpoint's:

* [AddDelegate](docs/endpoint/adddelegate.md)
* [ConvertId](docs/endpoint/convertid.md)
* [CreateItem](docs/endpoint/createitem.md)
* [DeleteItem](docs/endpoint/deleteitem.md)
* [ExecuteSearch](docs/endpoint/executesearch.md)
* [ExpandDL](docs/endpoint/expanddl.md)
* [GetAttachment](docs/endpoint/getattachment.md)
* [GetHiddenInboxRules](docs/endpoint/gethiddeninboxrules.md)
* [GetInboxRules](docs/endpoint/getinboxrules.md)
* [GetItem](docs/endpoint/getitem.md)
* [GetSearchableMailboxes](docs/endpoint/getsearchablemailboxes.md)
* [GetServiceConfiguration](docs/endpoint/getserviceconfiguration.md)
* [GetUserSettings](docs/endpoint/getusersettings.md)
* [ResolveNames](docs/endpoint/resolvenames.md)
* [SearchMailboxes](docs/endpoint/searchmailboxes.md)
* [SyncFolderHierarchy](docs/endpoint/syncfolderhierarchy.md)
* [SyncFolderItems](docs/endpoint/syncfolderitems.md)


## Installation

### OS X & Linux:

```python
pip install py-ews
```

### Windows:

```python
pip install py-ews
```

## Creating EWS Object

When instantiating the `EWS` class you will need to provide credentials which will be used for all methods within the EWS class.

```python
from pyews import EWS

ews = EWS(
      'myaccount@company.com',
      'Password1234'
)
```

If you would like to use an alternative EWS URL then provide one using the `ews_url` parameter when instantiating the EWS class.

```python
from pyews import EWS

ews = EWS(
      'myaccount@company.com',
      'Password1234',
      ews_url='https://outlook.office365.com/autodiscover/autodiscover.svc'
)
```

If you would like to specify a specific version of Exchange to use, you can provide that using the `exchange_version` parameter. By default `pyews` will attempt all Exchange versions as well as multiple static and generated EWS URLs.

## Using Provided Methods

Once you have instantiated the EWS class with your credentials, you will have access to pre-exposed methods for each endpoint.  These methods are:

* get_service_configuration
* get_searchable_mailboxes
* get_user_settings
* resolve_names
* execute_ews_search
* execute_outlook_search
* get_inbox_rules
* get_hidden_inbox_rules
* get_item
* sync_folder_hierarchy
* sync_folder_items
* create_item

## Importing Endpoints

If you would like to write your own methods, you can import each endpoint directly into your script.

This example will demonstrate how you can identify which mailboxes you have access to by using the [GetSearchableMailboxes](docs/endpoint/getsearchablemailboxes.md) EWS endpoint.

```python
from pyews import Core
from pyews.endpoint import GetSearchableMailboxes

Core.exchange_versions = 'Exchange2016'
Core.credentials = ('mymailbox@mailbox.com', 'some password')
Core.endpoints = 'mailbox.com'

reference_id_list = []
for mailbox in GetSearchableMailboxes().run():
      reference_id_list.append(mailbox.get('reference_id'))
      print(mailbox)
```

Once you have identified a list of mailbox reference ids, then you can begin searching all of those mailboxes by using the [SearchMailboxes](docs/endpoint/searchmailboxes.md) EWS endpoint.

```python
from pyews.endpoint import SearchMailboxes

for search_item in SearchMailboxes('phish', reference_id_list).run():
      print(search_item)
```

**For more examples and usage, please refer to the individual class documentation**

* [Endpoint](docs/endpoint/root.md)

## Release History
 
* 1.0.0
    * Initial release of py-ews and it is still considered a work in progress
* 2.0.0
   * Revamped logic and overhauled all endpoints and classes
* 3.0.0
   * Refactored completely - this can be considered a new version


## Meta

Josh Rickard – [@MSAdministrator](https://twitter.com/MSAdministrator)

Distributed under the MIT license. See ``LICENSE`` for more information.

## Contributing

1. Fork it (<https://github.com/swimlane/pyews/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
