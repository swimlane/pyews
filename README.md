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
* OAUth2 support
* Retrieve all mailboxes that can be searched based on credentials provided
* Search a list of (or single) mailboxes in your Exchange environment using all supported search attributes
* Delete email items from mailboxes in your Exchange environment
* Retrieve mailbox inbox rules for a specific account
* Find additional hidden inbox rules for a specified account
* Plus more supported endpoints

Currently this package supports the following endpoint's:

* [AddDelegate](docs/endpoint/adddelegate.md)
* [ConvertId](docs/endpoint/convertid.md)
* [CreateFolder](docs/endpoint/createfolder.md)
* [CreateItem](docs/endpoint/createitem.md)
* [DeleteFolder](docs/endpoint/deletefolder.md)
* [DeleteItem](docs/endpoint/deleteitem.md)
* [ExecuteSearch](docs/endpoint/executesearch.md)
* [ExpandDL](docs/endpoint/expanddl.md)
* [FindFolder](docs/endpoint/findfolder.md)
* [FindItem](docs/endpoint/finditem.md)
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

For convience, `py-ews` offers a simple interface to access all available EWS `endpoints` in the form of methods.  Each of these methods have
their own required inputs based on the individual endpoint. No matter which endpoint you use, you must first instantiate the `EWS` class by providing
authentication details.

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

Finally, if you would like to `impersonate_as` a specific user you must provide their primary SMTP address when instantiating the `EWS` class object:


```python
from pyews import EWS

ews = EWS(
      'myaccount@company.com',
      'Password1234',
      impersonate_as='myotheraccount@company.com'
)
```

### Exchange Search Multi-Threading

You can also specify `multi_threading=True` and when you search mailboxes we will use multi-threading to perform the search.

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
* get_attachment
* sync_folder_hierarchy
* sync_folder_items
* create_item
* delete_item
* search_and_delete_message
* get_domain_settings
* find_items
* search_mailboxes_using_find_item
* create_search_folder
* find_search_folder
* delete_search_folder

## Access Classes Directly

In some cases you may want to skip using the `EWS` interface class and build your own wrapper around `py-ews`.  To do this, you must first import the `Authentication` class and provide
credential and other details before invoking a desired `endpoint`. Below is an example of this:

```python
from pyews import Authentication, GetSearchableMailboxes

Authentication(
      'myaccount@company.com',
      'Password1234'
)

reference_id_list = []
for mailbox in GetSearchableMailboxes().run():
      reference_id_list.append(mailbox.get('reference_id'))
      print(mailbox)
```

As you can see, you must instantiate the `Authentication` class first before calling an endpoint.  By the way, you can import all `endpoints` directly without using the `EWS` interface.

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
